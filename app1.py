import streamlit as st
import requests
import json
import io
import base64

# ── PAGE CONFIG ───────────────────────────────
st.set_page_config(
    page_title="LinguaFlow – AI Translation Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@700&display=swap');
:root{--bg:#0d1117;--card:#161b22;--input:#21262d;--border:#30363d;
      --accent:#00d4ff;--adim:#00d4ff22;--fg:#e6edf3;--muted:#8b949e;
      --ok:#3fb950;--err:#f85149;--r:12px;}
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:var(--bg)!important;color:var(--fg)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:2rem 2rem 4rem!important;max-width:1100px;margin:auto;}
.hero{text-align:center;padding:2rem 1rem 1rem;}
.hero h1{font-family:'Space Grotesk',sans-serif;font-size:2.8rem;font-weight:700;
  background:linear-gradient(135deg,#00d4ff,#a78bfa);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;margin:0 0 .3rem;}
.hero p{color:var(--muted);font-size:.95rem;margin:0;}
.lbl{font-size:.7rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.4rem;}
textarea{background:var(--input)!important;color:var(--fg)!important;border:1px solid var(--border)!important;
  border-radius:10px!important;font-size:1rem!important;resize:vertical!important;}
textarea:focus{border-color:var(--accent)!important;box-shadow:0 0 0 3px var(--adim)!important;outline:none!important;}
.stSelectbox>div>div{background:var(--input)!important;border:1px solid var(--border)!important;
  border-radius:10px!important;color:var(--fg)!important;}
.stButton>button{background:linear-gradient(135deg,#00d4ff,#0097b2)!important;
  color:#0d1117!important;font-weight:700!important;border:none!important;border-radius:10px!important;
  padding:.55rem 1.4rem!important;transition:transform .15s,box-shadow .15s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 20px rgba(0,212,255,.3)!important;}
.outbox{background:var(--input);border:1px solid var(--accent);border-radius:var(--r);
  padding:1.2rem 1.4rem;min-height:130px;font-size:1.05rem;line-height:1.7;
  white-space:pre-wrap;word-break:break-word;box-shadow:0 0 0 1px var(--adim);}
.ph{color:var(--muted);font-style:italic;}
.strip{border-radius:0 8px 8px 0;padding:.65rem 1rem;font-size:.88rem;margin-top:.6rem;}
.info{background:#161b22;border-left:3px solid var(--accent);color:var(--muted);}
.good{background:#0d1f14;border-left:3px solid var(--ok);color:var(--ok);}
.bad {background:#1f1418;border-left:3px solid var(--err);color:var(--err);}
.stats{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:.7rem;}
.pill{background:var(--input);border:1px solid var(--border);border-radius:8px;
  padding:.3rem .75rem;font-size:.76rem;color:var(--muted);}
.pill b{color:var(--accent);}
.ttsbox{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:.9rem 1.1rem;margin-top:.8rem;}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.3rem 1.5rem;margin-bottom:1rem;}
hr.div{border:none;border-top:1px solid var(--border);margin:1.5rem 0;}
.cc{text-align:right;font-size:.73rem;color:var(--muted);margin-top:.2rem;}
.warn{color:#e3b341!important;} .over{color:var(--err)!important;}
audio{width:100%;border-radius:8px;margin-top:.4rem;}
.footer{text-align:center;padding:2rem 0 .5rem;font-size:.76rem;color:var(--muted);}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────
LANGUAGES = {
    "Auto Detect":"auto","Afrikaans":"af","Albanian":"sq","Arabic":"ar",
    "Armenian":"hy","Azerbaijani":"az","Bengali":"bn","Bulgarian":"bg",
    "Catalan":"ca","Chinese (Simplified)":"zh-CN","Chinese (Traditional)":"zh-TW",
    "Croatian":"hr","Czech":"cs","Danish":"da","Dutch":"nl","English":"en",
    "Finnish":"fi","French":"fr","Georgian":"ka","German":"de","Greek":"el",
    "Gujarati":"gu","Hebrew":"iw","Hindi":"hi","Hungarian":"hu","Indonesian":"id",
    "Irish":"ga","Italian":"it","Japanese":"ja","Kannada":"kn","Korean":"ko",
    "Latvian":"lv","Lithuanian":"lt","Malay":"ms","Maltese":"mt","Marathi":"mr",
    "Nepali":"ne","Norwegian":"no","Persian":"fa","Polish":"pl","Portuguese":"pt",
    "Punjabi":"pa","Romanian":"ro","Russian":"ru","Serbian":"sr","Sinhala":"si",
    "Slovak":"sk","Slovenian":"sl","Spanish":"es","Swahili":"sw","Swedish":"sv",
    "Tamil":"ta","Telugu":"te","Thai":"th","Turkish":"tr","Ukrainian":"uk",
    "Urdu":"ur","Uzbek":"uz","Vietnamese":"vi","Welsh":"cy","Yoruba":"yo","Zulu":"zu",
}
SRC_OPTS  = list(LANGUAGES.keys())
TGT_OPTS  = [l for l in SRC_OPTS if l != "Auto Detect"]
MAX_CHARS = 500
GTTS_MAP  = {v: v for v in LANGUAGES.values()}   # gTTS accepts same codes

DEMOS = {
    "👋 Greeting":  "Hello! How are you? I hope you are doing well today.",
    "📚 Education": "Artificial intelligence is transforming the way we learn and work in the modern era.",
    "🌍 Travel":    "I would like to book a hotel room near the city center for three nights.",
}

# ── SESSION STATE INIT ────────────────────────
def _init():
    defs = dict(
        translation="", last_src="", api_used="", detected="",
        history=[], errmsg="", copymsg="",
        src_lang="Auto Detect", tgt_lang="Urdu",
        input_text="",
        tts_b64="", tts_lbl="",
        # flags set by buttons BEFORE widgets render
        _pending_demo="",   # demo phrase to load
        _do_swap=False,     # swap was requested
    )
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

# ══════════════════════════════════════════════
#  PROCESS FLAGS — runs at TOP of every rerun,
#  BEFORE any widget is created.
#  This is the only safe place to change values
#  that widgets will read.
# ══════════════════════════════════════════════
if st.session_state._pending_demo:
    st.session_state.input_text    = st.session_state._pending_demo
    st.session_state.translation   = ""
    st.session_state.tts_b64       = ""
    st.session_state.errmsg        = ""
    st.session_state._pending_demo = ""

if st.session_state._do_swap:
    if st.session_state.src_lang != "Auto Detect":
        old_src = st.session_state.src_lang
        old_tgt = st.session_state.tgt_lang
        st.session_state.src_lang = old_tgt
        st.session_state.tgt_lang = old_src
        if st.session_state.translation:
            st.session_state.input_text  = st.session_state.translation
            st.session_state.translation = ""
            st.session_state.tts_b64     = ""
    else:
        st.session_state.errmsg = "Select a specific source language before swapping."
    st.session_state._do_swap = False

# ── HELPERS ───────────────────────────────────
def do_translate(text, src_name, tgt_name):
    src = LANGUAGES[src_name]
    tgt = LANGUAGES[tgt_name]
    pair = f"autodetect|{tgt}" if src == "auto" else f"{src}|{tgt}"
    try:
        r = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": pair, "de": "student@linguaflow.ai"},
            timeout=10,
        )
        r.raise_for_status()
        d = r.json()
        if d.get("responseStatus") == 200:
            return {"ok": True, "text": d["responseData"]["translatedText"],
                    "detected": d.get("responseData", {}).get("detectedLanguage", ""),
                    "api": "MyMemory"}
        return {"ok": False, "err": d.get("responseDetails", "Translation failed.")}
    except Exception as e:
        # fallback
        try:
            r2 = requests.post("https://libretranslate.com/translate",
                               json={"q": text, "source": src if src!="auto" else "auto",
                                     "target": tgt, "format": "text"}, timeout=12)
            if r2.status_code == 200:
                return {"ok": True, "text": r2.json().get("translatedText",""), "api": "LibreTranslate"}
        except Exception:
            pass
        return {"ok": False, "err": str(e)}

def do_tts(text, lang_code):
    try:
        from gtts import gTTS
        lc  = "en" if lang_code == "auto" else lang_code
        buf = io.BytesIO()
        gTTS(text=text, lang=lc, slow=False).write_to_fp(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
    except Exception:
        return None

# ── HERO ──────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🌐 LinguaFlow</h1>
  <p>AI-Powered Translation &nbsp;·&nbsp; 60+ Languages &nbsp;·&nbsp; Free API &nbsp;·&nbsp; Text-to-Speech</p>
</div>""", unsafe_allow_html=True)

# ── DEMO BUTTONS ──────────────────────────────
st.markdown('<div class="lbl" style="margin-top:.5rem">⚡ Quick Demo Phrases</div>', unsafe_allow_html=True)
_dc = st.columns(3)
for _col, (_lbl, _phrase) in zip(_dc, DEMOS.items()):
    if _col.button(_lbl, use_container_width=True, key=f"db_{_lbl[:2]}"):
        # Store phrase in flag — widget render hasn't happened yet next rerun
        st.session_state._pending_demo = _phrase
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── MAIN LAYOUT ───────────────────────────────
lcol, rcol = st.columns([1, 1], gap="large")

with lcol:
    st.markdown('<div class="lbl">Source Language</div>', unsafe_allow_html=True)

    # selectbox index derived from session state — NO key= used
    _si = SRC_OPTS.index(st.session_state.src_lang) if st.session_state.src_lang in SRC_OPTS else 0
    src_lang = st.selectbox("src", SRC_OPTS, index=_si, label_visibility="collapsed")
    st.session_state.src_lang = src_lang   # sync manual user changes

    st.markdown('<div class="lbl" style="margin-top:1rem">Enter Text</div>', unsafe_allow_html=True)

    # textarea value from session state — NO key= used
    source_text = st.text_area("txt", value=st.session_state.input_text,
                                height=200, placeholder="Type or paste text here…",
                                label_visibility="collapsed")
    st.session_state.input_text = source_text   # sync manual user changes

    _cc = len(source_text)
    _cls = "over" if _cc > MAX_CHARS else ("warn" if _cc > MAX_CHARS*0.8 else "")
    st.markdown(f'<div class="cc {_cls}">{_cc} / {MAX_CHARS}</div>', unsafe_allow_html=True)

with rcol:
    st.markdown('<div class="lbl">Target Language</div>', unsafe_allow_html=True)

    _ti = TGT_OPTS.index(st.session_state.tgt_lang) if st.session_state.tgt_lang in TGT_OPTS else TGT_OPTS.index("Urdu")
    tgt_lang = st.selectbox("tgt", TGT_OPTS, index=_ti, label_visibility="collapsed")
    st.session_state.tgt_lang = tgt_lang

    st.markdown('<div class="lbl" style="margin-top:1rem">Translated Output</div>', unsafe_allow_html=True)
    if st.session_state.translation:
        st.markdown(f'<div class="outbox">{st.session_state.translation}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="outbox"><span class="ph">Translation will appear here…</span></div>', unsafe_allow_html=True)

    if st.session_state.translation:
        _w = len(st.session_state.translation.split())
        _c = len(st.session_state.translation)
        _a = st.session_state.api_used or "—"
        _d = st.session_state.detected or "—"
        _dh = f'<div class="pill">Detected: <b>{_d}</b></div>' if _d != "—" else ""
        st.markdown(f"""<div class="stats">
            <div class="pill">Words: <b>{_w}</b></div>
            <div class="pill">Chars: <b>{_c}</b></div>
            <div class="pill">API: <b>{_a}</b></div>{_dh}
        </div>""", unsafe_allow_html=True)

    # TTS
    if st.session_state.translation:
        st.markdown('<div class="ttsbox"><div class="lbl">🔊 Text-to-Speech</div>', unsafe_allow_html=True)
        _t1, _t2 = st.columns(2)
        if _t1.button("▶ Source",      use_container_width=True, key="tts_src"):
            _lc = LANGUAGES.get(src_lang, "en")
            _au = do_tts(source_text or st.session_state.last_src, _lc)
            if _au:
                st.session_state.tts_b64 = _au
                st.session_state.tts_lbl = f"Source ({src_lang})"
            else:
                st.session_state.errmsg = "TTS failed. Install: pip install gtts"
        if _t2.button("▶ Translation", use_container_width=True, key="tts_tgt"):
            _lc = LANGUAGES.get(tgt_lang, "en")
            _au = do_tts(st.session_state.translation, _lc)
            if _au:
                st.session_state.tts_b64 = _au
                st.session_state.tts_lbl = f"Translation ({tgt_lang})"
            else:
                st.session_state.errmsg = "TTS failed. Install: pip install gtts"
        if st.session_state.tts_b64:
            st.markdown(f'<div style="font-size:.75rem;color:#8b949e">🎵 {st.session_state.tts_lbl}</div>'
                        f'<audio controls autoplay src="data:audio/mp3;base64,{st.session_state.tts_b64}"></audio>',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _ba, _bb, _bc = st.columns([2, 1, 1])
    _go    = _ba.button("🔁 Translate", use_container_width=True, key="btn_go")
    _copy  = _bb.button("📋 Copy",      use_container_width=True, key="btn_copy")
    _clear = _bc.button("🗑 Clear",      use_container_width=True, key="btn_clear")

# ── ACTIONS ───────────────────────────────────
if _clear:
    for k in ("translation","last_src","api_used","detected","errmsg","input_text","tts_b64","tts_lbl","copymsg"):
        st.session_state[k] = ""
    st.rerun()

if _copy:
    if st.session_state.translation:
        st.session_state.copymsg = "ok"
        st.components.v1.html(
            f"<script>navigator.clipboard.writeText({json.dumps(st.session_state.translation)});</script>",
            height=0)
    else:
        st.session_state.copymsg = "empty"

if st.session_state.copymsg == "ok":
    st.markdown('<div class="strip good">✅ Copied to clipboard!</div>', unsafe_allow_html=True)
    st.session_state.copymsg = ""
elif st.session_state.copymsg == "empty":
    st.markdown('<div class="strip info">ℹ️ Nothing to copy yet.</div>', unsafe_allow_html=True)
    st.session_state.copymsg = ""

if _go:
    st.session_state.errmsg = ""
    st.session_state.tts_b64 = ""
    _txt = source_text.strip()
    if not _txt:
        st.session_state.errmsg = "Please enter some text."
    elif len(_txt) > MAX_CHARS:
        st.session_state.errmsg = f"Too long — max {MAX_CHARS} chars."
    elif src_lang != "Auto Detect" and src_lang == tgt_lang:
        st.session_state.errmsg = "Source and target are the same language."
    else:
        with st.spinner("Translating…"):
            res = do_translate(_txt, src_lang, tgt_lang)
        if res["ok"]:
            st.session_state.translation = res["text"]
            st.session_state.last_src    = _txt
            st.session_state.api_used    = res.get("api", "")
            st.session_state.detected    = res.get("detected", "")
            st.session_state.history.append({
                "s": src_lang, "t": tgt_lang,
                "o": _txt[:80]+("…" if len(_txt)>80 else ""),
                "r": res["text"][:80]+("…" if len(res["text"])>80 else ""),
            })
            st.session_state.history = st.session_state.history[-10:]
            st.rerun()
        else:
            st.session_state.errmsg = res.get("err", "Unknown error.")
            st.rerun()

if st.session_state.errmsg:
    st.markdown(f'<div class="strip bad">⚠️ {st.session_state.errmsg}</div>', unsafe_allow_html=True)

# ── SWAP ──────────────────────────────────────
st.markdown("<hr class='div'>", unsafe_allow_html=True)
_sc, _, _ic = st.columns([1, 2, 1])
with _sc:
    if st.button("⇄ Swap Languages", use_container_width=True, key="btn_swap"):
        st.session_state._do_swap = True   # processed at TOP of next rerun
        st.rerun()
with _ic:
    st.markdown('<div style="text-align:right;font-size:.76rem;color:#8b949e;padding-top:.5rem;">'
                'Powered by <b style="color:#00d4ff">MyMemory</b> &amp; gTTS</div>', unsafe_allow_html=True)

# ── HISTORY ───────────────────────────────────
if st.session_state.history:
    with st.expander("📜 Translation History (last 10)"):
        for _i, _h in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"""<div class="card" style="margin-bottom:.5rem;">
                <div style="font-size:.7rem;color:#8b949e">#{_i} · {_h['s']} → {_h['t']}</div>
                <div style="font-size:.87rem"><b>Original:</b> {_h['o']}</div>
                <div style="font-size:.87rem;color:#00d4ff"><b>Translated:</b> {_h['r']}</div>
            </div>""", unsafe_allow_html=True)
    if st.button("🗑 Clear History", key="btn_clrhist"):
        st.session_state.history = []
        st.rerun()

# ── INFO ──────────────────────────────────────
with st.expander("ℹ️ How It Works"):
    st.markdown("""<div class="card">
    <h4 style="color:#00d4ff;margin-top:0">🔧 Stack</h4>
    <ol>
      <li><b>MyMemory API</b> — Free, no key, 1000 words/day</li>
      <li><b>LibreTranslate</b> — Auto-fallback</li>
      <li><b>gTTS</b> — Text-to-Speech (pip install gtts)</li>
    </ol>
    <h4 style="color:#00d4ff">✅ Features</h4>
    <ul>
      <li>60+ languages · Auto-detect · Demo phrases · Swap · History · TTS · Copy</li>
    </ul>
    <pre style="background:#21262d;padding:.7rem;border-radius:8px;font-size:.8rem;">pip install streamlit requests gtts
streamlit run app.py</pre></div>""", unsafe_allow_html=True)

st.markdown('<div class="footer">LinguaFlow · Streamlit + MyMemory + gTTS · AI Internship Project</div>',
            unsafe_allow_html=True)

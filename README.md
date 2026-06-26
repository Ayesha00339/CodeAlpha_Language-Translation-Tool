# # 🌍 Language Translation Tool

A modern and user-friendly **🌐 LinguaFlow – AI Language Translation Tool** built with **Python** and **Streamlit**. The application allows users to translate text between multiple languages using free online translation APIs. It provides an intuitive interface with features such as automatic language detection, translation history, language swapping, and one-click copy functionality.

---

# 📌 Introduction

The **🌐 LinguaFlow – AI Language Translation Tool**  is a fully-featured, professionally designed Language Translation Tool, designed to make communication across different languages simple and accessible. Users can enter text, select the source and target languages, and instantly receive accurate translations. The project integrates free translation APIs, eliminating the need for paid API keys while providing a smooth user experience. It is developed using Python and Streamlit, a modern web framework for AI applications, and supports translation across 60+ languages including Urdu, Arabic, Hindi, Chinese, Japanese, French, German, and many more.
The tool uses a smart dual-API fallback strategy: it calls the MyMemory Translation API as the primary engine (free, no key required), and automatically falls back to LibreTranslate if needed. The user interface is clean, dark-themed, and includes features like language auto-detection, translation history, one-click copy, language swap, character guard, and output statistics.

---

# ✨ Features

* 🌐 Translate text between **60+ languages**
* 🔍 Automatic source language detection
* 🔄 Swap source and target languages with one click
* 📜 Translation history (stores recent translations i.e., last 10)
* 📋 Copy translated text to clipboard
* 📊 Character counter and translation statistics
* ⚡ Fast and responsive Streamlit interface
* 🔁 Automatic fallback to a secondary translation API if the primary service is unavailable
* 💯 Uses **free APIs** (no paid API key required)

---

# 🛠️ Technologies Used

* Python 3.x (main programming language)
* Streamlit (web UI framework for AI/ML apps)
* Requests (HTTP library for API calls)
* MyMemory Translation API
* LibreTranslate API

---

# 📂 Project Structure

```text
translation_tool/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Required Python packages
└── README.md           # Project documentation
```

---

# 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/language-translation-tool.git
```

### 2. Navigate to the project folder

```bash
cd language-translation-tool
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

After running the command, open your browser and visit:

```
http://localhost:8501
```

---

# 🔗 APIs Used

## 1. MyMemory Translation API

* URL: https://api.mymemory.translated.net/get
* Free to use
* Primary engine (1000 words/day)
* No API key required
* Supports multiple languages
* Used as the primary translation service
* Docs: https://mymemory.translated.net/doc/spec.php

---

## 2. LibreTranslate API

* URL: https://libretranslate.com/translate
* Free public translation API
* Used as a backup if the primary API fails
* Docs: https://libretranslate.com/docs

---

# 🔧 Architecture & Flow

* User enters text and selects source/target languages in the Streamlit UI
* Input is validated (empty check, 500-char limit, same-language guard)
* App sends GET request to MyMemory REST API with language pair and text
* If successful: parsed JSON response is displayed in the output box
* If failed: automatically retries with LibreTranslate as fallback
* Output stats (word count, char count, API used, detected language) shown
* Translation is saved to session history (last 10 entries retained)

---

# 📖 How It Works

1. Enter the text you want to translate.
2. Select the source language or choose **Auto Detect**.
3. Select the target language.
4. Click the **Translate** button.
5. The translated text is displayed instantly.
6. Copy the result or review previous translations from the history section.

---

# 🎯 Project Objectives

* Build an interactive translation application.
* Integrate external REST APIs.
* Demonstrate real-time API communication.
* Provide a simple and responsive user interface.
* Enhance usability with additional features such as translation history and copy functionality.

---

# 📸 Application Features

* User-friendly interface
* Real-time translation
* Language selection
* Auto language detection
* Translation history
* Copy to clipboard
* Character limit indicator
* Translation statistics

---

# 🔮 Future Improvements

* Text-to-Speech support
* Speech-to-Text translation
* Dark Mode
* Save translation history locally
* Download translations as PDF or TXT
* Favorite translations
* OCR (Image to Text Translation)

---

# 👨‍💻 Author 
Intern: **AYESHA BUKHARI**

AI Intership by **CodeAlpha**

**🌐 LinguaFlow – AI Language Translation Tool** Developed using **Python**, **Streamlit**, and **Translation APIs**.

---

# 📄 License

This project is intended for educational and learning purposes. Feel free to modify and improve it for personal or academic use.

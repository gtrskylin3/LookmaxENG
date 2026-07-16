# LookmaxENG
![image](/image.png)
LookmaxENG is a lightweight Windows application for learning English while playing games or reading text on the screen.

The application captures a small region around the mouse cursor, recognizes the text using the native Windows OCR engine, determines the word under the cursor, and will later provide translation, history, and Anki integration.


## Features

* ⚡ Fast OCR using the built-in Windows OCR API (WinRT)
* 🎯 Detects the exact word under the mouse cursor
* 🖼 Captures only a small screen region for better performance
* ⌨️ Global hotkey support
* 🇬🇧 English learning while gaming
* 📚 Planned word history and vocabulary management
* 🔄 Planned Anki export

## How it works

```text
Hotkey
   │
   ▼
Get mouse position
   │
   ▼
Capture screen region
   │
   ▼
Windows OCR
   │
   ▼
Extract words and their coordinates
   │
   ▼
Find the word under the cursor
   │
   ▼
Translate and save
```

## Current project status

### ✅ Implemented

* Screen capture around the cursor
* Windows OCR integration
* Word parsing with bounding boxes
* Cursor-to-word detection
* Modular project structure

### 🚧 In progress

* Translation service
* Popup window
* Local word database
* Anki export
* OCR engine caching
* Better UI/UX

## Project structure

```text
lookmaxeng/
│
├── ocr/                # OCR engine and parsing
├── schemes/            # Data models
├── config.py
├── main.py             # Application entry point
└── README.md
```

## Requirements

* Windows 10 / Windows 11
* Python 3.12+
* English OCR language pack installed

If OCR is not available, install it from PowerShell:

```powershell
Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0"
```

## Installation

```bash
git clone https://github.com/yourusername/lookmaxeng.git

cd lookmaxeng

uv sync
```

## Running

```bash
python main.py
```

Default hotkey:

```text
Shift + Alt + Q
```

Move the cursor over a word and press the hotkey.

The application will detect the word located under the cursor.

## Motivation

Reading while playing games is one of the most effective ways to build vocabulary.

Instead of interrupting gameplay to search for unknown words, LookmaxENG is designed to recognize the word directly under the cursor and make the lookup process almost instantaneous.

## Roadmap

* [x] Screen capture
* [x] Windows OCR
* [x] Word detection
* [ ] Translation
* [ ] Popup interface
* [ ] SQLite vocabulary database
* [ ] Word frequency statistics
* [ ] Anki export
* [ ] Automatic language detection
* [ ] Multi-monitor support

✓ перевод слова
↓
✓ красивое всплывающее окно
↓
✓ горячая клавиша без лагов
↓
✓ кэш OCR Engine
↓
✓ экспорт в Anki
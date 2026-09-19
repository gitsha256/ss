# Coding Assistant AI

> **Multi-Agent Screen Solver with LangGraph & Free LLM Routing**

[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#license)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](#prerequisites)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](#prerequisites)
[![Cost](https://img.shields.io/badge/Cost-Free%20Tier-success)](#)

A powerful, keyboard-triggered desktop assistant that captures your screen, extracts online judge problems via OCR, and produces complete, judge-ready solutions using a multi-agent system powered by **CrewAI** and **LangGraph**.

Runs completely free via a local LLM routing proxy (**FreeLLMAPI**) across providers like Groq, Google AI Studio, Cerebras, and Mistral—no OpenAI credits required.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Setup & Installation](#-setup--installation)
  - [1. Clone and Virtual Environment](#1-clone-and-virtual-environment)
  - [2. Configure FreeLLMAPI](#2-configure-freellmapi)
  - [3. Configure Environment Variables (.env)](#3-configure-environment-variables-env)
  - [4. Create Required Folders](#4-create-required-folders)
- [Running the Application](#-running-the-application)
- [Multi-Language Support](#-multi-language-support)
- [Core Components Breakdown](#-core-components-breakdown)
- [Configuration Reference](#-configuration-reference)
- [Dependencies](#-dependencies)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## 🔍 Overview

The **Coding Assistant AI** is designed for fast problem solving on competitive programming platforms and online judges (LeetCode, Codeforces, HackerRank, HackerEarth, and others). 

1. **Press `Z` anywhere** on your screen when viewing a problem.
2. The system captures the window, extracts the text using **Tesseract OCR**, and identifies the target programming language.
3. A **CrewAI** agent crafts a tailored, judge-compliant solution.
4. Explanations and clean, pasteable code files are automatically saved to disk, while full history is stored in a local SQLite database (`qa.db`).

---

## ✨ Key Features

- **⚡ Hotkey Driven Workflow**: Press `Z` globally from any window to solve. Press `Esc` anytime to exit safely.
- **👁️ Optical Character Recognition**: Integrated Tesseract OCR extracts problem descriptions directly from the active screen.
- **🤖 Multi-Agent Engine**: Modular CrewAI & LangGraph orchestration for reliable problem interpretation and feedback generation.
- **🌐 Automatic Language Detection**: Identifies 15+ programming languages from problem pages and editor tabs.
- **🎯 Judge-Ready Solutions**: Formats output precisely for platform specifications (e.g., LeetCode's `class Solution`, Codeforces standard I/O, Go's `package main`).
- **🛡️ Python AST Syntax Checking**: Automatically parses generated Python code with `ast.parse` to detect errors before pasting.
- **💸 100% Free LLM Support**: Designed around local provider proxies (e.g., FreeLLMAPI) aggregating free tiers of Groq, Google Gemini / AI Studio, Cerebras, and more.
- **💾 Local SQLite History**: Every capture, parsed problem, and solution is logged to `qa.db` for later review.
- **🔄 Infinite Recursion Protection**: LangGraph recursion limits configured to allow non-stop, continuous background listening.

---

## 🏗️ System Architecture

```text
┌─────────────────┐
│  User presses Z │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  LangGraph: wait_for_   │
│  next_trigger           │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  capture_and_identify   │ ◄── Direct tool call (no LLM)
│  - Screenshot via PIL   │
│  - OCR via Tesseract    │
│  - Detect language      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  check_question_found   │
└────┬──────────────┬─────┘
     │              │
     │ Found        │ Not found
     ▼              ▼
┌──────────┐   ┌──────────────────┐
│ answer_  │   │ handle_no_       │
│ question │   │ question         │
│ (CrewAI) │   └──────────────────┘
└────┬─────┘
     │
     ▼
┌─────────────────────────┐
│  store_result           │
│  - Save to SQLite       │
│  - Write answers/*.md   │
│  - Write latest_code.*  │
│  - Validate Python AST  │
└────────┬────────────────┘
         │
         ▼
    (loop back to wait)
```

---

## 📁 Project Structure

```text
leetcode_assistant/
│
├── answers/                     # Generated solutions & extracted code
│   ├── latest_answer.md         # Full explanation + solution breakdown
│   ├── latest_code.py           # Generated Python code (or .js, .cpp, .go, etc.)
│   └── ...                      
│
├── screenshots/                 # Timestamped screen captures
│
├── src/
│   ├── crew/
│   │   ├── agents.py            # CrewAI agent definitions
│   │   ├── crew.py              # Crew orchestration & execution pipeline
│   │   ├── tasks.py             # Multi-language task prompts
│   │   └── tools.py             # Screenshot & OCR extraction tools
│   ├── database.py              # SQLite storage & database helper functions
│   ├── graph.py                 # LangGraph state machine & workflow setup
│   ├── nodes.py                 # Graph nodes & language detection logic
│   └── state.py                 # TypedDict graph state definitions
│
├── .env                         # API keys & configuration options
├── .gitignore                   # Git ignore patterns
├── main.py                      # Application entry point & global hotkey handler
├── qa.db                        # SQLite history database
└── requirements.txt             # Python dependencies
```

---

## 📦 Prerequisites

Ensure you have the following prerequisites installed on your system:

- **Python 3.10+**: [python.org](https://www.python.org/)
- **Tesseract OCR Engine**:
  - **Windows**: Download and install from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Add the installation path (e.g., `C:\Program Files\Tesseract-OCR`) to your system `PATH`.
  - **Ubuntu / Debian**: `sudo apt update && sudo apt install -y tesseract-ocr`
  - **macOS**: `brew install tesseract`
- **FreeLLMAPI Router** (or any OpenAI-compatible proxy):
  - Download and install the desktop app from [FreeLLMAPI Releases](https://github.com/tashfeenahmed/freellmapi/releases).
  - Ensure the local server is running (defaults to `http://localhost:3001`).

---

## 🚀 Setup & Installation

### 1. Clone and Virtual Environment

```bash
# Clone repository
git clone https://github.com/yourusername/coding-assistant-ai.git
cd ss

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell / CMD):
venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure FreeLLMAPI

1. Launch the **FreeLLMAPI** desktop application.
2. Navigate to **Keys** and add at least one free-tier API key:
   - [Groq Console](https://console.groq.com) (Recommended: ~1,000 requests/day free tier)
   - [Google AI Studio](https://aistudio.google.com) (Generous free tier)
   - [Cerebras Cloud](https://cloud.cerebras.ai) (Ultra-fast inference)
3. Copy your **Unified API Key** from the top header of the FreeLLMAPI dashboard.
4. Under **Models**, configure your preferred model (such as `gpt-oss-120b` or Gemini models) as the primary model.

### 3. Configure Environment Variables (`.env`)

Create or update your `.env` file in the root directory:

```env
# FreeLLMAPI / OpenAI-compatible endpoint
OPENAI_API_BASE=http://localhost:3001/v1
OPENAI_API_KEY=freellmapi-your-unified-key-here
OPENAI_MODEL_NAME=gpt-oss-120b

# Telemetry and logging configuration
CREWAI_TELEMETRY_OPT_OUT=true
CREWAI_DISABLE_TELEMETRY=true
OTEL_SDK_DISABLED=true
CREWAI_DISABLE_RICH_LOGGING=true

# LangChain Tracing (disable unless debugging)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_ENDPOINT=
```

### 4. Create Required Folders

Ensure the output directories exist:

```bash
mkdir -p screenshots answers
```

---

## 💻 Running the Application

> [!IMPORTANT]
> **Windows Administrator Requirement**: On Windows, run your terminal as **Administrator**. The `keyboard` package requires administrative rights to listen to global OS-level hotkeys.

Start the assistant:

```bash
python main.py
```

### Hotkeys

| Key | Description |
| :---: | :--- |
| <kbd>Z</kbd> | Capture active screen, extract OCR problem, identify language, and generate solution. |
| <kbd>Esc</kbd> | Instantly shut down the assistant and exit the background loop. |

### Generated Outputs

- **Terminal**: Real-time progress, detected language, and full response.
- **`answers/latest_answer.md`**: Complete markdown explanation, time & space complexity, and code.
- **`answers/latest_code.<ext>`**: Pure code file ready to paste directly into the judge editor (e.g. `.py`, `.cpp`, `.js`).
- **`qa.db`**: Local SQLite record containing timestamps, OCR text, target language, and generated solutions.

---

## 🌐 Multi-Language Support

The OCR engine detects the language specified in the problem statement or editor tab and formats the answer for direct submission:

| Language | Keywords Detected | Output Structure |
| :--- | :--- | :--- |
| **Python** | `python`, `python3` | `class Solution: def ...` |
| **JavaScript** | `javascript`, `js` | `var func = function(...) { ... };` |
| **TypeScript** | `typescript`, `ts` | Type-annotated function signatures |
| **C++** | `c++`, `cpp` | `class Solution { public: ... };` |
| **Java** | `java` | `class Solution { public ... }` |
| **C#** | `c#`, `csharp` | `public class Solution { ... }` |
| **Go** | `go`, `golang` | `package main` + function signatures |
| **Rust** | `rust` | `impl Solution { pub fn ... }` |
| **Kotlin** | `kotlin` | `class Solution { fun ... }` |
| **Swift** | `swift` | `class Solution { func ... }` |
| **Ruby** | `ruby` | Pure method signature |
| **Others** | `php`, `scala`, `haskell`, `elixir`, `dart`, `r` | Platform-idiomatic conventions |

*Output file extensions automatically match the detected language (`.py`, `.js`, `.ts`, `.cpp`, `.java`, `.cs`, `.go`, `.rs`, `.kt`, `.swift`, `.rb`, etc.).*

---

## 🧩 Core Components Breakdown

### Agents (`src/crew/agents.py`)
- **Coding Expert**: Evaluates problem input, extracts constraints, chooses optimal algorithms (time/space complexity), and produces clean code.
- **Helpful Assistant**: Provides graceful feedback when OCR cannot detect a valid question on the screen.
- **Screen Capture Specialist**: Reserved for compatibility.

### Workflow & Nodes (`src/graph.py` & `src/nodes.py`)
- **`wait_for_next_trigger`**: Suspends execution until the hotkey trigger (<kbd>Z</kbd>) is fired.
- **`capture_and_identify`**: Takes a screenshot via PIL/ImageGrab, runs Tesseract OCR directly, and checks for target language identifiers.
- **`check_question_found`**: Conditional routing node directing to solution generation or fallback.
- **`answer_question`**: Invokes the CrewAI pipeline with multi-language task templates.
- **`store_result`**: Persists records into SQLite, writes solution files, and performs `ast.parse` checks on Python code.

---

## ⚙️ Configuration Reference

| Variable | Default / Example | Purpose |
| :--- | :--- | :--- |
| `OPENAI_API_BASE` | `http://localhost:3001/v1` | URL for the OpenAI-compatible router (FreeLLMAPI) |
| `OPENAI_API_KEY` | `freellmapi-...` | Unified API key |
| `OPENAI_MODEL_NAME` | `gpt-oss-120b` | Model identifier requested through the proxy |
| `CREWAI_TELEMETRY_OPT_OUT` | `true` | Disables telemetry reporting |
| `CREWAI_DISABLE_RICH_LOGGING`| `true` | Disables rich log overhead for clean console display |
| `LANGCHAIN_TRACING_V2` | `false` | Disables LangSmith tracing |

*Recursion limit is explicitly set in `main.py` to allow continuous long-running loops:*
```python
app.invoke({}, {"recursion_limit": 1000})
```

---

## 🛠️ Troubleshooting

| Problem | Potential Cause | Solution |
| :--- | :--- | :--- |
| **Pressing <kbd>Z</kbd> does nothing** | Terminal lacks Administrator rights | Run CMD / PowerShell as **Administrator**. |
| **All models exhausted** | FreeLLMAPI quota or rate limit hit | Wait 60 seconds, or add an extra provider key (e.g. Google AI Studio + Groq). |
| **`model_unavailable` error** | Model identifier name changed | Check `/v1/models` in FreeLLMAPI or switch model selection in FreeLLMAPI UI. |
| **`invalid JSON schema for tool`** | Groq / LLM rejects CrewAI tool schemas | Bypassed by default: OCR and screenshots run deterministically without LLM tool-calling. |
| **`SyntaxError` when pasting** | Broken type hints or hidden characters | Check `answers/latest_code.<ext>` and run without optional type annotations if needed. |
| **`GraphRecursionError`** | LangGraph hit step limit | Ensure `recursion_limit` is set in `app.invoke({}, {"recursion_limit": 1000})` in `main.py`. |

---

## 🔮 Future Enhancements

- [ ] Automatic clipboard copying on completion.
- [ ] Windows / macOS system tray toast notifications.
- [ ] Active window detection and automatic multi-monitor display selection.
- [ ] Screenshot cropping mode to isolate the problem statement panel.
- [ ] Integrated linters (`gofmt`, `node --check`, `rustc --parse-only`).
- [ ] Interactive UI for browsing local problem history from `qa.db`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

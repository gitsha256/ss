Coding Assistant AI — Multi-Agent Screen Solver with LangGraph & Free LLM Routing
Status: Active. Works on LeetCode, Codeforces, HackerRank, HackerEarth, and most online judges.
Cost: Free. No OpenAI credits required.

Table of Contents
Introduction

Project Features

System Architecture

File Structure

Setup Instructions

Running the Application

Key Components

Multi-Language Support

Configuration

Dependencies

Troubleshooting

Future Enhancements

License

1. Introduction
The Coding Assistant AI is a desktop assistant that captures your screen, extracts the coding problem visible on it via OCR, and produces a complete solution using a multi-agent system powered by CrewAI and LangGraph.

It runs entirely on free LLM infrastructure through a local FreeLLMAPI router that aggregates free-tier providers (Groq, Google AI Studio, Cerebras, Mistral, OpenRouter, and more). No OpenAI credits are required.

The assistant detects the programming language from the problem page, generates judge-ready code in that language, validates it when possible, and saves both the explanation and the pasteable solution to disk. All Q&A pairs are stored in a local SQLite database for history.

2. Project Features
Z Hotkey Capture — Press Z anywhere to capture and solve.

Esc to Quit — Press Esc at any time to shut down instantly.

Multi-Agent System — Dedicated CrewAI agents for solving and feedback.

OCR Extraction — Tesseract OCR reads the problem text directly from your screen.

Automatic Language Detection — Detects 15+ languages (Python, JavaScript, TypeScript, Go, Rust, Java, C++, C#, Kotlin, Swift, Ruby, PHP, Scala, Haskell, Elixir, Dart, R).

Judge-Ready Output — Solutions are formatted for the target judge (LeetCode's class Solution, Codeforces' stdin/stdout, Go's package main, etc.).

Python Syntax Validation — ast.parse catches broken generated code before you paste it.

Clean Console Output — No CLI panels, no telemetry spam.

SQLite History — Every solved problem is logged to qa.db.

Free LLM Router — Pluggable via FreeLLMAPI, no paid API keys needed.

Recursion-Safe Workflow — Runs indefinitely without hitting LangGraph's default recursion limit.

3. System Architecture
text
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
     │ found        │ not found
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
│  - Validate Python      │
└────────┬────────────────┘
         │
         ▼
    (loop back to wait)
4. File Structure
text
/leetcode_assistant/
│
├── answers/                     # Generated solutions
│   ├── latest_answer.md         # Full explanation + code
│   ├── latest_code.py           # Python submission
│   ├── latest_code.js           # JavaScript submission
│   ├── latest_code.go           # Go submission
│   └── ...                      # Extension matches detected language
│
├── screenshots/                 # Timestamped screenshots
│
├── src/
│   ├── crew/
│   │   ├── agents.py            # CrewAI agents
│   │   ├── crew.py              # Crew orchestration
│   │   ├── tasks.py             # Task definitions (multi-language prompts)
│   │   └── tools.py             # CaptureAndExtractTool
│   ├── database.py              # SQLite storage
│   ├── graph.py                 # LangGraph workflow
│   ├── nodes.py                 # Workflow nodes + language detection
│   └── state.py                 # TypedDict state
│
├── main.py                      # Entry point
├── .env                         # Router URL + model name
├── qa.db                        # SQLite history
└── requirements.txt
5. Setup Instructions
Prerequisites
Python 3.10+

Tesseract OCR installed and on your PATH

Windows: UB-Mannheim installer

Linux: sudo apt install tesseract-ocr

macOS: brew install tesseract

FreeLLMAPI — unified local router for free LLM providers

Download from the FreeLLMAPI releases page

Install and launch the desktop app (runs on http://localhost:3001)

Installation
bash
git clone https://github.com/yourusername/coding-assistant-ai.git
cd coding-assistant-ai
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
Configure FreeLLMAPI
Launch the FreeLLMAPI desktop app.

Go to the Keys page and add at least one provider key:

Groq — https://console.groq.com (free tier: 1,000 req/day)

Google AI Studio — https://aistudio.google.com (generous free tier)

Cerebras — https://cloud.cerebras.ai (fast free tier)

Copy the Unified API Key from the dashboard header.

In the Models page, ensure gpt-oss-120b (Groq) or another tool-capable model is at the top of the fallback chain.

Configure .env
env
OPENAI_API_BASE=http://localhost:3001/v1
OPENAI_API_KEY=freellmapi-your-unified-key-here
OPENAI_MODEL_NAME=gpt-oss-120b

CREWAI_TELEMETRY_OPT_OUT=true
CREWAI_DISABLE_TELEMETRY=true
OTEL_SDK_DISABLED=true
CREWAI_DISABLE_RICH_LOGGING=true

LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_ENDPOINT=
Create Required Directories
bash
mkdir screenshots
mkdir answers
6. Running the Application
bash
python main.py
Important: On Windows, run your terminal as Administrator — the keyboard library needs elevated privileges for global hotkeys.

Key	Action
Z	Capture the screen and solve the visible problem
Esc	Shut down the assistant instantly
Output:

Full explanation and code appear in the terminal

answers/latest_answer.md — full markdown answer

answers/latest_code.<ext> — pasteable solution in the detected language

qa.db — SQLite history

7. Key Components
Agents
Screen Capture Specialist — Defined for compatibility. Not actively used since capture runs directly.

Coding Expert — Receives the problem and language, generates a judge-ready solution.

Helpful Assistant — Handles the "no question found" case.

Tasks
capture_and_identify_task — Instructs the agent to return raw OCR text.

answer_question_task — Language-aware prompt that adapts to Python, JavaScript, Go, Rust, etc.

handle_no_question_task — Fallback message.

Tools
CaptureAndExtractTool — Takes a screenshot, runs Tesseract OCR, returns the extracted text. Called directly from nodes.py rather than through the LLM, avoiding tool-schema serialization issues.

LangGraph Workflow
Node	Purpose
wait_for_next_trigger	Blocks on Z
capture_and_identify	Screenshot + OCR + language detection
check_question_found	Pass-through to conditional router
answer_question	Calls the CrewAI answer agent
handle_no_question	Friendly retry message
store_result	Saves to SQLite + disk
Database
SQLite (qa.db) stores every Q&A pair. Managed via database.py with init_db() and save_qa_pair().

8. Multi-Language Support
The assistant detects the language from the OCR text (looking at the language tab near the top of the page) and generates solutions in that language's judge-specific format.

Language	Detection Keyword	Submission Format
Python	python, python3	class Solution: def method(self, ...)
JavaScript	javascript, js	var method = function(...) {...};
TypeScript	typescript, ts	Typed function signature
Go	go, golang	package main + func signature
Rust	rust	impl Solution { pub fn ... }
Java	java	class Solution { public ... }
C++	c++, cpp	class Solution { public: ... };
C#	c#, csharp	public class Solution { ... }
Kotlin	kotlin	class Solution { fun ... }
Swift	swift	class Solution { func ... }
Ruby	ruby	Method signature only
PHP, Scala, Haskell, Elixir, Dart, R	all supported	Site-appropriate format
Output files use the correct extension: .py, .js, .ts, .go, .rs, .java, .cpp, .cs, .kt, .swift, .rb, etc.

9. Configuration
All runtime configuration lives in .env:

Variable	Purpose
OPENAI_API_BASE	FreeLLMAPI router URL
OPENAI_API_KEY	FreeLLMAPI unified key
OPENAI_MODEL_NAME	Preferred model (or auto)
CREWAI_*	Telemetry opt-out
LANGCHAIN_TRACING_V2	Set to false to disable LangSmith
Recursion limit — Set in main.py:

python
app.invoke({}, {"recursion_limit": 1000})
10. Dependencies
CrewAI — Multi-agent orchestration

LangGraph — Workflow state machine

Pillow + ImageGrab — Screenshot capture

pytesseract — OCR binding

Tesseract OCR — OCR engine (system install)

keyboard — Global hotkeys

python-dotenv — .env loading

SQLite3 — Built into Python

11. Troubleshooting
Symptom	Cause	Fix
image "z" does nothing	Not running as admin	Run terminal as Administrator
All models exhausted	FreeLLMAPI rate limit	Wait ~1 min, or add a second provider key
model_unavailable	Model ID changed	Use auto, or check /v1/models
invalid JSON schema for tool	Groq rejects CrewAI tool schemas	Already fixed — capture runs directly, bypassing tool calling
SyntaxError when pasting	Type hints with invisible characters	Run code without type hints; use untyped signatures
GraphRecursionError	Default 25-step limit	Set recursion_limit: 1000 in main.py
Broken code from LLM	Weak model output	Press Z again to retry, or switch models
12. Future Enhancements
Auto-copy code to clipboard on generation

System tray notifications when the solution is ready

Language-specific linters (gofmt, node --check, rustc --parse-only)

Codeforces stdin/stdout mode — distinguish from LeetCode's class-based format

Screenshot cropping — focus OCR on the problem panel only

RAG knowledge base — local embeddings via sentence-transformers

Problem history browser — search qa.db for previously solved problems

Multi-monitor support — capture the display with the active window

13. License
MIT License — see LICENSE for details.

Happy solving. Press Z. Get code. Paste. Done.

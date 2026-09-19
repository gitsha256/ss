import os
import re
import keyboard
from crewai import Crew
from .crew.crew import CodingAssistantCrew
from .database import init_db, save_qa_pair


STOP_KEY = "esc"


# Language detection table — order matters (specific before general)
LANGUAGE_PATTERNS = [
    (r"\btypescript\b|\bts\b", "TypeScript"),
    (r"\bjavascript\b|\bjs\b", "JavaScript"),
    (r"\bpython3?\b|\bpy\b", "Python"),
    (r"\bc\+\+\b|\bcpp\b", "C++"),
    (r"\bgolang\b|\bgo\b(?=\s|$)", "Go"),
    (r"\brust\b|\brs\b", "Rust"),
    (r"\bswift\b", "Swift"),
    (r"\bkotlin\b", "Kotlin"),
    (r"\bc#\b|\bcsharp\b|\bcs\b", "C#"),
    (r"\bjava\b(?!script)", "Java"),
    (r"\bruby\b|\brb\b", "Ruby"),
    (r"\bphp\b", "PHP"),
    (r"\bscala\b", "Scala"),
    (r"\bhaskell\b", "Haskell"),
    (r"\belixir\b|\bex\b", "Elixir"),
    (r"\bdart\b", "Dart"),
    (r"\br\b(?=\s|$)", "R"),
]

# File extensions per language
LANG_EXT = {
    "Python": ".py",
    "JavaScript": ".js",
    "TypeScript": ".ts",
    "Go": ".go",
    "Rust": ".rs",
    "Java": ".java",
    "C++": ".cpp",
    "C#": ".cs",
    "Ruby": ".rb",
    "PHP": ".php",
    "Swift": ".swift",
    "Kotlin": ".kt",
    "Scala": ".scala",
    "Haskell": ".hs",
    "Elixir": ".ex",
    "Dart": ".dart",
    "R": ".r",
}

# Fence languages that map back to our canonical names
FENCE_ALIASES = {
    "python": "Python",
    "py": "Python",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "go": "Go",
    "golang": "Go",
    "rust": "Rust",
    "rs": "Rust",
    "java": "Java",
    "cpp": "C++",
    "c++": "C++",
    "csharp": "C#",
    "cs": "C#",
    "c#": "C#",
    "ruby": "Ruby",
    "rb": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "scala": "Scala",
    "haskell": "Haskell",
    "elixir": "Elixir",
    "dart": "Dart",
    "r": "R",
}


class Nodes:
    def __init__(self):
        self.crew = CodingAssistantCrew()
        init_db()

    def log_event(self, event):
        pass

    def wait_for_next_trigger(self, state):
        print(f"\n## Ready. Press z to capture, or {STOP_KEY.upper()} to quit.")
        keyboard.wait('z')
        print("## z pressed — capturing screen")
        return {}

    def _detect_language(self, text: str) -> str:
        """Scan OCR text for a language name. Returns 'Python' if none found."""
        text_lower = text.lower()
        for pattern, lang in LANGUAGE_PATTERNS:
            if re.search(pattern, text_lower):
                return lang
        return "Python"   # default

    def capture_and_identify(self, state):
        from .crew.tools import CaptureAndExtractTool

        tool = CaptureAndExtractTool()
        text = tool._run().strip()

        if not text or "NO_QUESTION_FOUND" in text.upper():
            self.log_event("No question found in the screenshot.")
            return {"question": None, "language": None}

        language = self._detect_language(text)
        print(f"## Detected language: {language}")
        return {"question": text, "language": language}

    def check_question_found(self, state):
        return {}

    def question_found(self, state):
        return "found" if state.get("question") else "not_found"

    def handle_no_question(self, state):
        print("\n⚠️  No coding question detected. Press z to retry, or ESC to quit.\n")
        return {"answer": None, "question": None, "language": None}

    def answer_question(self, state):
        question = state.get("question")
        language = state.get("language") or "Python"
        if not question:
            return {"answer": None}

        print(f"## Generating {language} solution ... (press ESC to abort)")
        task = self.crew.tasks.answer_question_task(
            self.crew.answer_agent, question, language
        )
        crew = Crew(
            agents=[self.crew.answer_agent],
            tasks=[task],
            verbose=False,
            memory=False,
            planning=False,
        )
        result = crew.kickoff()
        if isinstance(result, dict):
            result = result.get("result", result)
        answer = (getattr(result, "raw", None) or str(result)).strip()
        return {"answer": answer}

    def _clean_code(self, code: str) -> str:
        code = code.replace('\xa0', ' ')
        code = code.replace('\u200b', '')
        code = code.replace('\u202f', ' ')
        code = code.replace('\u2009', ' ')
        code = code.replace('\t', '    ')
        code = code.replace('\r\n', '\n')
        code = code.replace('\r', '\n')
        code = "\n".join(line.rstrip() for line in code.splitlines())
        return code.strip()

    def _is_valid_python(self, code: str) -> bool:
        import ast
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            print(f"⚠️  Python code failed validation on line {e.lineno}: {e.msg}")
            return False

    def _extract_code_block(self, answer: str, language: str):
        """
        Find fenced code blocks, prefer ones tagged with `language`,
        then any fenced block. Returns cleaned code or None.
        """
        # 1. Try language-tagged blocks first
        lang_key = language.lower()
        tagged = re.findall(
            rf"```{lang_key}\n(.*?)```", answer, re.DOTALL | re.IGNORECASE
        )
        if tagged:
            return self._clean_code(tagged[-1])

        # 2. Try any fenced block
        any_block = re.findall(r"```(?:\w+\+?)?\n(.*?)```", answer, re.DOTALL)
        if any_block:
            return self._clean_code(any_block[-1])

        return None

    def store_result(self, state):
        question = state.get("question")
        answer = state.get("answer")
        language = state.get("language") or "Python"

        if not question or not answer:
            return {}

        save_qa_pair(question, answer)

        os.makedirs("answers", exist_ok=True)
        with open("answers/latest_answer.md", "w", encoding="utf-8") as f:
            f.write(f"# Question\n\n{question}\n\n# Solution ({language})\n\n{answer}\n")

        cleaned = self._extract_code_block(answer, language)

        # Python gets validation; other languages are trusted as-is
        if cleaned and language == "Python":
            if not self._is_valid_python(cleaned):
                cleaned = None

        ext = LANG_EXT.get(language, ".txt")

        if cleaned:
            code_path = f"answers/latest_code{ext}"
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            code_status = f"💻 Pasteable code: {code_path}"
        else:
            code_status = "⚠️  No valid code block found — check answers/latest_answer.md"

        bar = "=" * 72
        print(f"\n{bar}\nQUESTION\n{bar}")
        print(question.strip()[:500])

        print(f"\n{bar}\nSOLUTION ({language})\n{bar}")
        print(answer.strip())

        print(f"\n{bar}")
        print("📄 answers/latest_answer.md   (full answer)")
        print(code_status)
        print(f"{bar}\n")

        return {}
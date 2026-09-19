from crewai import Task
from textwrap import dedent


class CodingAssistantTasks:

    def capture_and_identify_task(self, agent):
        return Task(
            description=(
                "Use the capture_and_extract tool to take a screenshot and extract "
                "the coding question text. Return ONLY the raw extracted problem text. "
                "Do NOT solve the problem. Do NOT add markdown formatting. "
                "If no question is visible, return exactly: NO_QUESTION_FOUND"
            ),
            expected_output=(
                "The raw problem statement as plain text, "
                "or exactly 'NO_QUESTION_FOUND' if nothing was found."
            ),
            agent=agent,
        )

    def handle_no_question_task(self, agent):
        return Task(
            description="Inform the user that no coding question was detected.",
            expected_output="A short friendly message suggesting the user retry.",
            agent=agent,
        )

    def answer_question_task(self, agent, question, language="Python"):
        lang_specific = {
            "Python": (
                "Wrap the solution in `class Solution` with the correct method name. "
                "Do NOT include type hints. No imports, no print statements."
            ),
            "JavaScript": (
                "Use LeetCode's expected form: `var functionName = function(...) { ... };`. "
                "Do NOT wrap in a class. Use `Map` for hash maps. No console.log."
            ),
            "TypeScript": (
                "Use LeetCode's expected form with type annotations as shown on the page. "
                "No console.log, no example usage."
            ),
            "Go": (
                "Use `package main` and the exact function signature LeetCode or the "
                "judge expects. Include necessary imports. No `main()` unless required."
            ),
            "Rust": (
                "Use the exact `impl Solution { pub fn ... }` block that LeetCode expects. "
                "No `fn main()`."
            ),
            "Java": (
                "Use `class Solution { public returnType methodName(...) { ... } }`. "
                "No `main` method, no imports beyond the standard library."
            ),
            "C++": (
                "Use `class Solution { public: returnType methodName(...) { ... } };`. "
                "Include standard headers only if LeetCode does."
            ),
            "C#": (
                "Use `public class Solution { public returnType MethodName(...) { ... } }`."
            ),
            "Ruby": (
                "Use the exact method signature LeetCode expects. No `puts` or `print`."
            ),
            "Kotlin": (
                "Use `class Solution { fun methodName(...): ReturnType { ... } }`."
            ),
            "Swift": (
                "Use `class Solution { func methodName(...) -> ReturnType { ... } }`."
            ),
        }.get(language, "Follow the exact submission format that the target judge expects.")

        return Task(
            description=dedent(f"""\
                Provide a complete, detailed solution to the following coding problem.

                Problem:
                {question}

                Target language: {language}

                Output format (follow exactly):
                1. A brief explanation of the approach.
                2. The solution in {language}, in the format the judge expects:
                   {lang_specific}
                   - No example usage, no top-level test calls, no __main__ block.
                3. Time and space complexity analysis.

                IMPORTANT: Put the code inside a single fenced block tagged with
                the correct language: ```{language.lower()}
                """),
            expected_output=(
                f"A complete answer with: (a) an explanation, (b) {language} code "
                f"in judge-ready submission format, and (c) complexity analysis."
            ),
            agent=agent,
        )
from crewai import Agent
from .tools import CaptureAndExtractTool


class CodingAssistantAgents:

    def __init__(self):
        self.capture_tool = CaptureAndExtractTool()

    def screen_capture_agent(self):
        return Agent(
            role="Screen Capture Specialist",
            goal="Capture the screen and extract the coding question text from it.",
            backstory=(
                "You specialize in capturing screenshots and using OCR to extract "
                "the text of coding problems visible on screen."
            ),
            tools=[self.capture_tool],
            verbose=False,
            allow_delegation=False,
            max_iter=3,
            max_retry_limit=2,
        )

    def question_not_found_agent(self):
        return Agent(
            role="Helpful Assistant",
            goal="Politely inform the user when no coding question was found.",
            backstory=(
                "You help users understand that their screenshot did not contain "
                "a detectable coding question and suggest how to retry."
            ),
            tools=[],
            verbose=False,
            allow_delegation=False,
        )
    def answer_agent(self):
        return Agent(
            role="Coding Expert",
            goal="Provide correct, judge-ready solutions in any programming language.",
            backstory=(
            "You are an experienced software engineer fluent in Python, "
            "JavaScript, TypeScript, Go, Rust, Java, C++, C#, Kotlin, Swift, "
            "Ruby, and more. You know each judge's exact submission format."
            ),
            tools=[],
            verbose=False,
            allow_delegation=False,
            max_iter=3,
        )
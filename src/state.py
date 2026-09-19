from typing import TypedDict, Optional


class CodingAssistantState(TypedDict, total=False):
    question: Optional[str]
    answer: Optional[str]
    language: Optional[str]
import re
import time
import os
import pytesseract
from PIL import Image, ImageGrab
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class CaptureAndExtractInput(BaseModel):
    """Empty input schema so Groq accepts the tool definition."""
    pass


class CaptureAndExtractTool(BaseTool):
    name: str = "capture_and_extract"
    description: str = (
        "Captures the current screen, extracts all visible text using OCR, "
        "and returns the extracted text. Takes no arguments."
    )
    args_schema: type[BaseModel] = CaptureAndExtractInput

    def _run(self) -> str:
        os.makedirs("screenshots", exist_ok=True)
        timestamp = int(time.time())
        filepath = os.path.abspath(f"screenshots/screenshot_{timestamp}.png")
        ImageGrab.grab().save(filepath)

        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)

        pattern = r"(?s)(?:(?:Problem|Question|Q\d*):\s*)(.*?)(?:\n\n|$)"
        matches = re.findall(pattern, text)
        if matches:
            return matches[0].strip()

        return text.strip() if text.strip() else "NO_QUESTION_FOUND"
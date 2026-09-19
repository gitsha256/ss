import os
import keyboard

os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_RICH_LOGGING"] = "true"

from dotenv import load_dotenv
load_dotenv()

import logging
logging.getLogger("crewai").setLevel(logging.CRITICAL)
logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.WARNING)

STOP_KEY = "esc"


def install_stop_listener():
    def on_stop():
        print("\n\n⛔ Stop key pressed — shutting down.\n")
        os._exit(0)
    keyboard.add_hotkey(STOP_KEY, on_stop)


if __name__ == "__main__":
    install_stop_listener()

    from src.graph import Workflow

    print(f"Press z to capture a problem, or {STOP_KEY.upper()} to quit at any time.")
    app = Workflow().app
    app.invoke({}, {"recursion_limit": 1000})
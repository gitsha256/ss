from crewai import Crew
from .agents import CodingAssistantAgents
from .tasks import CodingAssistantTasks

class CodingAssistantCrew:
    def __init__(self):
        agents = CodingAssistantAgents()
        self.capture_agent = agents.screen_capture_agent()
        self.no_question_agent = agents.question_not_found_agent()
        self.answer_agent = agents.answer_agent()
        self.tasks = CodingAssistantTasks()

    def kickoff(self, state=None):
        return None

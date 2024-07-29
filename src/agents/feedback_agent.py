# feedback_agent.py

from src.debate.debate_data import DebateData
from src.llm.llm_client import LLMClient
from typing import Dict, Any

class FeedbackAgent:
    def __init__(self, llm_client: LLMClient, prompt_template: Dict[str, str]):
        self.llm_client = llm_client
        self.prompt_template = prompt_template

    def generate_feedback(self, debate_data: DebateData, summary: Dict[str, Any]) -> str:
        prompt = self.prompt_template["system_prompt_temp"]
        prompt += f"トピック: {debate_data.topic}\n\n"
        prompt += f"評価要約:\n{summary['summary']}\n\n"
        feedback = self.llm_client.generate_text(prompt)
        return feedback

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.llm_client.model
        }

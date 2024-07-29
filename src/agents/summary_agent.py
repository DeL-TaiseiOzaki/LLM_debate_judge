from typing import List, Dict, Any
from src.llm.llm_client import LLMClient

class SummaryAgent:
    def __init__(self, llm_client: LLMClient, prompt_template: Dict[str, str]):
        self.llm_client = llm_client
        self.prompt_template = prompt_template

    def summarize(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = self.prompt_template["system_prompt_temp"]
        for result in evaluation_results:
            prompt += f"側面: {result['aspect']}\n"
            prompt += f"フィードバック: {result['feedback']}\n\n"
        summary = self.llm_client.generate_text(prompt)
        return {"summary": summary}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.llm_client.model
        }
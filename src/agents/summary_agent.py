from typing import List, Dict, Any
from src.llm.llm_client import LLMClient

class SummaryAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def summarize(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = "以下の評価結果を要約し、主要なポイントと改善提案をまとめてください:\n\n"
        for result in evaluation_results:
            prompt += f"側面: {result['aspect']}\n"
            prompt += f"フィードバック: {result['feedback']}\n\n"
        summary = self.llm_client.generate_text(prompt)
        return {"summary": summary}
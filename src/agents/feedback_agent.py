from src.debate.debate_data import DebateData
from src.llm.llm_client import LLMClient

class FeedbackAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate_feedback(self, debate_data: DebateData, summary: Dict[str, Any]) -> str:
        prompt = f"以下のディベートの要約と評価結果に基づいて、総合的なフィードバックを生成してください。具体的な改善点と、ディベートスキル向上のためのアドバイスを含めてください。\n\n"
        prompt += f"トピック: {debate_data.topic}\n\n"
        prompt += f"評価要約:\n{summary['summary']}\n\n"
        feedback = self.llm_client.generate_text(prompt)
        return feedback
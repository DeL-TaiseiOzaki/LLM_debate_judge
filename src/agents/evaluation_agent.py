from typing import List, Dict, Any
from src.debate.debate_data import DebateData
from src.debate.evaluation_criteria import EvaluationCriteria
from src.llm.llm_client import LLMClient

class EvaluationAgent:
    def __init__(self, llm_client: LLMClient, prompt_template: str):
        self.llm_client = llm_client
        self.prompt_template = prompt_template

    def evaluate(self, debate_data: DebateData, criteria: EvaluationCriteria) -> List[Dict[str, Any]]:
        results = []
        for aspect in criteria.feedback_criteria:
            context = self._prepare_context(debate_data, aspect["target_documents"])
            prompt = self.prompt_template.format(
                aspect=aspect["aspect"],
                description=aspect["description"],
                evaluation_points=self._format_evaluation_points(aspect["evaluation_points"]),
                context=context
            )
            feedback = self.llm_client.generate_text(prompt)
            results.append({
                "aspect": aspect["aspect"],
                "feedback": feedback
            })
        return results

    def _prepare_context(self, debate_data: DebateData, target_documents: List[str]) -> str:
        context = ""
        for doc in target_documents:
            if doc == "affirmative_argument":
                context += f"肯定的議論:\n{debate_data.affirmative_argument}\n\n"
            elif doc == "counter_argument":
                context += f"反論:\n{debate_data.counter_argument}\n\n"
            elif doc == "reconstruction":
                context += f"再構築:\n{debate_data.reconstruction}\n\n"
        return context

    def _format_evaluation_points(self, evaluation_points: List[Dict[str, Any]]) -> str:
        formatted = ""
        for point in evaluation_points:
            formatted += f"- {point['focus']}\n"
            for question in point["guiding_questions"]:
                formatted += f"  質問: {question}\n"
            formatted += "  改善提案:\n"
            for suggestion in point["improvement_suggestions"]:
                formatted += f"    - {suggestion}\n"
        return formatted
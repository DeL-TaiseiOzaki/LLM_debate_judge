from typing import Dict, Any
from src.debate.debate_data import DebateData
from src.llm.llm_client import LLMClient
from src.debate.evaluation_criteria import AspectCriteria

class EvaluationAgent:
    def __init__(self, llm_client: LLMClient, prompt_template: Dict[str, str], aspect: AspectCriteria):
        self.llm_client = llm_client
        self.prompt_template = prompt_template
        self.aspect = aspect

    def evaluate(self, debate_data: DebateData) -> Dict[str, Any]:
        system_prompt = self._prepare_system_prompt(debate_data)
        focus_evaluations = []

        for evaluation_point in self.aspect.evaluation_points:
            user_prompt = self._prepare_user_prompt(evaluation_point)
            feedback = self.llm_client.generate_text(system_prompt, user_prompt)
            focus_evaluations.append({
                "focus": evaluation_point.focus,
                "feedback": feedback
            })

        return {
            "aspect": self.aspect.aspect,
            "focus_evaluations": focus_evaluations
        }

    def _prepare_system_prompt(self, debate_data: DebateData) -> str:
        return self.prompt_template["system_prompt_temp"].replace(
            "###topic###", debate_data.topic
        ).replace(
            "###affirmative_argument###", debate_data.affirmative_argument
        ).replace(
            "###counter_argument###", debate_data.counter_argument
        ).replace(
            "###reconstruction###", debate_data.reconstruction
        ).replace(
            "###aspect###", self.aspect.aspect
        ).replace(
            "###description###", self.aspect.description
        ).replace(
            "###target_documents###", ", ".join(self.aspect.target_documents)
        )

    def _prepare_user_prompt(self, evaluation_point: Any) -> str:
        return self.prompt_template["user_prompt_temp"].replace(
            "###focus###", evaluation_point.focus
        ).replace(
            "###sub_evaluation_points###", "\n".join(evaluation_point.sub_evaluation_points)
        ).replace(
            "###sub_target_document###", ", ".join(evaluation_point.sub_target_document)
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.llm_client.model,
            "aspect": self.aspect.aspect
        }

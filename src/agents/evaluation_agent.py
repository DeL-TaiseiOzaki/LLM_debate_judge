from typing import List, Dict, Any
from src.llm.llm_client import LLMClient
from src.debate.debate_data import DebateData
from src.debate.evaluation_criteria import AspectCriteria, EvaluationPoint
from src.utils.logger import logger

class EvaluationAgent:
    def __init__(self, llm_client: LLMClient, prompt_template: Dict[str, str], aspect: AspectCriteria):
        self.llm_client = llm_client
        self.prompt_template = prompt_template
        self.aspect = aspect

    def evaluate(self, debate_data: DebateData) -> List[Dict[str, Any]]:
        logger.info(f"Starting evaluation for aspect: {self.aspect.aspect}")
        system_prompt = self.get_system_prompt(debate_data)
        evaluation_results = []

        for i, evaluation_point in enumerate(self.aspect.evaluation_points, 1):
            user_prompt = self.get_user_prompt(evaluation_point)
            logger.info(f"Evaluating focus: {evaluation_point.focus}")
            result = self.llm_client.generate_text(system_prompt, user_prompt)
            evaluation_results.append({
                "focus": evaluation_point.focus,
                "result": result,
                "prompt": user_prompt,
                "prompt_id": f"user_prompt_{i}"
            })

        logger.info(f"Finished evaluation for aspect: {self.aspect.aspect}")
        return evaluation_results

    def get_system_prompt(self, debate_data: DebateData) -> str:
        logger.info("Preparing system prompt for evaluation")
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

    def get_user_prompt(self, evaluation_point: EvaluationPoint) -> str:
        logger.info(f"Preparing user prompt for focus: {evaluation_point.focus}")
        return self.prompt_template["user_prompt_temp"].replace(
            "###focus###", evaluation_point.focus
        ).replace(
            "###sub_evaluation_points###", "\n".join(f"・{point}" for point in evaluation_point.sub_evaluation_points)
        ).replace(
            "###sub_target_document###", ", ".join(evaluation_point.sub_target_document)
        )
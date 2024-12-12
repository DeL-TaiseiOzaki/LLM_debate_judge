from typing import List, Dict, Any
from src.llm.llm_client import LLMClient
from src.debate.debate_data import DebateData
from src.debate.evaluation_criteria import AspectCriteria
from src.utils.logger import logger

class SummaryAgent:
    def __init__(self, llm_client: LLMClient, prompt_template: Dict[str, str]):
        self.llm_client = llm_client
        self.prompt_template = prompt_template

    def summarize(self, debate_data: DebateData, evaluation_results: List[Dict[str, Any]], evaluation_criteria: List[AspectCriteria]) -> str:
        logger.info("Starting summary generation")
        system_prompt = self.get_system_prompt(debate_data)
        user_prompt = self.get_user_prompt(evaluation_results, evaluation_criteria)
        
        logger.info("Calling API for summary generation")
        summary = self.llm_client.generate_text(system_prompt, user_prompt)
        logger.info("Finished summary generation")
        
        return summary

    def get_system_prompt(self, debate_data: DebateData) -> str:
        logger.info("Preparing system prompt for summary")
        return self.prompt_template["system_prompt_temp"].replace(
            "###topic###", debate_data.topic
        ).replace(
            "###affirmative_argument###", debate_data.affirmative_argument
        ).replace(
            "###counter_argument###", debate_data.counter_argument
        ).replace(
            "###reconstruction###", debate_data.reconstruction
        )

    def get_user_prompt(self, evaluation_results: List[Dict[str, Any]], evaluation_criteria: List[AspectCriteria]) -> str:
        logger.info("Preparing user prompt for summary")
        formatted_results = []
        for result in evaluation_results:
            aspect = result['aspect']
            weight = next((criterion.weight for criterion in evaluation_criteria if criterion.aspect == aspect), 1.0)
            formatted_results.append(f"Aspect: {aspect}")
            formatted_results.append(f"Weight: {weight}")
            formatted_results.append(f"Evaluation: {result['result']}")
            formatted_results.append("")  # Add an empty line for readability
        
        return self.prompt_template["user_prompt_temp"].replace(
            "###evaluation_from_agents###", "\n".join(formatted_results)
        )
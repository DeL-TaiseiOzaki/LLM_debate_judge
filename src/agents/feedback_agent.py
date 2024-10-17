from src.debate.debate_data import DebateData
from src.llm.llm_client import LLMClient
from src.utils.logger import logger

class FeedbackAgent:
    def __init__(self, llm_client: LLMClient, prompt_template: dict[str, str]):
        self.llm_client = llm_client
        self.prompt_template = prompt_template

    def generate_feedback(self, debate_data: DebateData, summary: str, topic_intention: str) -> str:
        logger.info("Starting feedback generation")
        system_prompt = self.get_system_prompt(debate_data)
        user_prompt = self.get_user_prompt(summary, topic_intention)
        
        logger.info("Calling API for feedback generation")
        feedback = self.llm_client.generate_text(system_prompt, user_prompt)
        logger.info("Finished feedback generation")
        
        return feedback

    def get_system_prompt(self, debate_data: DebateData) -> str:
        logger.info("Preparing system prompt for feedback")
        return self.prompt_template["system_prompt_temp"].replace(
            "###topic###", debate_data.topic
        ).replace(
            "###affirmative_argument###", debate_data.affirmative_argument
        ).replace(
            "###counter_argument###", debate_data.counter_argument
        ).replace(
            "###reconstruction###", debate_data.reconstruction
        )

    def get_user_prompt(self, summary: str, topic_intention: str) -> str:
        logger.info("Preparing user prompt for feedback")
        return self.prompt_template["user_prompt_temp"].replace(
            "###final_evaluation###", summary
        ).replace(
            "###topic_intention###", topic_intention
        )
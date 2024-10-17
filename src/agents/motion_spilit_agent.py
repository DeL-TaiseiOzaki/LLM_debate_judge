from src.llm.llm_client import LLMClient
from src.debate.debate_data import DebateData
from src.utils.logger import logger

class MotionspilitAgent:
    def __init__(self, llm_client: LLMClient, prompt_template: dict[str, str]):
        self.llm_client = llm_client
        self.prompt_template = prompt_template

    def generate_intention(self, debate_data: DebateData) -> str:
        logger.info("Starting topic intention generation")
        system_prompt = self.get_system_prompt()
        user_prompt = self.get_user_prompt(debate_data.topic)
        
        logger.info("Calling API for topic intention generation")
        intention = self.llm_client.generate_text(system_prompt, user_prompt)
        logger.info("Finished topic intention generation")
        
        return intention

    def get_system_prompt(self) -> str:
        logger.info("Preparing system prompt for topic intention")
        return self.prompt_template["system_prompt_temp"]

    def get_user_prompt(self, topic: str) -> str:
        logger.info("Preparing user prompt for topic intention")
        return self.prompt_template["user_prompt_temp"].replace(
            "###topic###", topic
        )
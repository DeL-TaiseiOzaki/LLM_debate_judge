from abc import ABC, abstractmethod
import openai
from src.utils.logger import logger

class LLMClient(ABC):
    @abstractmethod
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        pass
        
    def generate_text(self, prompt: str) -> str:
        logger.info(f"Calling API with model: {self.model}")
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        logger.info(f"Received response from API")
        return response.choices[0].message.content
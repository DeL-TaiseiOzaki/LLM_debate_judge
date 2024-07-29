from abc import ABC, abstractmethod
from typing import Dict, Any
from src.debate.debate_data import DebateData

class BaseAgent(ABC):
    @abstractmethod
    def process(self, debate_data: DebateData) -> Dict[str, Any]:
        pass
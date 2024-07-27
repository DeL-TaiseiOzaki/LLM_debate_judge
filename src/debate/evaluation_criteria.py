from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class EvaluationCriteria:
    feedback_criteria: List[Dict[str, Any]]
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class EvaluationPoint:
    focus: str
    sub_evaluation_points: List[str]
    sub_target_document: List[str]
    improvement_suggestions: List[str]
    sub_weight: float

@dataclass
class AspectCriteria:
    aspect: str
    description: str
    target_documents: List[str]
    weight: float
    evaluation_points: List[EvaluationPoint]

@dataclass
class EvaluationCriteria:
    criteria: List[AspectCriteria]
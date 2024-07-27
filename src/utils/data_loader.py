import json
from src.models.debate_data import DebateData
from src.models.evaluation_criteria import EvaluationCriteria

def load_debate_data(file_path: str) -> DebateData:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return DebateData(**data)

def load_evaluation_criteria(file_path: str) -> EvaluationCriteria:
    with open(file_path, 'r', encoding='utf-8') as file:
        criteria = json.load(file)
    return EvaluationCriteria(**criteria)
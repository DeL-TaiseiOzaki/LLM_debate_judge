import json
from typing import Dict, Any
from src.debate.debate_data import DebateData
from src.debate.evaluation_criteria import EvaluationCriteria, AspectCriteria, EvaluationPoint

def load_debate_data(file_path: str) -> DebateData:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return DebateData(**data)

def load_evaluation_criteria(file_path: str) -> EvaluationCriteria:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    criteria = []
    for aspect_data in data:
        evaluation_points = [
            EvaluationPoint(
                focus=point['focus'],
                sub_evaluation_points=point['sub_evaluation_points'],
                sub_target_document=point['sub_target_document'],
                improvement_suggestions=point['improvement_suggestions'],
                sub_weight=point['sub_weight']
            ) for point in aspect_data['evaluation_points']
        ]
        aspect = AspectCriteria(
            aspect=aspect_data['aspect'],
            description=aspect_data['description'],
            target_documents=aspect_data['target_documents'],
            weight=aspect_data['weight'],
            evaluation_points=evaluation_points
        )
        criteria.append(aspect)
    
    return EvaluationCriteria(criteria=criteria)
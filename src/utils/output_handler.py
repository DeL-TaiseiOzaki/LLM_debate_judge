import json
import os
from datetime import datetime
from typing import List, Dict, Any
from src.debate.debate_data import DebateData

def save_output(output_dir: str, debate_data: DebateData, evaluation_results: Dict[str, List[Dict[str, Any]]], summary: str, feedback: str, agent_configs: Dict[str, Any]) -> str:
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename based on current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debate_evaluation_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    # Prepare output data
    output_data = {
        "input_debate_data": debate_data.__dict__,
        "evaluation_results": evaluation_results,
        "summary": summary,
        "feedback": feedback,
        "agent_configurations": agent_configs
    }

    # Write to JSON file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Output saved to: {filepath}")
    return filepath
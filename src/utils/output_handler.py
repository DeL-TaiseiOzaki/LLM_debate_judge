import json
import os
from datetime import datetime

def save_output(output_dir: str, debate_data, evaluation_results, summary, feedback, agent_configs):
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
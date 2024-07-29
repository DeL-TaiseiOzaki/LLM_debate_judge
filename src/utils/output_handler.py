import json
import os
from datetime import datetime
from typing import List, Dict, Any
from src.agents.summary_agent import SummaryAgent
from src.agents.feedback_agent import FeedbackAgent

def save_output(output_dir: str, debate_data, evaluation_agents: List, summary_agent: SummaryAgent, feedback_agent: FeedbackAgent, agent_configs: Dict[str, Any]) -> str:
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename based on current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debate_evaluation_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    # Convert agents to dictionary
    evaluation_results = [agent.to_dict() for agent in evaluation_agents]
    summary_agent_dict = summary_agent.to_dict()
    feedback_agent_dict = feedback_agent.to_dict()

    # Prepare output data
    output_data = {
        "input_debate_data": debate_data.__dict__,
        "evaluation_results": evaluation_results,
        "summary": summary_agent_dict,
        "feedback": feedback_agent_dict,
        "agent_configurations": agent_configs
    }

    # Write to JSON file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Output saved to: {filepath}")
    return filepath
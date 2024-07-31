import os
from typing import Dict, Any
from dotenv import load_dotenv
from src.debate.debate_data import DebateData
from src.debate.evaluation_criteria import EvaluationCriteria
from src.agents.evaluation_agent import EvaluationAgent
from src.agents.summary_agent import SummaryAgent
from src.agents.feedback_agent import FeedbackAgent
from src.llm.openai_client import OpenAIClient
from src.utils.data_loader import load_debate_data, load_evaluation_criteria
from src.utils.prompt_loader import load_prompt
from src.utils.output_handler import save_output
from src.utils.logger import logger

def get_env_or_default(key: str, default: str) -> str:
    return os.getenv(key, default)

def main():
    # Load environment variables
    load_dotenv()

    # Get API key from .env file
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set OPENAI_API_KEY in your .env file.")

    logger.info("Starting debate evaluation process")

    # Load data
    logger.info("Loading debate data and evaluation criteria")
    debate_data = load_debate_data(get_env_or_default('DEBATE_DATA_PATH', 'data/debate_data.json'))
    evaluation_criteria = load_evaluation_criteria(get_env_or_default('EVALUATION_CRITERIA_PATH', 'data/evaluation_criteria.json'))

    # Load prompts
    logger.info("Loading prompts")
    evaluation_prompt = load_prompt(get_env_or_default('EVALUATION_PROMPT_PATH', 'data/prompts/evaluation_prompt.json'))
    summary_prompt = load_prompt(get_env_or_default('SUMMARY_PROMPT_PATH', 'data/prompts/summary_prompt.json'))
    feedback_prompt = load_prompt(get_env_or_default('FEEDBACK_PROMPT_PATH', 'data/prompts/feedback_prompt.json'))
    
    # Create evaluation agents
    logger.info("Creating evaluation agents")
    evaluation_model = get_env_or_default('EVALUATION_MODEL', 'gpt-3.5-turbo')
    evaluation_agents = []
    for aspect in evaluation_criteria.criteria:
        agent = EvaluationAgent(OpenAIClient(api_key, evaluation_model), evaluation_prompt, aspect)
        evaluation_agents.append(agent)

    # Create summary and feedback agents
    logger.info("Creating summary and feedback agents")
    summary_model = get_env_or_default('SUMMARY_MODEL', 'gpt-3.5-turbo')
    feedback_model = get_env_or_default('FEEDBACK_MODEL', 'gpt-3.5-turbo')
    summary_agent = SummaryAgent(OpenAIClient(api_key, summary_model), summary_prompt)
    feedback_agent = FeedbackAgent(OpenAIClient(api_key, feedback_model), feedback_prompt)

    # Perform evaluations
    logger.info("Starting evaluation process")
    evaluation_results = []
    updated_agent_configs = {"evaluation_agents": []}
    for i, agent in enumerate(evaluation_agents, 1):
        logger.info(f"Running evaluation agent {i}/{len(evaluation_agents)}")
        results = agent.evaluate(debate_data)
        for result in results:
            result['aspect'] = agent.aspect.aspect
        evaluation_results.extend(results)
        updated_agent_configs["evaluation_agents"].append({
            "model": agent.llm_client.model,
            "prompt": {
                "system_prompt": agent.get_system_prompt(debate_data),
                "user_prompts": {result["prompt_id"]: result["prompt"] for result in results}
            },
            "aspect": agent.aspect.aspect
        })
    logger.info("Evaluation process completed")

    # Summarize results
    logger.info("Starting summary generation")
    summary = summary_agent.summarize(debate_data, evaluation_results)
    updated_agent_configs["summary_agent"] = {
        "model": summary_agent.llm_client.model,
        "prompt": {
            "system_prompt": summary_agent.get_system_prompt(debate_data),
            "user_prompt": summary_agent.get_user_prompt(evaluation_results)
        }
    }
    logger.info("Summary generation completed")

    # Generate feedback
    logger.info("Starting feedback generation")
    feedback = feedback_agent.generate_feedback(debate_data, summary)
    updated_agent_configs["feedback_agent"] = {
        "model": feedback_agent.llm_client.model,
        "prompt": {
            "system_prompt": feedback_agent.get_system_prompt(debate_data),
            "user_prompt": feedback_agent.get_user_prompt(summary)
        }
    }
    logger.info("Feedback generation completed")

    # Save output
    logger.info("Saving output")
    output_dir = get_env_or_default('OUTPUT_DIR', 'output')
    save_output(output_dir, debate_data, evaluation_results, summary, feedback, updated_agent_configs)

    logger.info("Debate evaluation process completed")

if __name__ == "__main__":
    main()
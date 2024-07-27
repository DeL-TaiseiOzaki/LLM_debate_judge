import os
from dotenv import load_dotenv
from src.models.debate_data import DebateData
from src.models.evaluation_criteria import EvaluationCriteria
from src.agents.evaluation_agent import EvaluationAgent
from src.agents.summary_agent import SummaryAgent
from src.agents.feedback_agent import FeedbackAgent
from src.llm.openai_client import OpenAIClient
from src.utils.data_loader import load_debate_data, load_evaluation_criteria
from src.utils.prompt_loader import load_prompt
from src.utils.output_handler import save_output

def get_env_or_default(key: str, default: str) -> str:
    return os.getenv(key, default)

def main():
    # Load environment variables
    load_dotenv()

    # Get API key from .env file
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set OPENAI_API_KEY in your .env file.")

    # Load data
    debate_data = load_debate_data(get_env_or_default('DEBATE_DATA_PATH', 'data/debate_data.json'))
    evaluation_criteria = load_evaluation_criteria(get_env_or_default('EVALUATION_CRITERIA_PATH', 'data/evaluation_criteria.json'))

    # Load prompts
    evaluation_prompt = load_prompt(get_env_or_default('EVALUATION_PROMPT_PATH', 'data/prompts/evaluation_prompt.json'))
    summary_prompt = load_prompt(get_env_or_default('SUMMARY_PROMPT_PATH', 'data/prompts/summary_prompt.json'))
    feedback_prompt = load_prompt(get_env_or_default('FEEDBACK_PROMPT_PATH', 'data/prompts/feedback_prompt.json'))

    # Create agents with individual models
    evaluation_model = get_env_or_default('EVALUATION_MODEL', 'gpt-3.5-turbo')
    summary_model = get_env_or_default('SUMMARY_MODEL', 'gpt-3.5-turbo')
    feedback_model = get_env_or_default('FEEDBACK_MODEL', 'gpt-3.5-turbo')

    evaluation_agent = EvaluationAgent(OpenAIClient(api_key, evaluation_model), evaluation_prompt)
    summary_agent = SummaryAgent(OpenAIClient(api_key, summary_model), summary_prompt)
    feedback_agent = FeedbackAgent(OpenAIClient(api_key, feedback_model), feedback_prompt)

    # Perform evaluations
    evaluation_results = evaluation_agent.evaluate(debate_data, evaluation_criteria)

    # Summarize results
    summary = summary_agent.summarize(evaluation_results)

    # Generate feedback
    feedback = feedback_agent.generate_feedback(debate_data, summary)

    # Prepare agent configurations
    agent_configs = {
        "evaluation_agent": {"model": evaluation_model, "prompt": evaluation_prompt},
        "summary_agent": {"model": summary_model, "prompt": summary_prompt},
        "feedback_agent": {"model": feedback_model, "prompt": feedback_prompt}
    }

    # Save output
    output_dir = get_env_or_default('OUTPUT_DIR', 'output')
    save_output(output_dir, debate_data, evaluation_results, summary, feedback, agent_configs)

if __name__ == "__main__":
    main()
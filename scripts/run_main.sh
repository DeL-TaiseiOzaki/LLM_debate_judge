#!/bin/bash

# Set environment variables
export DEBATE_DATA_PATH="data/debate_data.json"
export EVALUATION_CRITERIA_PATH="data/evaluation_criteria.json"
export EVALUATION_PROMPT_PATH="data/prompts/evaluation_prompt.json"
export SUMMARY_PROMPT_PATH="data/prompts/summary_prompt.json"
export FEEDBACK_PROMPT_PATH="data/prompts/feedback_prompt.json"

# Set models for each agent
export EVALUATION_MODEL="gpt-3.5-turbo"
export SUMMARY_MODEL="gpt-4"
export FEEDBACK_MODEL="gpt-3.5-turbo"

# Set output directory
export OUTPUT_DIR="output"

# Run the main Python script
python src/main.py
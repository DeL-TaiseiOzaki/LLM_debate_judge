#!/bin/bash

# Set environment variables
export DEBATE_DATA_PATH="data/model_debate.json"
export EVALUATION_CRITERIA_PATH="data/evaluation_criteria_test.json"
export EVALUATION_PROMPT_PATH="data/prompts/evaluation_prompt.json"
export SUMMARY_PROMPT_PATH="data/prompts/summary_prompt.json"
export FEEDBACK_PROMPT_PATH="data/prompts/feedback_prompt.json"

# Set models for each agent
export EVALUATION_MODEL="gpt-4o"
export SUMMARY_MODEL="gpt-4o"
export FEEDBACK_MODEL="gpt-4o"

# Set output directory
export OUTPUT_DIR="output"

# プロジェクトのルートディレクトリへのパスを設定
export PYTHONPATH="/home/ozaki_vm/LLM_debate_judge:$PYTHONPATH"

# Run the main Python script
python3 src/main.py
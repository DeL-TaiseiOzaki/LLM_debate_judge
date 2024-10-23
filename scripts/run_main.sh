#!/bin/bash

# Set environment variables
export DEBATE_DATA_PATH="data/debate_data/model_debate2.json"
export EVALUATION_CRITERIA_PATH="data/evaluation_criteria.json"
export EVALUATION_PROMPT_PATH="data/prompts/evaluation_prompt.json"
export SUMMARY_PROMPT_PATH="data/prompts/summary_prompt.json"
export FEEDBACK_PROMPT_PATH="data/prompts/feedback_prompt.json"
export MOTION_SPILIT_PROMPT_PATH="data/prompts/motion_spilit_prompt.json"

export MOTION_SPILIT_MODEL="gpt-4o"
export EVALUATION_MODEL="gpt-4o" #"gpt-4o-2024-08-06"
export SUMMARY_MODEL="gpt-4o" #"gpt-4o-2024-08-06"
export FEEDBACK_MODEL="gpt-4o" #"gpt-4o-2024-08-06"

# Set output directory
export OUTPUT_DIR="output"

# プロジェクトのルートディレクトリへのパスを設定
export PYTHONPATH="/home/ozaki_vm/LLM_debate_judge:$PYTHONPATH"

# Run the main Python script
python3 src/main.py
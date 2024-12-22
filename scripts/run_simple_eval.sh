#!/bin/bash

# デフォルトのパスを設定
DEBATE_DATA=${1:-"debate_data/sample.json"}
EVAL_CRITERIA=${2:-"data/evaluation_criteria.json"}
EVAL_PROMPT=${3:-"data/prompts/evaluation_prompt.json"}
SUMMARY_PROMPT=${4:-"data/prompts/summary_prompt.json"}
OUTPUT_DIR=${5:-"output"}

# Pythonスクリプトを実行
python simplified_evaluation.py \
    --debate_data "$DEBATE_DATA" \
    --evaluation_criteria "$EVAL_CRITERIA" \
    --evaluation_prompt "$EVAL_PROMPT" \
    --summary_prompt "$SUMMARY_PROMPT" \
    --output_dir "$OUTPUT_DIR"
#!/bin/bash

# デフォルトのディレクトリとパスを設定
INPUT_DIR=${1:-"debate_data"}
EVAL_CRITERIA=${2:-"data/evaluation_criteria.json"}
EVAL_PROMPT=${3:-"data/prompts/evaluation_prompt.json"}
SUMMARY_PROMPT=${4:-"data/prompts/summary_prompt.json"}
OUTPUT_DIR=${5:-"output"}

# ログファイルの設定
LOG_DIR="logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/simple_eval_all_$(date +%Y%m%d_%H%M%S).log"

# 実行時の設定を記録
echo "=== Execution Settings ===" | tee -a "$LOG_FILE"
echo "Input Directory: $INPUT_DIR" | tee -a "$LOG_FILE"
echo "Evaluation Criteria: $EVAL_CRITERIA" | tee -a "$LOG_FILE"
echo "Evaluation Prompt: $EVAL_PROMPT" | tee -a "$LOG_FILE"
echo "Summary Prompt: $SUMMARY_PROMPT" | tee -a "$LOG_FILE"
echo "Output Directory: $OUTPUT_DIR" | tee -a "$LOG_FILE"
echo "Log File: $LOG_FILE" | tee -a "$LOG_FILE"
echo "=======================" | tee -a "$LOG_FILE"

# 入力ディレクトリの存在確認
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist." | tee -a "$LOG_FILE"
    exit 1
fi

# 出力ディレクトリの作成
mkdir -p "$OUTPUT_DIR"

# 処理開始時刻の記録
START_TIME=$(date +%s)
echo "Processing started at $(date)" | tee -a "$LOG_FILE"

# カウンターの初期化
TOTAL_FILES=0
PROCESSED_FILES=0
FAILED_FILES=0

# JSONファイルの総数をカウント
for file in "$INPUT_DIR"/*.json; do
    if [ -f "$file" ]; then
        ((TOTAL_FILES++))
    fi
done

echo "Found $TOTAL_FILES JSON files to process" | tee -a "$LOG_FILE"
echo "------------------------" | tee -a "$LOG_FILE"

# 各JSONファイルを処理
for file in "$INPUT_DIR"/*.json; do
    if [ -f "$file" ]; then
        echo "Processing file: $file" | tee -a "$LOG_FILE"
        
        # simplified_evaluation.pyを実行
        if python src/simple_evaluation.py \
            --debate_data "$file" \
            --evaluation_criteria "$EVAL_CRITERIA" \
            --evaluation_prompt "$EVAL_PROMPT" \
            --summary_prompt "$SUMMARY_PROMPT" \
            --output_dir "$OUTPUT_DIR" \
            2>> "$LOG_FILE"; then
            
            ((PROCESSED_FILES++))
            echo "Successfully processed: $file" | tee -a "$LOG_FILE"
        else
            ((FAILED_FILES++))
            echo "Failed to process: $file" | tee -a "$LOG_FILE"
        fi
        
        echo "------------------------" | tee -a "$LOG_FILE"
    fi
done

# 処理終了時刻の記録と実行時間の計算
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# 実行結果のサマリーを出力
echo "=== Execution Summary ===" | tee -a "$LOG_FILE"
echo "Total files: $TOTAL_FILES" | tee -a "$LOG_FILE"
echo "Successfully processed: $PROCESSED_FILES" | tee -a "$LOG_FILE"
echo "Failed: $FAILED_FILES" | tee -a "$LOG_FILE"
echo "Total duration: $DURATION seconds" | tee -a "$LOG_FILE"
echo "Detailed log saved to: $LOG_FILE" | tee -a "$LOG_FILE"
echo "=======================" | tee -a "$LOG_FILE"
#!/bin/bash

# ディレクトリの設定
DEBATE_DATA_DIR="debate_data"
OUTPUT_DIR="output"

# 基本的な環境変数の設定
export EVALUATION_CRITERIA_PATH="data/evaluation_criteria.json"
export EVALUATION_PROMPT_PATH="data/prompts/evaluation_prompt.json"
export SUMMARY_PROMPT_PATH="data/prompts/summary_prompt.json"
export FEEDBACK_PROMPT_PATH="data/prompts/feedback_prompt.json"
export MOTION_SPILIT_PROMPT_PATH="data/prompts/motion_spilit_prompt.json"

export MOTION_SPILIT_MODEL="gpt-4o-2024-11-20"
export EVALUATION_MODEL="gpt-4o-2024-11-20" 
export SUMMARY_MODEL="gpt-4o-2024-11-20" 
export FEEDBACK_MODEL="gpt-4o-2024-11-20" 

export OUTPUT_DIR="$OUTPUT_DIR"
export PYTHONPATH="/home/ozaki_vm/LLM_debate_judge:$PYTHONPATH"

# ログディレクトリの作成
LOGDIR="logs"
mkdir -p "$LOGDIR"

# 現在の日時を取得
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# JSONファイルを処理する関数
process_debate_file() {
    local debate_file="$1"
    local filename=$(basename "$debate_file")
    local logfile="$LOGDIR/${filename%.*}_${TIMESTAMP}.log"
    
    echo "Processing: $filename"
    echo "Log file: $logfile"
    
    # 環境変数の設定とPythonスクリプトの実行
    export DEBATE_DATA_PATH="$debate_file"
    python3 src/main.py 2>&1 | tee "$logfile"
    
    # 処理結果の確認
    if [ $? -eq 0 ]; then
        echo "Successfully processed: $filename"
    else
        echo "Error processing: $filename"
    fi
    echo "----------------------------------------"
}

# メイン処理
echo "Starting debate processing at $(date)"
echo "Processing files in: $DEBATE_DATA_DIR"

# ディレクトリ内のすべてのJSONファイルを処理
find "$DEBATE_DATA_DIR" -type f -name "*.json" | while read file; do
    process_debate_file "$file"
done

echo "Finished processing all debate files at $(date)"
echo "Logs are available in: $LOGDIR"
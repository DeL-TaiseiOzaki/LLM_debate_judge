#!/bin/bash

# デフォルト値の設定
DATA_PATH="/path/to/default/data.csv"
OUTPUT_PATH="/path/to/default/output"
MODEL="gpt-3.5-turbo"
MAX_TOKENS=1000
TEMPERATURE=0.5
PROMPT_DIR="/path/to/default/prompts"
CRITERIA=("論理性" "説得力" "証拠の使用" "反論の質")
API_KEY=""

# コマンドライン引数の解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --data_path)
            DATA_PATH="$2"
            shift 2
            ;;
        --output_path)
            OUTPUT_PATH="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --max_tokens)
            MAX_TOKENS="$2"
            shift 2
            ;;
        --temperature)
            TEMPERATURE="$2"
            shift 2
            ;;
        --prompt_dir)
            PROMPT_DIR="$2"
            shift 2
            ;;
        --criteria)
            CRITERIA=()
            shift
            while [[ $# -gt 0 && ! $1 == --* ]]; do
                CRITERIA+=("$1")
                shift
            done
            ;;
        --api_key)
            API_KEY="$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# API キーを環境変数にセット
if [ -n "$API_KEY" ]; then
    export OPENAI_API_KEY="$API_KEY"
elif [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY is not set. Please provide it using --api_key option or set it as an environment variable."
    exit 1
fi

# クライテリアの配列を文字列に変換
CRITERIA_STR=$(IFS=' ' ; echo "${CRITERIA[*]}")

# Python実行コマンドの決定
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Neither 'python3' nor 'python' command is available. Please install Python 3."
    exit 1
fi

# 必要なライブラリのインストール確認と実行
REQUIRED_PACKAGES="pandas openai tqdm"
for package in $REQUIRED_PACKAGES; do
    if ! $PYTHON_CMD -c "import $package" &>/dev/null; then
        echo "Installing $package..."
        pip install $package
        if [ $? -ne 0 ]; then
            echo "Failed to install $package. Please install it manually."
            exit 1
        fi
    fi
done

# Pythonスクリプトの実行
$PYTHON_CMD evaluate_debate.py \
    --data_path "$DATA_PATH" \
    --output_path "$OUTPUT_PATH" \
    --model "$MODEL" \
    --max_tokens "$MAX_TOKENS" \
    --temperature "$TEMPERATURE" \
    --prompt_dir "$PROMPT_DIR" \
    --criteria $CRITERIA_STR
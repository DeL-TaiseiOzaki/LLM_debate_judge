import argparse
import pandas as pd
from debate_judge_agent import create_agents
import json
import os
from tqdm import tqdm
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Debate evaluation script")
    parser.add_argument("--data_path", type=str, required=True, help="Path to the CSV file containing debate data")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save the evaluation results")
    parser.add_argument("--model", type=str, required=True, help="Name of the GPT model to use")
    parser.add_argument("--max_tokens", type=int, required=True, help="Maximum number of tokens for GPT response")
    parser.add_argument("--temperature", type=float, required=True, help="Temperature for GPT response")
    parser.add_argument("--prompt_dir", type=str, required=True, help="Directory containing prompt files for agents")
    return parser.parse_args()

def evaluate_debate(agents, debate_text):
    results = {}
    for criterion, agent in agents.items():
        evaluation = agent.evaluate(debate_text)
        if evaluation is not None:
            results[criterion] = evaluation
        else:
            results[criterion] = "評価に失敗しました"
    return results

def main():
    args = parse_args()

    # 評価基準とプロンプトファイルのパスを設定
    criteria = ["論理性", "説得力", "証拠の使用", "反論の質"]
    prompt_paths = {criterion: os.path.join(args.prompt_dir, f"{criterion}_prompt.json") for criterion in criteria}

    # エージェントの作成
    agents = create_agents(criteria, args.model, args.max_tokens, args.temperature, prompt_paths)

    # データの読み込みと評価
    df = pd.read_csv(args.data_path)
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        debate_text = f"質問文: {row['質問文']}\n回答文: {row['回答文']}"
        results = evaluate_debate(agents, debate_text)

        # 結果の保存
        output_file = os.path.join(args.output_path, f"evaluation_{index}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        time.sleep(5)  # API制限を考慮したスリープ

if __name__ == "__main__":
    main()
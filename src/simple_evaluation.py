from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from src.llm.openai_client import OpenAIClient
from src.agents.evaluation_agent import EvaluationAgent
from src.agents.summary_agent import SummaryAgent
from src.debate.debate_data import DebateData
from src.debate.evaluation_criteria import AspectCriteria
from src.utils.data_loader import load_debate_data, load_evaluation_criteria
from src.utils.prompt_loader import load_prompt
from src.utils.output_handler import save_simplified_output
from src.utils.logger import logger

def run_simplified_evaluation(
    debate_data_path: str,
    evaluation_criteria_path: str,
    evaluation_prompt_path: str,
    summary_prompt_path: str,
    output_dir: str = "output"
) -> str:
    """
    ディベートの簡易評価を実行し、要約までを行います。
    
    Args:
        debate_data_path (str): ディベートデータのJSONファイルパス
        evaluation_criteria_path (str): 評価基準のJSONファイルパス
        evaluation_prompt_path (str): 評価用プロンプトのJSONファイルパス
        summary_prompt_path (str): 要約用プロンプトのJSONファイルパス
        output_dir (str): 出力ディレクトリパス
    
    Returns:
        str: 出力ファイルのパス
    """
    # 環境変数の読み込み
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    # LLMクライアントの初期化
    llm_client = OpenAIClient(api_key=api_key)

    # データと設定の読み込み
    logger.info("Loading debate data and evaluation criteria")
    debate_data = load_debate_data(debate_data_path)
    evaluation_criteria = load_evaluation_criteria(evaluation_criteria_path)
    evaluation_prompt = load_prompt(evaluation_prompt_path)
    summary_prompt = load_prompt(summary_prompt_path)

    # 評価結果を格納するリスト
    evaluation_results: List[Dict[str, Any]] = []

    # 各観点での評価を実行
    logger.info("Starting evaluation process")
    for aspect_criteria in evaluation_criteria.criteria:
        evaluation_agent = EvaluationAgent(llm_client, evaluation_prompt, aspect_criteria)
        aspect_results = evaluation_agent.evaluate(debate_data)
        evaluation_results.append({
            "aspect": aspect_criteria.aspect,
            "result": aspect_results
        })

    # 要約の生成
    logger.info("Generating summary")
    summary_agent = SummaryAgent(llm_client, summary_prompt)
    summary = summary_agent.summarize(
        debate_data,
        evaluation_results,
        evaluation_criteria.criteria
    )

    # 結果の保存
    logger.info("Saving results")
    output_path = save_simplified_output(
        output_dir,
        debate_data,
        evaluation_results,
        summary,
        "",  # フィードバックは空文字列として保存
        ""   # 議題分析も空文字列として保存
    )

    return output_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run simplified debate evaluation")
    parser.add_argument("--debate_data", required=True, help="Path to debate data JSON file")
    parser.add_argument("--evaluation_criteria", required=True, help="Path to evaluation criteria JSON file")
    parser.add_argument("--evaluation_prompt", required=True, help="Path to evaluation prompt JSON file")
    parser.add_argument("--summary_prompt", required=True, help="Path to summary prompt JSON file")
    parser.add_argument("--output_dir", default="output", help="Output directory path")
    
    args = parser.parse_args()
    
    output_path = run_simplified_evaluation(
        args.debate_data,
        args.evaluation_criteria,
        args.evaluation_prompt,
        args.summary_prompt,
        args.output_dir
    )
    
    print(f"Evaluation completed. Results saved to: {output_path}")
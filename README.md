# LLM Debate Judge

LLMを用いたディベート自動評価システム。ディベートの議論を分析し、客観的な評価とフィードバックを提供します。

## 概要

このシステムは以下の機能を提供します：
- ディベートの議論内容の自動評価
- 多角的な観点からの分析（メリット評価、論理性評価、反論への対応）
- 詳細なフィードバックの生成
- 議題の意図分析

## セットアップ

### 必要条件
- Python 3.8以上
- OpenAI API キー

### インストール

1. リポジトリのクローン
```bash
git clone https://github.com/yourusername/LLM_debate_judge.git
cd LLM_debate_judge
```

2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
```bash
export OPENAI_API_KEY='your-api-key'
```

## 使用方法

### 単一のディベートデータを評価する場合
```bash
./run_single.sh
```

### 複数のディベートデータを一括評価する場合
```bash
./process_debates.sh
```

### ディベートデータのフォーマット
```json
{
    "topic": "議題",
    "affirmative_argument": "肯定側の主張",
    "counter_argument": "否定側の反論",
    "reconstruction": "肯定側の再構築"
}
```

## ディレクトリ構造
```
LLM_debate_judge/
├── data/              # 評価基準、プロンプトなどの設定ファイル
├── src/               # ソースコード
│   ├── agents/       # 評価エージェント
│   ├── debate/       # ディベートデータ処理
│   ├── llm/          # LLMクライアント
│   └── utils/        # ユーティリティ
├── debate_data/      # ディベートデータ
└── output/           # 評価結果の出力
```

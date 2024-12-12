import json
import os
from pathlib import Path

def rename_affirmative_column(directory_path):
    """
    ディレクトリ内の議論データJSONファイルの 'affirmative' カラムを 'affirmative_argument' に変更する
    
    Args:
        directory_path (str): JSONファイルが格納されているディレクトリのパス
    """
    # ディレクトリ内の全JSONファイルを取得
    json_files = Path(directory_path).glob('*.json')
    
    for json_file in json_files:
        try:
            # JSONファイルを読み込む
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # affirmativeカラムの名前を変更
            if 'affirmative' in data:
                data['affirmative_argument'] = data.pop('affirmative')
            
            # 変更したデータを保存
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Successfully processed: {json_file}")
            
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

# テスト用のサンプルデータを作成して処理を実行
if __name__ == "__main__":

    # スクリプトを実行
    rename_affirmative_column("debate_data")

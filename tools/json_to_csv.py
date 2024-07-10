import json
import csv
import os

import json
import csv
import os

def read_json_files(directory, key_mapping):
    data = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)

            # JSONファイルを読み込む
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

                gen_questions = json_data.get('result', '').split('\n')
                for gen_question in gen_questions:
                    if gen_question.strip():  # 空の行を無視
                        extracted_data = {csv_key: json_data.get(json_key, '') for json_key, csv_key in key_mapping.items()}
                        extracted_data['生成質問例'] = gen_question
                        data.append(extracted_data)


    return data

def write_to_csv(data, output_file):
    if not data:
        return
    # CSVファイルに書き出し
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

directory = '/home/output/35-0.3-quattro'
keys_to_extract = {'sample_question':"質問例", 'answer':"解答", 'result':"生成質問例"}
output_csv_file = '/home/output/35-0.3-quattro/output.csv'

# プログラムの実行
json_data = read_json_files(directory, keys_to_extract)
write_to_csv(json_data, output_csv_file)

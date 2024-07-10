import pandas as pd

# CSVファイルのパス
file_paths = [
    '/home/data/paypay.csv', 
    '/home/data/あいおいニッセイ同和.csv', 
    '/home/data/ソニー損保.csv', 
    '/home/data/奥村組.csv']

dataframes = []
for file in file_paths:
    df = pd.read_csv(file)
    df_clean = df.dropna()  # nullを含む行を除外
    dataframes.append(df_clean.sample(1))
    
# 選択したデータを結合
combined_data = pd.concat(dataframes)

# 新しいCSVファイルとして保存
combined_data.to_csv('/home/data/for_example.csv', index=False)

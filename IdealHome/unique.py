import pandas as pd

# CSVを読み込み
df = pd.read_csv("IdealHome/IdealHome/suumo.csv")

col = "url"  # URL列名

# 重複している行だけ抽出（完全一致で判定）
duplicates = df[df.duplicated(subset=[col], keep=False)]

# 結果表示
print(duplicates[[col]])

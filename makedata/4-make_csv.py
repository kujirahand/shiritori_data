import glob
import csv

FILE_OUT = "result/csvdata.txt"

csv_example = """
残飯,1285,1285,5621,名詞,一般,*,*,*,*,残飯,ザンパン,ザンパン
賃搗,1285,1285,5622,名詞,一般,*,*,*,*,賃搗,チンヅキ,チンズキ
常民,1285,1285,5622,名詞,一般,*,*,*,*,常民,ジョウミン,ジョーミン
別後,1285,1285,5622,名詞,一般,*,*,*,*,別後,ベツゴ,ベツゴ
心血,1285,1285,5622,名詞,一般,*,*,*,*,心血,シンケツ,シンケツ
九輪,1285,1285,5189,名詞,一般,*,*,*,*,九輪,クリン,クリン
"""

def filter_csv_data(lines):
    result = []
    for line in lines:
        title = line[0].strip()
        hinsi = line[4].strip()
        yomi = line[11].strip()
        # 名詞以外を除去
        if hinsi != "名詞":
            continue
        result.append(f"{title}\t{yomi}")
    return result

result = []
files = glob.glob("csv/*.csv")
for file in files:
    print(f"Processing {file}...")
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        filtered_data = filter_csv_data(reader)
        result.extend(filtered_data)

# 重複を除去
result = list(set(result))
# ヨミでソート
result.sort(key=lambda x: x.split("\t")[1])

with open(FILE_OUT, "w", encoding="utf-8", newline='') as f:
    f.write("\n".join(result))
print(f"Output written to {FILE_OUT}")
print(f"Total entries: {len(result)}")

from glob import glob
import json

uniq_check = {}
result = {}
files = glob('src/*.txt')
for file in files:
    with open(file, 'r', encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()
        for line in lines:
            title, yomi = line.split('\t')
            title = title.strip()
            yomi = yomi.strip()
            # 数字から始まるものはスキップ
            if title[0] in '0123456789０１２３４５６７８９':
                continue
            # ひらがな→カタカナ
            yomi = ''.join(
                chr(ord(c) + 96) if 'ぁ' <= c <= 'ゖ' else c for c in yomi
            )
            # カタカナ以外があればスキップ
            if any(not ('ァ' <= c <= 'ヶ') for c in yomi):
                continue
            if not yomi:
                continue
            # 長すぎるものはスキップ
            if len(yomi) > 10:
                continue
            # 短すぎるものもスキップ
            if len(yomi) <= 1:
                continue
            # 小さな「っ」から始まる語は飛ばす
            if yomi[0] == 'ッ':
                continue
            # 末尾に「ん」があるものはスキップ
            if yomi[-1] == 'ン':
                continue
            if title in uniq_check:
                continue
            uniq_check[title] = True
            k = yomi[0]
            # 濁点があれば、濁点ナシのカナに変換
            # if 'ガ' <= k <= 'ポ':
            #    base_k = chr(ord(k) - 1)
            #    if base_k in 'カサタナハマヤラワ':
            #        k = base_k
            # 小書きがあれば、大書きに変換
            small_to_large = {
                'ァ': 'ア', 'ィ': 'イ', 'ゥ': 'ウ', 'ェ': 'エ', 'ォ': 'オ',
                'ガ': 'カ', 'ギ': 'キ', 'グ': 'ク', 'ゲ': 'ケ', 'ゴ': 'コ',
                'ザ': 'サ', 'ダ': 'タ', 'バ': 'ハ', 'パ': 'ハ',
                'ッ': 'ツ', 'ヴ': 'フ',
                'ジ': 'シ', 'ヂ': 'チ', 'ビ': 'ヒ', 'ピ': 'ヒ',
                'ャ': 'ヤ', 'ュ': 'ユ', 'ョ': 'ヨ',
                'ヮ': 'ワ',
                'ズ': 'ス', 'ヅ': 'ツ', 'ブ': 'フ', 'プ': 'フ',
                'ゼ': 'セ', 'デ': 'テ', 'ベ': 'ヘ', 'ペ': 'ヘ',
                'ゾ': 'ソ', 'ド': 'ト', 'ボ': 'ホ', 'ポ': 'ホ',
                'ヰ': 'イ', 'ヱ': 'エ', 'ヲ': 'オ',
            }
            if k in small_to_large:
                k = small_to_large[k]
            if k not in result:
                result[k] = []
            result[k].append((title, yomi))

for key, values in result.items():
    with open(f'out/{key}.csv', 'w', encoding="utf-8") as f:
        for title, yomi in values:
            f.write(f'{title}\t{yomi}\t{key}\n')
        #json.dump(values, f, ensure_ascii=False, indent=2)
        print(f'Wrote out/{key}.csv with {len(values)} entries')

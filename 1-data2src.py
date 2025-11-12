#!/usr/bin/env python
import MeCab
import glob
import re
import yomi

# --- MeCab設定 ---
tagger = yomi.tagger

# --- 入出力ファイル名 ---
INPUT_FILE = 'data/data.txt'
OUTPUT_FILE = 'src/data2src.txt'

# --- 日本語のみを許可する正規表現 ---
# ひらがな・カタカナ・漢字を許可（英数字や記号は除外）
re_japanese = re.compile(r'^[ぁ-んァ-ン一-龥ー]+$')
re_katakana = re.compile(r'^[ァ-ンー]+$')

# --- 名詞の集合（重複除去） ---
nouns = set()

exclide_list = [
    "あへ", "む", "そっ", "ワールドイズマイン", 
]

def load_from_file(filename):
    """テキストファイルを読み込み、名詞を抽出して nouns セットに追加する"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        try:
            with open(filename, 'r', encoding='shift_jis') as f:
                text = f.read()
                return text
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    return ""

# --- 処理本体 ---
def load_text(filename):
    """テキストファイルを読み込み、名詞を抽出して nouns セットに追加する"""
    text = load_from_file(filename)
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        line = re.sub(r'《.+?》', '', line)  # 空白削除
        line = line.replace('｜', '')  # ルビ用記号削除
        node = tagger.parseToNode(line)
        while node:
            features = node.feature.split(',')
            # 「名詞,一般」のみ対象
            # print(features)
            if features[0] == '名詞' and features[2] == '一般':
                word = node.surface.strip()
                # 一文字もOK、日本語文字のみ
                if word and re_japanese.match(word) and len(word) <= 10:
                    if word not in exclide_list:
                        nouns.add(word)
            node = node.next

# --- enum ---
files = glob.glob('data/**/*.txt', recursive=True)
for filename in files:
    print("=== Processing", filename)
    load_text(filename)

# --- 出力 ---
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    for noun in sorted(nouns):
        yomi_text = yomi.get_yomi(noun)
        if not yomi_text:
            continue
        if not re_katakana.match(yomi_text):
            continue
        f.write(f'{noun}\t{yomi_text}\n')

print(nouns)
print(f'抽出完了: {len(nouns)} 件の名詞を {OUTPUT_FILE} に出力しました。')

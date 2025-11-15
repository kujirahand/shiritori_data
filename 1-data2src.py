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
    "あへ", "む", "そっ", "ワールドイズマイン", "ホホ"
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
    cnt = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        line = re.sub(r'《.+?》', '', line)  # 空白削除
        line = line.replace('｜', '')  # ルビ用記号削除
        node = tagger.parseToNode(line)
        while node:
            word = node.surface.strip()
            if re.match(r'^[a-zA-Z0-9]+$', word):
                node = node.next
                continue
            features = node.feature.split(',')
            # 「名詞,一般」のみ対象
            # クラゲ ['名詞', '一般', '*', '*', '*', '*', 'クラゲ', 'クラゲ', 'クラゲ']
            # ヒトデ ['名詞', '一般', '*', '*', '*', '*', 'ヒトデ', 'ヒトデ', 'ヒトデ']
            # サンショウウオ ['名詞', '一般', '*', '*', '*', '*', 'サンショウウオ', 'サンショウウオ', 'サンショーウオ']
            if features[0] == '名詞' and features[1] == '一般':
                print(word, features)
                # 一文字もOK、日本語文字のみ
                if word and len(word) <= 15:
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
            print('Skipping (not katakana):', noun, '->', yomi_text)
            continue
        f.write(f'{noun}\t{yomi_text}\n')

print(nouns)
print(f'抽出完了: {len(nouns)} 件の名詞を {OUTPUT_FILE} に出力しました。')

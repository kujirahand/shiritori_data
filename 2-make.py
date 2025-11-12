#!/usr/bin/env python
from glob import glob
import re
import json

starts_with_exclode_list = [
    "アッハ", "アハ", "ワハ", "イヒヒ","ウフ","エヘ","オホホ",
    "ゴホンゴホン", "ゴホン", "コホン", "コホンコホン", "処女", "ギャァ", "ギィェ",
    "フラ", "ヘロヘロ", "ハハハ", "ヒヒヒ", "ホホホ", "ホホホホ", "ヒュルル", "アヘ",
    "スヤスヤ", "ずっと", "夢じゃない", "びれ", "モシクハ",
    "グゥモォ", "ムクムク", "第一", "第二", "第三", "第四", "第五",
    "グオォ", "ヘヘヘ", "オノレ", "ウシテモ", "人肉", "ん", "ないじゃない",
    "いつまでも", "ン", "モゥ", "そこ", "ふふ", 
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "０", "１", "２", "３", "４", "５", "６", "７", "８", "９",
    "アアッ", "アトカラアトカラ", "アト",
    "アニリン", "アブサン", "アラユル","フフ",
    "ウハ","ウッフ","ウムッ","ウヨウヨ",
    "ヘヘイ", "ヘエッ", "ヘヘン", "ヘエイ","ヘエッ","ヘエー",
    "ジュゥォン","ジュ","ジンパジー","ナルモノニ","ガチガチ", "メチャクチャ",
    "ウルトコロノ","ヨロヨロ","ガサガサ","ガチャガチャ","ガラガラ","ガンガン",
    "ギュウギュウ","ギンギン","グチャグチャ","グラグラ","グングン","グンニャリ",
    "ゲラゲラ","ゴチャゴチャ","ゴロゴロ","ザワザワ","ジャブジャブ","ジャラジャラ",
    "ジュクジュク","ジョロジョロ","ズクズク","ズンズン","ドキドキ","ドンドン",
    "バタバタ","バラバラ","ビクビク","ビチャビチャ","ビンビン","ブクブク",
    "ブヨブヨ","ブルブル","ベタベタ","ベロベロ","ボロボロ","ボンヤリ","ポタポタ",
    "ポンポン","マゴマゴ","マルマル","ミシミシ","ムズムズ","ムニャムニャ","メソメソ",
    "モヤモヤ","モロモロ","ヤキモキ","ヤンヤン","ユラユラ","ヨチヨチ","ヨロヨロ",
    "ラブラブ","リクツ","ルンルン","レロレロ","ロクデナシ","ワイワイ","ワラワラ",
    "ドッコイ","ヨボヨボ","ナニイ","コトコトコトコト", "ナスリ",
]

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
            # 漢数字などをスキップ
            if re.match(r'^[一二三四五六七八九十百千万億兆年月日時分秒世紀]+$', title):
                continue
            if not yomi:
                continue
            # 長すぎるものはスキップ
            if len(title) > 10:
                continue
            # 短すぎるものもスキップ
            if len(yomi) <= 1:
                continue
            # 小さな「っ」から始まる語は飛ばす
            if yomi[0] == 'ッ':
                continue
            # 除外国を先頭に持つものはスキップ
            skip_flag = False
            for ex in starts_with_exclode_list:
                if yomi.startswith(ex):
                    skip_flag = True
                    break
            if skip_flag:
                continue
            # 末尾に「ん」があるものはスキップ (ヨミを得るために辞書引きする場合に困るため)
            #if yomi[-1] == 'ン':
            #    continue
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

cnt = 0
for key, values in result.items():
    with open(f'out/{key}.csv', 'w', encoding="utf-8") as f:
        for title, yomi in values:
            f.write(f'{title}\t{yomi}\t{key}\n')
            cnt += 1
        #json.dump(values, f, ensure_ascii=False, indent=2)
        print(f'Wrote out/{key}.csv with {len(values)} entries')
print("Total entries:", cnt)
#!/usr/bin/env python
import re

IN_FILE = "data/titles2.txt"
OUT_FILE = "data/titles3.txt"

title_dict = {}
with open(IN_FILE, "r", encoding="utf-8") as inp, open(OUT_FILE, "w", encoding="utf-8") as out:
    for line in inp:
        parts = line.strip().split("\t")
        if len(parts) != 2:
            continue
        title, yomi = parts
        # 年号を除去
        if re.match(r"^(紀元前|明治|大正|昭和|平成|令和)\d+年$", title):
            continue
        # 一覧を除去
        if title.endswith("一覧"):
            continue
        # 重複を除去
        if title in title_dict:
            continue
        title_dict[title] = yomi

        # ヨミガナをカタカナに変換
        yomi_katakana = ""
        for char in yomi:
            code = ord(char)
            if 0x3041 <= code <= 0x3096:  # ひらがな
                yomi_katakana += chr(code + 0x60)
            else:
                yomi_katakana += char
        out.write(f"{title}\t{yomi_katakana}\n")
print(f"Converted readings written to {OUT_FILE}")

#!/usr/bin/env python
import bz2
import re
import mwparserfromhell

IN_FILE = "data/jawiki-latest-pages-articles.xml.bz2"
OUT_FILE = "data/titles2.txt"

def extract_summary(wikitext):
    """wikitext から最初の段落部分を抜き出す"""
    text = mwparserfromhell.parse(wikitext).strip_code()  # Wiki記法を除去
    text = text.strip()
    # 最初の空行までを「概要」とみなす
    summary = text.split("\n\n")[0]
    summary = summary.replace("\n", " ")
    return summary

def extract_yomi(page_title, summary):
    """概要テキストからカタカナ読みを抽出する（簡易版）"""
    # 例として「名前空間（なまえくうかん、namespace）は、...」のようなパターンを抽出
    try:
        match = re.search(page_title + r'（([ぁ-ん]+)、?([a-zA-Z]*)）(とは|は、)', summary)
        if match:
            return match.group(1)
    except Exception as _:
        return ""

def parse_wiki_dump(filename):
    page_title = None
    in_text = False
    page_text = []
    i = 0

    with open(OUT_FILE, "w", encoding="utf-8") as out:
        with bz2.open(filename, mode='rt', encoding='utf-8') as f:
            for line in f:
                # ページタイトル
                if "<title>" in line:
                    page_title = re.sub(r".*<title>(.*?)</title>.*", r"\1", line).strip()

                # 本文開始
                if "<text" in line:
                    in_text = True
                    page_text = []
                    line = re.sub(r".*<text.*?>", "", line)

                # 本文収集中
                if in_text:
                    # 本文終了
                    if "</text>" in line:
                        line = re.sub(r"(.*?)</text>.*", r"\1", line)
                        page_text.append(line)
                        in_text = False

                        # カテゴリのような不要ページを除外
                        if page_title.startswith(("Category:", "Template:", "ファイル:", "Help:")):
                            continue
                        if re.match(r"\d+月\d+日", page_title):
                            continue
                        if re.match(r"^\d+年", page_title):
                            continue

                        text = "".join(page_text)
                        summary = extract_summary(text)

                        yomi = extract_yomi(page_title, summary)
                        if not yomi:
                            continue
                        # print(f"{page_title}\t{summary}")
                        # print(f"{page_title}\t{yomi}")
                        # result.append(f"{page_title}\t{yomi}")
                        out.write(f"{page_title}\t{yomi}\n")
                        i += 1
                        #
                        if i % 100 == 0:
                            print(f"{i}: {page_title}\t{yomi}")
                            out.flush()
                    else:
                        page_text.append(line)

# 実行
parse_wiki_dump(IN_FILE)

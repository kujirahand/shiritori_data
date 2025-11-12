import MeCab

# MeCab初期化（辞書パスを指定する場合は -d オプションを追加）
dicpath = "/opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd"
tagger = MeCab.Tagger((f"-Ochasen -d {dicpath}")) 

def get_yomi(text: str) -> str:
    """文章を入力してヨミガナ（ひらがな）を返す"""
    node = tagger.parseToNode(text)
    result = []
    while node:
        features = node.feature.split(',')
        # 品詞情報など: ['名詞','一般','*','*','*','*','ヨミ','原形']
        if len(features) >= 8:
            yomi = features[6]
            if yomi != '*':
                result.append(yomi)
            else:
                result.append(node.surface)
        else:
            result.append(node.surface)
        node = node.next
    return ''.join(result)

# テスト例
if __name__ == '__main__':
    text = "すもももももももものうち"
    print("原文:", text)
    print("読み:", get_yomi(text))

# 「しりとり」のための辞書データ作成ツールとデータ

このリポジトリは、テキストファイルなどのデータから「しりとり」用の辞書データを作成するためのツール群を提供します。

基本的に、dataフォルダに、テキストファイル(*.txt)をたくさん保存します。
そして、1-data2src.py、2-make.py…と番号順にスクリプトを実行していくとデータが生成されます。

## しりとりデータだけが欲しい方

[こちらのRelease](https://github.com/kujirahand/shiritori_data/releases)から`out.zip`または`shiritori.db.zip`をダウンロードしてください。
`shiritori.db.zip`は、[kudb](https://pypi.org/project/kudb/)用のデータベース(SQLite)形式です。

## ツールを利用して自分で辞書データを作成したい方

ツールの利用には、MeCabが必要です。MeCabはC++で書かれた高速な形態素解析エンジンで、多くの言語バインディングが提供されています。Pythonからも利用できます。

Windowsであれば、下記にて、インストーラーをダウンロードできます。

- [形態素解析エンジン MeCab](https://taku910.github.io/mecab/#download)


macOSの場合には、Homebrewを使ってインストールできます。Homebrewは、macOS用のパッケージ管理システムです。Homebrewがインストールされていない場合には、[Homebrew](https://brew.sh/index_ja)を参考にしてインストールしてください。
Homebrewがインストールされたら、次のコマンドでMeCabをインストールできます。

```sh
brew install mecab mecab-ipadic
```

続いて、ライブラリをインストールします。

```sh
pip install -r requirements.txt
```

また、`make`をインストールしておいてください。

## 単語データの作り方

`data`フォルダの中に、テキストファイルを保存します。テキストファイルに、しりとりで使いたい単語を含むテキストを記述してください。

準備ができたら、以下のコマンドを実行します。

```
make all
```

コマンドの実行には、`make`が必要です。もし、なければ、1-xxx、2-xxxのようにスクリプトが用意されていますので、番号順にスクリプトを実行してください。

`out`フォルダにしりとりデータが作成されます。


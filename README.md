# 「しりとり」のための単語データベース作成ツール

このリポジトリは、テキストファイルなどのデータから「しりとり」用の辞書データを作成するためのツール群を提供します。

基本的に、dataフォルダに、テキストファイル(*.txt)を保存します。
そして、下記のライブラリをインストールした上で`make.bat`か`make.sh`を実行します。

## しりとりデータだけが欲しい方

[こちらのRelease](https://github.com/kujirahand/shiritori_data/releases)から`out.zip`または`shiritori.db.zip`をダウンロードしてください。
`shiritori.db.zip`は、[kudb](https://pypi.org/project/kudb/)用のデータベース(SQLite)形式です。

## ツールを利用して自分で辞書データを作成したい方

ツールの利用には、MeCabが必要です。MeCabはC++で書かれた高速な形態素解析エンジンで、多くの言語バインディングが提供されています。Pythonからも利用できます。

### Windows WSL/Ubuntu/Debianの場合

Windowsの場合は、WSLをセットアップして、Ubuntu/Linux上でMeCabをインストールして、作業を行ってください。Ubuntu/Linuxでは、下記のコマンドでMeCabをインストールできます。

```sh
sudo apt update
sudo apt install mecab mecab-ipadic
```

### macOSの場合

macOSの場合には、Homebrewを使ってインストールできます。Homebrewは、macOS用のパッケージ管理システムです。Homebrewがインストールされていない場合には、[Homebrew](https://brew.sh/index_ja)を参考にしてインストールしてください。
Homebrewがインストールされたら、次のコマンドでMeCabをインストールできます。

```sh
brew install mecab mecab-ipadic
```

### 共通のセットアップ

続いて、ライブラリをインストールします。

```sh
pip install -r requirements.txt
```

## 単語データの作り方

`data`フォルダの中に、テキストファイルを保存します。テキストファイルに、しりとりで使いたい単語を含むテキストを記述してください。

準備ができたら、以下のコマンドを実行します。

```
# macOS/Linuxなら
make.sh
# あるいは
make all
```

すると、`out`フォルダにしりとりデータが作成されます。
また、`shiritori.db`という名前でkudb用のデータベースファイルも作成されます。

#!/usr/bin/env python3
"""
CSV/TSVファイルを指定行数で分割するプログラム
5万行以上のCSV/TSVファイルを5万行ごとに分割します。
"""

import csv
import sys
import argparse
from pathlib import Path


def count_lines(file_path):
    """CSV/TSVファイルの行数を数える"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)


def detect_delimiter(file_path):
    """ファイルの区切り文字を自動判定する"""
    with open(file_path, 'r', encoding='utf-8') as f:
        # 最初の数行をサンプルとして読み取り
        sample_lines = []
        for i, line in enumerate(f):
            if i >= 5:  # 最初の5行で判定
                break
            sample_lines.append(line)
        
        sample_text = ''.join(sample_lines)
        
        # csv.Snifferを使用して区切り文字を検出
        try:
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample_text, delimiters=',\t;|').delimiter
            return delimiter
        except (csv.Error, ValueError):
            # 手動でタブとカンマの数を比較
            tab_count = sample_text.count('\t')
            comma_count = sample_text.count(',')
            
            if tab_count > comma_count:
                return '\t'
            else:
                return ','


def split_csv(input_file, lines_per_file=50000, output_dir=None, delimiter=None, force_tsv=False, no_header=False):
    """
    CSV/TSVファイルを指定行数で分割する
    
    Args:
        input_file (str): 入力CSV/TSVファイルのパス
        lines_per_file (int): 分割する行数（デフォルト: 50000）
        output_dir (str): 出力ディレクトリ（デフォルト: 入力ファイルと同じディレクトリ）
        delimiter (str): 区切り文字（None の場合は自動判定）
        force_tsv (bool): TSVファイルとして強制的に扱う
        no_header (bool): ヘッダー行を無視する
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"エラー: ファイル '{input_file}' が見つかりません。")
        return False
    
    # 出力ディレクトリの設定
    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # 区切り文字の決定
    if delimiter is None:
        if force_tsv:
            delimiter = '\t'
        else:
            delimiter = detect_delimiter(input_file)
    
    # ファイル形式の表示
    file_format = "TSV" if delimiter == '\t' else "CSV"
    print(f"ファイル形式: {file_format} (区切り文字: {repr(delimiter)})")
    
    # 総行数をカウント
    total_lines = count_lines(input_file)
    print(f"総行数: {total_lines:,}行")
    
    if total_lines <= lines_per_file:
        print(f"ファイルの行数が{lines_per_file:,}行以下のため、分割は不要です。")
        return True
    
    # ファイル名の準備
    base_name = input_path.stem
    extension = input_path.suffix
    
    file_count = 0
    current_line = 0
    
    with open(input_file, 'r', encoding='utf-8', newline='') as infile:
        csv_reader = csv.reader(infile, delimiter=delimiter)
        
        # ヘッダー行を取得（存在する場合）
        header = None
        has_header = not no_header
        
        try:
            first_row = next(csv_reader)
            current_line = 1
            if has_header:
                header = first_row
            else:
                # ヘッダーが無い場合は最初の行をデータとして扱う
                header = None
        except StopIteration:
            print("エラー: ファイルが空です。")
            return False
        
        output_file = None
        csv_writer = None
        lines_in_current_file = 0
        
        # 最初のファイルを開始
        file_count += 1
        output_filename = output_dir / f"{base_name}_part{file_count:03d}{extension}"
        output_file = open(output_filename, 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(output_file, delimiter=delimiter)
        
        # ヘッダーを書き込み
        if has_header and header is not None:
            csv_writer.writerow(header)
            lines_in_current_file = 1
        
        print(f"分割開始: {output_filename}")
        
        # 最初の行がヘッダーでない場合は書き込む
        if not has_header and first_row is not None:
            csv_writer.writerow(first_row)
            lines_in_current_file += 1
        
        # データ行を処理
        for row in csv_reader:
            current_line += 1
            
            # 新しいファイルが必要かチェック
            if lines_in_current_file >= lines_per_file:
                output_file.close()
                print(f"完了: {output_filename} ({lines_in_current_file:,}行)")
                
                # 新しいファイルを開始
                file_count += 1
                output_filename = output_dir / f"{base_name}_part{file_count:03d}{extension}"
                output_file = open(output_filename, 'w', encoding='utf-8', newline='')
                csv_writer = csv.writer(output_file, delimiter=delimiter)
                
                # ヘッダーを書き込み
                if has_header and header is not None:
                    csv_writer.writerow(header)
                    lines_in_current_file = 1
                else:
                    lines_in_current_file = 0
                
                print(f"分割続行: {output_filename}")
            
            # データ行を書き込み
            csv_writer.writerow(row)
            lines_in_current_file += 1
            
            # 進捗表示
            if current_line % 10000 == 0:
                progress = (current_line / total_lines) * 100
                print(f"進捗: {current_line:,}/{total_lines:,}行 ({progress:.1f}%)")
        
        # 最後のファイルを閉じる
        if output_file:
            output_file.close()
            print(f"完了: {output_filename} ({lines_in_current_file:,}行)")
    
    print("\n分割完了!")
    print(f"総ファイル数: {file_count}個")
    print(f"出力ディレクトリ: {output_dir}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="CSV/TSVファイルを指定行数で分割します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python split_csv.py input.csv                    # 5万行ごとに分割（自動判定）
  python split_csv.py input.tsv --tsv              # TSVファイルを分割
  python split_csv.py input.csv -l 30000           # 3万行ごとに分割
  python split_csv.py input.csv -o output_dir      # 出力ディレクトリを指定
  python split_csv.py input.csv -d ";"             # セミコロン区切りファイルを分割
  python split_csv.py input.csv --noheader         # ヘッダー無しで分割
  python split_csv.py input.csv -l 25000 -o split_files --tsv --noheader
        """
    )
    
    parser.add_argument('input_file', help='分割するCSV/TSVファイルのパス')
    parser.add_argument('-l', '--lines', type=int, default=50000,
                        help='分割する行数 (デフォルト: 50000)')
    parser.add_argument('-o', '--output', help='出力ディレクトリ (デフォルト: 入力ファイルと同じディレクトリ)')
    parser.add_argument('-d', '--delimiter', help='区切り文字を指定 (デフォルト: 自動判定)')
    parser.add_argument('--tsv', action='store_true', help='TSVファイルとして処理 (タブ区切り)')
    parser.add_argument('--noheader', action='store_true', help='ヘッダー行を無視する（すべての行をデータとして扱う）')
    
    args = parser.parse_args()
    
    if args.lines <= 0:
        print("エラー: 行数は正の整数である必要があります。")
        sys.exit(1)
    
    # 区切り文字の競合チェック
    if args.delimiter and args.tsv:
        print("エラー: --delimiter と --tsv オプションは同時に指定できません。")
        sys.exit(1)
    
    # 区切り文字の決定
    delimiter = None
    if args.delimiter:
        delimiter = args.delimiter
    elif args.tsv:
        delimiter = '\t'
    
    print("CSV/TSVファイル分割プログラム")
    print(f"入力ファイル: {args.input_file}")
    print(f"分割行数: {args.lines:,}行")
    print(f"出力ディレクトリ: {args.output or '入力ファイルと同じディレクトリ'}")
    if delimiter:
        format_type = "TSV" if delimiter == '\t' else f"区切り文字: {repr(delimiter)}"
        print(f"ファイル形式: {format_type}")
    else:
        print("ファイル形式: 自動判定")
    print(f"ヘッダー行: {'無視' if args.noheader else '処理'}")
    print("-" * 50)
    
    success = split_csv(args.input_file, args.lines, args.output, delimiter, args.tsv, args.noheader)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

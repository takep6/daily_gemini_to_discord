import re
import os

def split_markdown_by_date(input_file, output_dir):
    """
    マークダウンファイルを日付ごとに分割します。

    Args:
        input_file (str): 分割対象のマークダウンファイルへのパス。
        output_dir (str): 分割後のファイルを出力するディレクトリへのパス。
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"エラー: 入力ファイルが見つかりません: {input_file}")
        return

    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"ディレクトリを作成しました: {output_dir}")

    # 正規表現でセクションを検索
    # `## YYYY-MM-DD HH:MM:SS の出力` 形式のヘッダーで分割
    sections = re.split(r'(## \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} の出力)', content)

    # 最初の要素はヘッダー前の部分なので無視（通常は空かタイトル）
    # ヘッダーと内容がペアになるように処理
    for i in range(1, len(sections), 2):
        header = sections[i]
        body = sections[i+1].strip()

        # ヘッダーから日付を抽出
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', header)
        if match:
            year, month, day = match.groups()
            date_str = f"{year}{month}{day}"
            
            # 出力ファイル名を作成
            output_filename = os.path.join(output_dir, f"{date_str}_history.md")
            
            # ファイルに書き込み（追記モード）
            with open(output_filename, 'a', encoding='utf-8') as out_f:
                # ファイルが空の場合のみ、Markdownのタイトルを追加
                if out_f.tell() == 0:
                    out_f.write(f"# {year}-{month}-{day} の出力履歴\n\n")
                out_f.write(header + '\n' + body + '\n\n')
            
            print(f"'{output_filename}' にコンテンツを追記しました。")

if __name__ == '__main__':
    INPUT_FILE = '.github/history.md'
    OUTPUT_DIR = '.github/archives'
    split_markdown_by_date(INPUT_FILE, OUTPUT_DIR)
    print("処理が完了しました。")

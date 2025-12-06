#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

# --- 設定項目 ---

# 画像と判定し、要約の対象とする拡張子
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
# 要約を開始する画像の数の閾値
IMAGE_THRESHOLD = 3

# 表示から除外するディレクトリ名・ファイル名のセット
IGNORE_PATTERNS = {
    '.venv',          # Python仮想環境
    '__pycache__',    # Pythonキャッシュ
    '.git',           # Gitリポジトリ
    '.vscode',        # Visual Studio Code設定
    'uv.lock',        # uvロックファイル
    '.python-version' # pyenvバージョンファイル
}
# 表示から除外する拡張子のセット
IGNORE_EXTENSIONS = {
    '.pyc',           # Pythonコンパイル済みファイル
}

# --- スクリプト本体 ---

def tree_with_image_summary(dir_path: Path, prefix: str = ""):
    """
    ディレクトリを再帰的に探索し、特定のファイル/ディレクトリを無視し、
    画像ファイルが閾値以上の場合に要約して表示する関数
    """
    try:
        # 無視リストに含まれるものを除外し、ディレクトリを先に表示するようにソート
        entries = sorted(
            [
                p for p in dir_path.iterdir()
                if p.name not in IGNORE_PATTERNS and p.suffix not in IGNORE_EXTENSIONS
            ],
            key=lambda p: (p.is_file(), p.name.lower())
        )
    except PermissionError:
        print(f"{prefix}├── ⛔ [Permission Denied]")
        return
    except FileNotFoundError:
        print(f"{prefix}├── ❓ [Not Found]")
        return

    # エントリを分類
    dirs = [e for e in entries if e.is_dir()]
    all_files = [e for e in entries if e.is_file()]
    image_files = [f for f in all_files if f.suffix.lower() in IMAGE_EXTENSIONS]
    other_files = [f for f in all_files if f.suffix.lower() not in IMAGE_EXTENSIONS]

    # 表示項目のリストを構築
    display_items = dirs + other_files

    # 画像ファイルの要約処理
    if len(image_files) >= IMAGE_THRESHOLD:
        summary = f"🖼️ images x{len(image_files)}"
        display_items.append(summary)
    else:
        display_items.extend(image_files)

    # 最終的な表示順にソート
    display_items.sort(
        key=lambda x: (
            isinstance(x, str),  # ファイルとディレクトリが先
            str(x).lower() if isinstance(x, Path) else x
        )
    )
    
    # ツリー表示の生成
    for i, item in enumerate(display_items):
        is_last = (i == len(display_items) - 1)
        connector = "└── " if is_last else "├── "
        
        if isinstance(item, Path):
            if item.is_dir():
                print(f"{prefix}{connector}📁 {item.name}")
                new_prefix = prefix + ("    " if is_last else "│   ")
                tree_with_image_summary(item, new_prefix)
            else:
                print(f"{prefix}{connector}📄 {item.name}")
        else:  # 画像の要約文字列
            print(f"{prefix}{connector}{item}")


def main():
    """
    メイン関数
    """
    parser = argparse.ArgumentParser(
        description="Recursively list directory contents, summarizing image files and ignoring specified patterns."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="The directory path to start from. Defaults to the current directory.",
    )
    args = parser.parse_args()
    
    start_path = Path(args.path).resolve()
    if not start_path.is_dir():
        print(f"Error: '{start_path}' is not a valid directory.")
        return

    print(f"📁 {start_path.name}")
    tree_with_image_summary(start_path)

if __name__ == "__main__":
    main()
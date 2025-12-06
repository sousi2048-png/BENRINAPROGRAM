# BENRINAPROGRAM (便利なプログラム集)

このディレクトリには、日々の作業を効率化するための様々なユーティリティスクリプトが含まれています。

## 📋 含まれているプログラム一覧

| ファイル名 | 機能概要 | 言語 |
| :--- | :--- | :--- |
| `combine_images.py` | 複数の画像をランダムに選んでグリッド状に結合する | Python |
| `convert_to_jpg.py` | PNG画像をJPG形式に一括変換する | Python |
| `custom_tree.py` | 見やすいディレクトリツリーを表示する（画像要約機能付き） | Python |
| `fix_json_file.py` | JSONファイルの構文エラー（不正エスケープ等）を修正する | Python |
| `web_scraping.py` | 指定URLからWebページを再帰的にクローリングしてテキストを抽出する | Python |
| `text_ketugou.sh` | 複数のソースコードやテキストファイルを1つのファイルに結合する | Shell |
| `text_ketugou_R.sh` | サブディレクトリも含めてファイルを結合する（再帰版） | Shell |

---

## 🔧 各プログラムの詳細と使い方

### 1. 画像結合 (`combine_images.py`)
カレントディレクトリにある画像ファイルからランダムに画像を選び、1枚のグリッド画像（5x5など）として結合します。

**使い方:**
```bash
# デフォルト（5x5の25枚で作成）
python combine_images.py

# サイズを指定（例: 3列 x 4行）
python combine_images.py --cols 3 --rows 4

# 出力ファイル名を指定
python combine_images.py --output my_grid.jpg
```

### 2. png → jpg 一括変換 (`convert_to_jpg.py`)
指定したディレクトリ内の全てのPNGファイルをJPGファイルに変換します。透明部分は白背景になります。

**使い方:**
```bash
# 基本的な使用法
uv run convert_to_jpg.py /path/to/directory

# 変換後に元のPNGファイルを削除する場合
uv run convert_to_jpg.py /path/to/directory --delete
```

### 3. ディレクトリツリー表示 (`custom_tree.py`)
ディレクトリ構造をツリー形式で表示します。`.venv` などの不要なフォルダを除外したり、画像ファイルが大量にある場合は「images x10」のように要約して表示します。

**使い方:**
```bash
# カレントディレクトリを表示
python custom_tree.py

# 特定のディレクトリを表示
python custom_tree.py /path/to/directory
```

### 4. JSON修復 (`fix_json_file.py`)
破損した文字列エスケープ（`\`など）を含むJSONファイルを修正し、正しい形式で保存し直します。元のファイルは `.bak` としてバックアップされます。

**使い方:**
```bash
# data.json を修復する
uv run python fix_json_file.py data.json
```

### 5. Webスクレイピング (`web_scraping.py`)
指定したURL（ソースコード内で編集）からリンクを辿ってWebページを収集し、本文テキストを `crawled_content.txt` に保存します。

**使い方:**
スクリプト内の `start_urls` 変数を編集してから実行してください。
```bash
python web_scraping.py
```

### 6. ファイル結合 (`text_ketugou.sh` / `text_ketugou_R.sh`)
指定された拡張子（py, txt, md, sh 等）を持つファイルの中身をすべて抽出し、`combined_document.txt` という1つのファイルにまとめます。AIへのコンテキスト渡しなどに便利です。Wordファイル(`docx`)等は `pandoc` を使ってテキスト変換されます。

**使い方:**
```bash
# カレントディレクトリのみ対象
./text_ketugou.sh

# サブディレクトリも再帰的に含める場合
./text_ketugou_R.sh
```
※ 実行には `pandoc` が必要な場合があります (`docx`, `odt` 等を含む場合)。

---

## ⚠️ 必要要件
- Python 3.x
- Pandoc (シェルスクリプトでドキュメント変換を行う場合)
  - `sudo apt install pandoc`

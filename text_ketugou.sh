#!/bin/bash

# ==============================================================================
# 指定された拡張子のファイルからテキストを抽出し、一つのファイルに統合するスクリプト
# ==============================================================================

# 出力ファイル名を変数として定義する
OUTPUT_FILE="combined_document.txt"

# 依存コマンド 'pandoc' の存在を確認する
if ! command -v pandoc &> /dev/null; then
    echo "エラー: このスクリプトの実行には 'pandoc' が必須である。" >&2
    echo "'sudo apt update && sudo apt install pandoc' を実行してインストールせよ。" >&2
    exit 1
fi

# スクリプト実行時に既存の出力ファイルがあれば、その内容を空にする
> "${OUTPUT_FILE}"

echo "テキスト抽出処理を開始する..."

# 指定された拡張子リストに一致する全てのファイルに対してループ処理を実行する
for file in *.txt *.html *.xml *.md *.rtf *.docx *.odt *.py *.cpp *.java *.sh
do
  # ループ対象のファイルが存在し、かつ読み取り可能であるかを確認する
  # これにより、対象の拡張子を持つファイルが存在しない場合のエラーを抑制する
  if [ -f "${file}" ] && [ -r "${file}" ]; then
    
    echo "処理中: ${file}"

    # ===== 抽出元ファイル名の書き込み =====
    echo "==================== FILE: ${file} ====================" >> "${OUTPUT_FILE}"
    echo "" >> "${OUTPUT_FILE}"

    # ===== ファイル内容の抽出と書き込み =====
    # ファイルの拡張子を小文字で取得する
    extension="${file##*.}"
    extension_lower=$(echo "$extension" | tr '[:upper:]' '[:lower:]')

    # 拡張子に応じて処理を分岐させる
    case "${extension_lower}" in
      # --- プレーンテキストとして扱える形式 ---
      txt|html|xml|md|py|cpp|java|sh)
        cat "${file}" >> "${OUTPUT_FILE}"
        ;;

      # --- pandocによる変換が必要な形式 ---
      docx)
        pandoc --from docx --to plain "${file}" >> "${OUTPUT_FILE}"
        ;;
      odt)
        pandoc --from odt --to plain "${file}" >> "${OUTPUT_FILE}"
        ;;
      rtf)
        pandoc --from rtf --to plain "${file}" >> "${OUTPUT_FILE}"
        ;;
      
      # --- 予期せぬ拡張子のためのフォールバック ---
      *)
        echo "警告: 未定義の拡張子 (${extension}) のため、標準的なテキストとして処理を試みる。" >> "${OUTPUT_FILE}"
        cat "${file}" >> "${OUTPUT_FILE}"
        ;;
    esac

    # 各ファイルの内容の後に、区切りとして空行を挿入する
    echo -e "\n" >> "${OUTPUT_FILE}"

  fi
done

echo "全ての処理が完了した。出力ファイル: ${OUTPUT_FILE}"
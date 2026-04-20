#uv run python fix_json_file.py data.json

import json
import re
import sys
import shutil
from pathlib import Path

def fix_bad_escapes_in_json(json_str: str) -> str:
    r"""
    JSON文字列内の不正なエスケープを自動修正する。
    例: "C:\newfolder\data.txt" → "C:\\newfolder\\data.txt"
    """
    def fix_string_literal(s: str) -> str:
        # s は "..." を含む文字列リテラル
        content = s[1:-1]
        out = []
        i = 0
        hexdigits = set("0123456789abcdefABCDEF")
        while i < len(content):
            ch = content[i]
            if ch != "\\":
                out.append(ch)
                i += 1
                continue

            # バックスラッシュの処理
            if i + 1 >= len(content):
                # 末尾の単独バックスラッシュはエスケープ
                out.append("\\\\")
                i += 1
                continue

            nxt = content[i + 1]
            if nxt in "\"\\/bfnrt":
                out.append("\\" + nxt)
                i += 2
                continue
            if nxt == "u":
                hexpart = content[i + 2:i + 6]
                if len(hexpart) == 4 and all(c in hexdigits for c in hexpart):
                    out.append("\\u" + hexpart)
                    i += 6
                    continue
                # 不正な \u シーケンスはバックスラッシュをエスケープ
                out.append("\\\\")
                i += 1
                continue

            # それ以外は不正エスケープとしてバックスラッシュをエスケープ
            out.append("\\\\")
            i += 1

        return "\"" + "".join(out) + "\""

    # JSON内の文字列リテラルだけを対象に修正
    fixed_json_str = re.sub(r'\"(\\.|[^"\\])*\"', lambda m: fix_string_literal(m.group(0)), json_str)
    return fixed_json_str


def remove_citations(json_str: str) -> str:
    """
    JSON文字列内の[cite_start]と[cite: ...]をすべて削除する。
    例: "[cite: 12]" "[cite: 66, 76]" など。
    """
    # [cite_start] を削除
    cleaned = json_str.replace("[cite_start]", "")
    # [cite: ...] を削除（任意の内容を許容）
    cleaned = re.sub(r"\[cite:[^\]]*\]", "", cleaned)
    return cleaned


def fix_json_file(filepath: str, backup: bool = True):
    """
    指定したJSONファイル全体を自動修正して保存する。
    - 不正エスケープを修正
    - [cite_start]を削除
    - JSON構文を確認
    """
    path = Path(filepath)

    if not path.exists():
        print(f"ファイルが存在しない: {filepath}")
        sys.exit(1)

    # バックアップを作成
    if backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        shutil.copy(path, backup_path)
        print(f"バックアップを作成: {backup_path}")

    # ファイル内容を読み込み
    with open(path, "r", encoding="utf-8") as f:
        raw_data = f.read()

    # 処理ステップ
    fixed_data = remove_citations(raw_data)
    fixed_data = fix_bad_escapes_in_json(fixed_data)

    # JSON構文チェック
    try:
        json.loads(fixed_data)
    except json.JSONDecodeError as e:
        print("⚠ 修正後もJSONとして無効:", e)
        raise

    # 修正後のJSONを上書き保存
    with open(path, "w", encoding="utf-8") as f:
        f.write(fixed_data)

    print(f"✅ 修正完了: {path}")
    print("・不正なエスケープを修正")
    print("・[cite_start] を削除")
    print("・正しい形式のJSONとして保存した。")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python fix_json_file.py data.json")
        sys.exit(1)

    target_file = sys.argv[1]
    fix_json_file(target_file)

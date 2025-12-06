#実行するときは「uv run convert_to_jpg.py /home/haseg/Image_Segmentation/datasetcp --delete」と入力

import os
import argparse
from PIL import Image

def convert_png_to_jpg(directory_path, delete_original=False):
    """
    指定されたディレクトリ内のすべてのPNGファイルをJPGに変換する。
    PNGが持つ透過情報(アルファチャンネル)は白色の背景で塗りつぶされる。

    Args:
        directory_path (str): PNGファイルが含まれるディレクトリのパス。
        delete_original (bool): 変換成功後に元のPNGファイルを削除するかどうか。
    """
    if not os.path.isdir(directory_path):
        print(f"エラー: ディレクトリ '{directory_path}' が見つかりません。")
        return

    print(f"スキャン対象ディレクトリ: {directory_path}")

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".png"):
            png_path = os.path.join(directory_path, filename)
            
            try:
                with Image.open(png_path) as img:
                    jpg_filename = os.path.splitext(filename)[0] + ".jpg"
                    jpg_path = os.path.join(directory_path, jpg_filename)

                    if img.mode == 'RGBA':
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[3])
                        converted_img = background
                    else:
                        converted_img = img.convert('RGB')
                    
                    converted_img.save(jpg_path, "JPEG", quality=95)
                    print(f"変換完了: {filename} -> {jpg_filename}")

                if delete_original:
                    os.remove(png_path)
                    print(f"  => 元ファイルを削除: {filename}")

            except Exception as e:
                print(f"エラー: {filename} の変換中に問題が発生しました - {e}")

    print("\n処理が完了しました。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ディレクトリ内のすべてのPNGファイルをJPGファイルに一括変換するプログラム。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "directory",
        type=str,
        help="変換対象のPNGファイルが含まれるディレクトリのパス。"
    )
    
    parser.add_argument(
        "--delete",
        action="store_true",
        help="このフラグを指定すると、変換成功後に元のPNGファイルが削除されます。"
    )

    args = parser.parse_args()
    convert_png_to_jpg(args.directory, args.delete)
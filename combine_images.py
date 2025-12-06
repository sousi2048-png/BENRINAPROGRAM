#python combine_images.py　デフォルトは5×5
##python combine_images.py --cols 3 --rows 4 --output my_grid.jpg

import os
from PIL import Image
import sys
import random

def combine_images_grid(output_filename="combined_output.jpg", grid_size=(5, 5)):
    """
    カレントディレクトリ内の画像からランダムに25枚を選び、グリッド状に結合する関数

    Args:
        output_filename (str): 出力する画像ファイル名
        grid_size (tuple): グリッドのサイズ (列数, 行数)
    """
    # スクリプトのあるディレクトリを取得
    input_dir = os.path.dirname(os.path.abspath(__file__))

    # グリッドの列数と行数を取得
    cols, rows = grid_size
    num_images_required = cols * rows

    # 画像ファイルの一覧を取得
    try:
        all_image_files = [
            f for f in os.listdir(input_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and f != output_filename
        ]
    except FileNotFoundError:
        print(f"エラー: ディレクトリ '{input_dir}' が見つからない。")
        return

    # 画像枚数が要件を満たしているか確認
    if len(all_image_files) < num_images_required:
        print(f"エラー: {num_images_required}枚の画像が必要だが、{len(all_image_files)}枚しか見つからなかった。")
        return

    # ランダムに25枚の画像を選択
    images_to_process = random.sample(all_image_files, num_images_required)
    print(f"選択された画像: {images_to_process}")

    # 画像オブジェクトのリストを作成
    images = []
    try:
        for f in images_to_process:
            img = Image.open(os.path.join(input_dir, f))
            # サイズを統一するためにリサイズが必要かもしれないが、
            # 元のコードでは「全ての画像のサイズは等しいものと仮定」していたため、
            # ここではそのままにする。必要ならリサイズ処理を追加する。
            images.append(img)
    except Exception as e:
        print(f"エラー: 画像ファイルの読み込み中に問題が発生した: {e}")
        return

    # 基準となる画像のサイズを取得 (最初の画像)
    img_width, img_height = images[0].size
    
    # 画像サイズが一致していない場合のリサイズ処理（オプションとして追加、念のため）
    resized_images = []
    for img in images:
        if img.size != (img_width, img_height):
            # 最初の画像に合わせてリサイズ
            resized_images.append(img.resize((img_width, img_height)))
        else:
            resized_images.append(img)
    images = resized_images

    # 結合後の全体の画像サイズを計算
    total_width = img_width * cols
    total_height = img_height * rows

    # 新しい画像を作成 (キャンバス)
    combined_image = Image.new('RGB', (total_width, total_height))

    # 各画像をキャンバスに貼り付け
    for index, img in enumerate(images):
        col = index % cols
        row = index // cols
        x_offset = col * img_width
        y_offset = row * img_height
        combined_image.paste(img, (x_offset, y_offset))


    
    # 結合した画像を保存
    try:
        output_path = os.path.join(input_dir, output_filename)
        combined_image.save(output_path)
        print(f"画像の結合が完了した。出力ファイル: {output_path}")
    except Exception as e:
        print(f"エラー: 画像の保存中に問題が発生した: {e}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='ディレクトリ内のランダムな画像をグリッド状に結合します。')
    parser.add_argument('--cols', type=int, default=5, help='グリッドの列数 (デフォルト: 5)')
    parser.add_argument('--rows', type=int, default=5, help='グリッドの行数 (デフォルト: 5)')
    parser.add_argument('--output', type=str, default="random_grid_output.jpg", help='出力ファイル名 (デフォルト: random_grid_output.jpg)')

    args = parser.parse_args()

    combine_images_grid(output_filename=args.output, grid_size=(args.cols, args.rows))

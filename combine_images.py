#python combine_images.py /path/to/images

import os
from PIL import Image
import sys
import random

def combine_images_grid(output_filename="combined_output.jpg", grid_size=(5, 5), input_dir=None):
    """
    指定されたディレクトリ（デフォルトはカレント）内の画像から再帰的にランダムに25枚を選び、グリッド状に結合する関数

    Args:
        output_filename (str): 出力する画像ファイル名
        grid_size (tuple): グリッドのサイズ (列数, 行数)
        input_dir (str): 画像を検索するディレクトリへのパス。Noneの場合はスクリプトのあるディレクトリ。
    """
    # 検索対象ディレクトリの決定
    if input_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        base_dir = os.path.abspath(input_dir)

    # グリッドの列数と行数を取得
    cols, rows = grid_size
    num_images_required = cols * rows

    # 画像ファイルの一覧を再帰的に取得
    all_image_files = []
    try:
        if not os.path.exists(base_dir):
            print(f"エラー: ディレクトリ '{base_dir}' が見つからない。")
            return

        for root, dirs, files in os.walk(base_dir):
             for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and f != output_filename:
                    # フルパスで保存
                    all_image_files.append(os.path.join(root, f))
    except Exception as e:
        print(f"エラー: ファイル検索中に問題が発生した: {e}")
        return

    # 画像枚数が要件を満たしているか確認
    if len(all_image_files) < num_images_required:
        print(f"エラー: {num_images_required}枚の画像が必要だが、{len(all_image_files)}枚しか見つからなかった(検索パス: {base_dir})。")
        return

    # ランダムに25枚の画像を選択
    images_to_process = random.sample(all_image_files, num_images_required)
    print(f"選択された画像: {images_to_process}")

    # 画像オブジェクトのリストを作成
    images = []
    try:
        for file_path in images_to_process:
            # 配列にはフルパスが入っているためそのままopen
            img = Image.open(file_path)
            images.append(img)
    except Exception as e:
        print(f"エラー: 画像ファイルの読み込み中に問題が発生した: {e}")
        return

    # 基準となる画像のサイズを取得 (最初の画像)
    img_width, img_height = images[0].size
    
    # 画像サイズが一致していない場合のリサイズ処理
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
    # 出力パスが指定されている場合、そのディレクトリが存在することを確認
    try:
        # output_filenameが絶対パスの場合はそのまま使用
        # 相対パスの場合は実行時のカレントディレクトリを基準にする
        if os.path.isabs(output_filename):
            output_path = output_filename
        else:
            output_path = os.path.join(os.getcwd(), output_filename)
        
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        combined_image.save(output_path)
        print(f"画像の結合が完了した。出力ファイル: {output_path}")
    except Exception as e:
        print(f"エラー: 画像の保存中に問題が発生した: {e}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='指定ディレクトリ以下の画像を再帰的に検索し、ランダムにグリッド状に結合します。')
    parser.add_argument('input_dir', nargs='?', type=str, default=None, help='画像を検索するディレクトリ (デフォルト: カレントディレクトリ)')
    parser.add_argument('--cols', type=int, default=5, help='グリッドの列数 (デフォルト: 5)')
    parser.add_argument('--rows', type=int, default=5, help='グリッドの行数 (デフォルト: 5)')
    parser.add_argument('--output', type=str, default="combined_images/random_grid_output.jpg", help='出力ファイル名 (デフォルト: combined_images/random_grid_output.jpg)')

    args = parser.parse_args()

    combine_images_grid(output_filename=args.output, grid_size=(args.cols, args.rows), input_dir=args.input_dir)

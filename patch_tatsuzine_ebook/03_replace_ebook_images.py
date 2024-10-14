# 03_replace_ebook_images.py
#
# このスクリプトは、元のPDFファイルの画像を前処理済みの画像で置き換えます。
# 主な機能:
# 1. 前処理済み画像の読み込み
# 2. PDFファイルの各ページの画像を新しい画像で置換
# 3. 置換後のPDFを新しいファイルとして保存
#
# 使用方法:
# python 03_replace_ebook_images.py <入力PDFファイルパス>
#
# 出力:
# 入力PDFファイルと同じディレクトリに、ファイル名の先頭に「【カラー版】」を付加した新しいPDFファイルが作成されます。
#
# 必要なパッケージのインストール:
# pip install pikepdf Pillow

import sys
from collections import defaultdict
import io
from pathlib import Path
import os

from pikepdf import Pdf, PdfImage, Name, Stream
from PIL import Image, ImageEnhance

# コマンドライン引数から入力PDFファイルのパスを取得
if len(sys.argv) != 2:
    print("使用方法: python 03_replace_ebook_images.py <入力PDFファイルパス>")
    sys.exit(1)

input_pdf = Path(sys.argv[1])
output_pdf = input_pdf.parent / f"【カラー版】{input_pdf.name}"
script_dir = Path(__file__).parent
preprocessed_images_dir = script_dir / "preprocessed_images"
support_repo = Path(os.environ['USERPROFILE']) / "repo" / "cursor-perfect-guide"

PAGE_OFFSET = 13    # 紙面の 12 ページは pages[25] に当たる

# 画像の一時保存先ディレクトリを作成
preprocessed_images_dir.mkdir(exist_ok=True, parents=True)

# 加工済の画像のファイルパスを整理しておく
# screenshots[ページ番号][画像インデックス] = スクリーンショットのファイルパス
screenshots = defaultdict(dict)
screenshot_paths = preprocessed_images_dir.glob("*.png")
for screenshot_path in screenshot_paths:
    # "111_0.png", "p111_1.png" 等のファイルをページ番号でグループ化
    page, index = screenshot_path.stem.split("_")
    screenshots[int(page)][int(index)] = screenshot_path

# PDFファイルを開く
pdf = Pdf.open(input_pdf)

# 各ページの画像を置換
for page_num, screenshot_paths in screenshots.items():
    page = pdf.pages[PAGE_OFFSET + page_num]
    resources = page.get('/Resources', {})
    xobjects = resources.get('/XObject', {})

    image_items = page.images.items()
    if len(image_items) != len(screenshot_paths):
        print(f"page {page_num} has {len(image_items)} images, but {len(screenshot_paths)} screenshots")
        continue

    print(f"page {page_num} has {len(image_items)} images")
    # 画像の並び順を fitz での抽出順に合わせる
    image_items = sorted(image_items, key=lambda x: x[1].objgen)
    for image_index, (name, item) in enumerate(image_items):
        screenshot_path = screenshot_paths[image_index]
        pdf_image = PdfImage(item)

        # 新しい画像を読み込む
        with open(screenshot_path, 'rb') as img_file:
            # 画像を読み込み、アルファチャンネルを除去しておく
            image = Image.open(img_file).convert('RGB')

        # コントラストを上げる→P.126～で白飛びしたのでいったんコメントアウト
        # con = ImageEnhance.Contrast(image)
        # image2 = con.enhance(1.2)

        with io.BytesIO() as output:
            # 当初は PNG で埋め込もうとしたがうまくいかなかったので JPEG に変更しておく
            # image.save(output, format='PNG')
            image.save(output, format='JPEG', quality=95)
            img_data = output.getvalue()

        if (
           (pdf_image.width, pdf_image.height) != (image.width, image.height) and
           # 理由は不明だが、PDF に埋め込まれた画像のサイズは 2 ピクセル大きいものが多いので
           # その場合はサイズが一致しているとみなす
           (pdf_image.width-2, pdf_image.height-2) != (image.width, image.height)
        ):
            print(f"image size mismatch: {img_file.name} {pdf_image.width}x{pdf_image.height} -> {image.width}x{image.height}")

        # 画像データを新しいものに置き換える
        new_pdf_image = Stream(
            pdf,
            img_data,
            Type=Name.XObject,
            Subtype=Name.Image,
            Width=image.width,
            Height=image.height,
            ColorSpace=Name.DeviceRGB,
            BitsPerComponent=8,
            Filter=Name.DCTDecode,    # JPEG
            # Filter=Name.FlateDecode,    # PNG
        )

        # 置き換え
        xobjects[name] = new_pdf_image

# 新しいPDFを保存
pdf.save(output_pdf)

print(f"カラー版PDFを保存しました: {output_pdf}")

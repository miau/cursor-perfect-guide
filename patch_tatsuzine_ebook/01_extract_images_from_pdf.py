# 01_extract_images_from_pdf.py
#
# このスクリプトは、指定されたPDFファイルから画像を抽出し、
# 'extracted_images' ディレクトリに保存します。
# 各画像のファイル名は 'ページ番号_画像インデックス.拡張子' の形式で保存されます。
#
# 必要なパッケージのインストール:
# pip install PyMuPDF

import sys
from pathlib import Path
import fitz  # PyMuPDF

script_dir = Path(__file__).parent
output_dir = script_dir / "extracted_images"
PAGE_OFFSET = 13    # 紙面上の 12 ページは pages[25] に当たる

# PDFファイルからの画像抽出処理
def extract_images_from_pdf(pdf_path):
    output_dir.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        images = page.get_images(full=True)
        # 紙面上のページ数に変換しておく
        real_page_number = page_number - PAGE_OFFSET
        # 紙面上のページでない場合（表紙、最終ページ）はスキップ
        if not 1 <= real_page_number <= 273:
            continue
        for img_index, img in enumerate(images):
            # img は (xref, smask, width, height, bpc, colorspace, ...) のタプル
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            image_filename = f"{real_page_number}_{img_index}.{image_ext}"
            with open(output_dir / image_filename, "wb") as image_file:
                image_file.write(image_bytes)

# メイン処理
if __name__ == "__main__":
    # コマンドライン引数の検証
    if len(sys.argv) != 2:
        print("使用方法: python 01_extract_images_from_pdf.py <PDFファイル名>")
        sys.exit(1)
    
    input_pdf = Path(sys.argv[1])
    if not input_pdf.exists():
        print(f"エラー: ファイル '{input_pdf}' が見つかりません。")
        sys.exit(1)
    
    # 処理開始メッセージ
    print("画像抽出処理を開始します...")

    # PDF画像抽出の実行
    extract_images_from_pdf(input_pdf)

    # 処理終了メッセージ
    print("画像抽出処理が完了しました。")

# AIエディタCursor完全ガイド（達人出版会PDF）カラー版作成スクリプト

このリポジトリは、達人出版会で購入した『AIエディタCursor完全ガイド ―やりたいことを伝えるだけでできる新世代プログラミング―』のPDFに対して、サポートリポジトリのスクリーンショットを使って書籍中の画像をカラー版に差し換えるためのスクリプトを含んでいます。

## 使用方法

1. 必要なファイル：
   - 元のPDFファイル：「AIエディタCursor完全ガイド―やりたいことを伝えるだけでできる新世代プログラミング―-1.0.0.pdf」
   （注：本リポジトリはサポートリポジトリのForkであり、スクリーンショットは本リポジトリに含まれています）

2. スクリプトの実行順序：
   - `01_extract_images_from_pdf.py`: PDFから画像を抽出します。
   - `02_preprocess_images.py`: PDFから抽出した画像を使用して、サポートリポジトリのスクリーンショットから対応する部分を切り出します。
   - `03_replace_ebook_images.py`: 前処理したスクリーンショット画像をPDFに埋め込みます。

注意：このリポジトリには`02_preprocess_images.py`の出力結果が含まれているため、同一バージョンのPDFをお持ちの方は`03_replace_ebook_images.py`のみを実行すれば十分です。

3. 各スクリプトの実行方法

### 01_extract_images_from_pdf.py

```sh
pip install PyMuPDF
python 01_extract_images_from_pdf.py <元のPDFファイルパス>
```

### 02_preprocess_images.py

```sh
pip install opencv-python
python 02_preprocess_images.py
```

### 03_replace_ebook_images.py

```sh
pip install pikepdf Pillow
python 03_replace_ebook_images.py <元のPDFファイルパス>
```

## 補足事項

- このスクリプトは、購入したPDFの個人利用の範囲内でカラー版を作成することを目的としています。
- 作成したカラー版PDFの配布や公開は著作権法に抵触する可能性があるため、絶対に行わないでください。
- スクリプトの使用によって生じた問題や損害について、作者は一切の責任を負いません。

## 注意事項

- スクリプトを実行する前に、必ず元のPDFファイルのバックアップを取ってください。
- 使用するPDFのバージョンによっては、スクリプトが正常に動作しない可能性があります。

ご不明な点がありましたら、イシューを作成してお問い合わせください。

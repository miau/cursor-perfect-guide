# 02_preprocess_images.py

# このスクリプトは、PDFから抽出された画像とスクリーンショットを前処理します。
# 主な機能:
# 1. 特定のページの画像の修正や複製
# 2. 外部URLからの画像のダウンロード
# 3. テンプレートマッチングを使用して、PDFから抽出された画像に類似する領域をスクリーンショットから探して切り出し
# 4. 処理済み画像を 'preprocessed_images' ディレクトリに保存

# このスクリプトは、PDFから抽出された各画像に対して、対応するスクリーンショット内で
# 類似した領域を探し、その部分を切り出します。これにより、元の画像をカラーバージョンに
# 置き換えることができます。

# 必要なパッケージのインストール:
# pip install opencv-python

from pathlib import Path
import shutil
import urllib.request

import cv2
import numpy as np

script_dir = Path(__file__).parent
extracted_images_dir = script_dir / "extracted_images"
screenshots_dir = script_dir.parent / "screenshots"
preprocessed_images_dir = script_dir / "preprocessed_images"

preprocessed_images_dir.mkdir(exist_ok=True)

# 特定のページの画像修正や複製
# screenshots ディレクトリに適切なページ名で配置しておくことで該当ページのテンプレートマッチング対象となる
tmp_files = {
    "p112_3.png": "p114_tmp.png",   # ページ数の誤り
    "p232_2.png": "p234_tmp.png",  # p234 の稲妻アイコンがスクショのどこにも出現しないので p232 から持ってくる
    "p172_2.png": "p173_tmp.png",  # p173 の最初の図は p172 の画像に含まれる
    "p265_2.png": "p266_tmp.png",  # p266 の図は p265 として保存されている
    "p129.png": "p129_tmp.png",    # 特別な加工が必要なので処理前にコピーしておく
}
# テンプレートマッチング対象のスクショをコピーしておく
for src, dst in tmp_files.items():
    if (screenshots_dir / src).exists():
        shutil.copy2(screenshots_dir / src, screenshots_dir / dst)

# p129 の画像は中間部分が省略されて 1334x1265 -> 1336x715 のようにサイズが変わっている（？）
# 同じように加工したものを作っておく
if (screenshots_dir / "p129.png").exists():
    img = cv2.imread(screenshots_dir / "p129.png")
    # Discover Cursor の位置が 578 -> 415 に変わっている（164 削ればよい）
    img = np.vstack([img[:400], img[400+164:]])
    # 残り 388 削って 1334x713 にしておく
    img = np.vstack([img[:500], img[500+388:]])
    cv2.imwrite(screenshots_dir / "p129_tmp.png", img)

# P.2 のスクリーンショットは元 URL から取得しておく
url = "https://research-assets.cbinsights.com/2023/02/23153811/OpenAI_investmentthesismap_022323V3-1010x1024.png"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as res:
    body = res.read()
    (preprocessed_images_dir / "2_0.png").write_bytes(body)

# テンプレートマッチングを使用して画像を切り出し
for ext_image_path in extracted_images_dir.glob("*"):
    # 特定のページをデバッグする場合にアンコメント
    # if not ext_image_path.name.startswith("149_"):
    #     continue
    print(ext_image_path.name)
    img_template = cv2.imread(str(ext_image_path), cv2.IMREAD_GRAYSCALE)
    assert img_template is not None, "file could not be read, check with os.path.exists()"
    h, w = img_template.shape
    page_num = int(ext_image_path.stem.split("_")[0])
    screenshot_images = (
        list(screenshots_dir.glob(f"p{page_num}.png")) + 
        list(screenshots_dir.glob(f"p{page_num}_*.png"))
    )
    if not screenshot_images:
        print("  no screenshot images, skipped.")
        continue
    print("  candidates:", ", ".join(p.name for p in screenshot_images))
    best_img = img_template
    best_max_val = -1
    best_screenshot = None
    best_loc = None
    for screenshot_image in screenshot_images:
        try:
            img_color = cv2.imread(str(screenshot_image), cv2.IMREAD_COLOR)
            img_gray = cv2.imread(str(screenshot_image), cv2.IMREAD_GRAYSCALE)
            # スクリーンショットよりも大きくなっている画像があるのでエラーにならないよう広げておく
            img_color = cv2.copyMakeBorder(img_color, 2, 2, 2, 2, cv2.BORDER_REPLICATE)
            img_gray = cv2.copyMakeBorder(img_gray, 2, 2, 2, 2, cv2.BORDER_REPLICATE)
            h2, w2 = img_gray.shape
            # print(w, h, w2, h2)
            if h2 < h or w2 < w:
                # 小さいファイルに対するマッチングは誤判定されるのでスキップ
                # print("small screenshot, skipping")
                continue
            for img in [img_gray, 255 - img_gray]:  # そのままマッチング＆反転してマッチングを試す
                res = cv2.matchTemplate(img, img_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > best_max_val:
                    # 通常のケース
                    x, y = max_loc
                    best_img = img_color[y:y+h, x:x+w]
                    best_max_val = max_val
                    best_screenshot = screenshot_image.name
                    best_loc = x, y
                    # print(f"Best: {best_screenshot} {best_loc} {best_max_val}")
        except Exception as e:
            print(f"Skipping {screenshot_image.name}, {e}")
    cv2.imwrite((preprocessed_images_dir / ext_image_path.name).with_suffix(".png"), best_img)
    # print(f"Best: {best_screenshot} {best_loc}")

# 自動で切り出した画像を上書き

# p181 とスクショは他と違って縮小画像が埋め込まれている（1472x1373 -> 829x596）
# 上記のロジックでは一部の領域が切り出されてしまうので、
# 縦横比を保ったまま縦を 596 * 1472 / 829 = 1058 に切りつめた画像で上書きする
if (screenshots_dir / "p181.png").exists():
    img = cv2.imread(screenshots_dir / "p181.png")
    img = img[:1058]
    cv2.imwrite(preprocessed_images_dir / "181_0.png", img)

# スクリーンショット用にコピーした画像は削除しておく
for src in tmp_files.values():
    if (screenshots_dir / src).exists():
        (screenshots_dir / src).unlink()

# 「AIエディタCursor完全ガイド」 サポートリポジトリ

## 📕 このGitHubリポジトリについて

書籍「AIエディタCursor完全ガイド」 について下記のサポートを行うリポジトリです。

- 書籍に掲載されているハンズオン用コード、生成されたサンプルコード、プロンプト、スクリーンショット画像の公開。
- 原稿を書き上げた後の Cursor のアップデートによる変更点の補足説明。

まだお持ちでない方は、ぜひお買い求めください！

[![AIエディタCursor完全ガイド](images/cover_cursor_boook.jpg)](https://amzn.to/4c2tjdt)

## 🌟 アップデート情報 🌟

| 日付       | 更新内容                                                                                                                                                                   |
| 日付       | 更新内容                                                                                                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2024/09/04 | 書籍発売日に備えた初版リリース。                                                                                                                                           |
| 2024/09/05 | 「第6章 Cursor開発テクニック」 Composer Projects の説明を追加。                                                                                                            |
| 2024/09/06 | 「第4章 Cursorのカスタマイズ設定」 Composer、Chat の設定事項を追記。「第3章 Cursorの機能説明」 参照情報の表示変更の説明を追加。正誤表更新。                                |
| 2024/09/08 | チャットモードのプルダウンが表示されない場合についての対策と説明を追記。                                                                                                   |
| 2024/09/09 | 「第5章 プロンプト・プログラミング実践例」掲載データを追加。                                                                                                               |
| 2024/09/10 | 「Debug with AI」が日本語で回答するようになった点の反映。                                                                                                                  |
| 2024/09/12 | 第2章、第3章のスクリーンショット画像を掲載。                                                                                                                               |
| 2024/09/13 | 第4章、第5章、第6章のスクリーンショット画像を掲載。                                                                                                                        |
| 2024/09/21 | 追補 Composer の内容を 0.41 に対応。AI 内ペイン表示、コントロールパネルのウィンドウ化、0.41 その他の変更点の説明を追記。                                                   |
| 2024/09/22 | 第4章に Cursor Tab の設定説明を追記。Composer 設定説明のアップデート。                                                                                                     |
| 2024/09/25 | o1-mini の利用上限についての記載を追加（第1章、本ページ）。                                                                                                                |
| 2024/10/11 | 0.42 に対応。変更事項については [Cursorの変更履歴ページ](https://changelog.cursor.com/?nightly=true#042---composer-history-lint-errors-vs-code-1931-) を参照してください。 |
| 2024/10/13 | 0.42 での Composer 設定の変更に対応。                                                                                                                                      |

## 📕 このリポジトリの構成

各章のハンズオン用コード、サンプルコード、プロンプトなどは章ごとにまとめてあります。各章のリンクから該当章に移動して、内容をご覧ください。

### 📘 第1章 Cursor の導入

#### 📗 Cursor の概要（P2）

本書内では OpenAI などからの Anysphere 社への出資の紹介をしていますが、2024年8月22日に、Stripe、Github、Ramp、Perplexity、OpenAI の創設者などから、さらに6000万ドル（約88億円）の出資があったことが公式にアナウンスされました。心強いニュースですね。
- [We Raised $60M](https://www.cursor.com/blog/series-a)

#### 📗 Cursorの料金体系（P3）

- 「高速 GTP-4」という呼び方から「高速プレミアムモデル」に変更になっています。
- 「高速プレミアムモデル」には下記モデルが含まれます。
    1. GPT-4
    2. GPT-4o
    3. Claude 3.5 Sonnet
- [料金ページ](https://www.cursor.com/pricing)には記載されていませんが、GPT-4o mini は料金体系上 cursor-small と同じ扱い（Pro 以上は回数制限なし）になっています（コストパフォーマンスが良いので、活用の価値が高い）。
- [Pro 料金プラン](https://www.cursor.com/pricing)に「10 o1-mini uses per day」と明記されました。o1-mini モデルは10リクエスト/日が利用上限となります。

### 📘 第2章 Cursor の基本操作

[🔗 スクリーンショット](chapter2/SCREENSHOT.md)

[🔗 プロンプト](chapter2/PROMPT.md)

[🔗 「cursor-tutor」リポジトリ](https://github.com/kinopeee/cursor-tutor/)

- 2024年6月以前に Cursor をインストールされた方は、書籍の手順通りで操作を進めていただくことができます。
- ローカルに「.cursor-tutor」フォルダがない場合は、「cursor-tutor」リポジトリをダウンロードしてご利用ください。

### 📘 第3章 Cursor の基本操作

[🔗 スクリーンショット](chapter3/SCREENSHOT.md)

[🔗 補足説明](chapter3/README.md)

### 📘 第4章 Cursorのカスタマイズ設定

[🔗 スクリーンショット](chapter4/SCREENSHOT.md)

[🔗 補足説明](chapter4/README.md)

### 📘 第5章 プロンプト・プログラミング実践例

スクリーンショット  
[🔗 5.1〜5.10](chapter5/SCREENSHOT1.md)   
[🔗 5.11〜5.14](chapter5/SCREENSHOT2.md)  
[🔗 5.15〜5.16](chapter5/SCREENSHOT3.md)

[🔗 補足説明 / サンプルコード](chapter5/README.md)

[🔗 プロンプト](chapter5/PROMPT.md)

### 📘 第6章 Cursor開発テクニック

[🔗 スクリーンショット](chapter6/SCREENSHOT.md)

[🔗 補足説明](chapter6/README.md)

## 📕 誤植などのお知らせ

こちらの[正誤表](errata.md)を随時更新します。

## 📕 エラー等を見つけた際は

本リポジトリの [Issues](https://github.com/kinopeee/cursor-perfect-guide/issues) にご報告ください。ベストエフォートで対応いたします。

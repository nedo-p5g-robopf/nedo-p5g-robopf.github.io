# 検証手順

## この環境での実施結果

- Ruby 3.3.12・Jekyll 4.4.1で20ページのビルドに成功。
- 全内部リンク・ページ内アンカーと19件のサイトマップを検証。
- `/test-project` をbaseurlに指定した別ビルドでも、リンク検証に成功。
- 固定済み依存関係の再インストールと再ビルドに成功。
- 以下のブラウザー検証をChromiumで実行し、全項目が成功。
- axe-core 4.10.3の自動チェックは、主要5ページ種別・デスクトップ／モバイルの10ケースで違反なし。
- デスクトップとモバイルのスクリーンショットを目視確認。

外部ソフトウェアそのものの動作検証、GitHubへのpush、GitHub Actions上のビルド・公開は、このサイト制作の検証には含めていません。

## ビルドとリンク検証（CIでも実行）

```bash
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 scripts/check_site.py _site
```

サブディレクトリでの運用を確認する場合:

```bash
bundle exec jekyll build --baseurl /test-project --destination /tmp/nedo-baseurl-check
python3 scripts/check_site.py /tmp/nedo-baseurl-check /test-project
```

## ブラウザー検証

Pythonの `playwright` パッケージとChromiumを用意し、Jekyllサーバーを起動した状態で実行します。

```bash
python3 scripts/browser_smoke.py --url http://127.0.0.1:4000 --browser /usr/bin/chromium
```

このクラウド環境では、PlaywrightとChromiumは利用可能です。一般の環境ではPython仮想環境に `playwright` をインストールし、`python -m playwright install chromium` でブラウザーを用意できます。その場合は `--browser` の指定を省略してください。

`axe-core` を使った自動アクセシビリティ検証も実行する場合:

```bash
python3 scripts/browser_smoke.py --axe /workspace/site-tools/audit/node_modules/axe-core/axe.min.js
```

検証内容:

- 工程別・キーワード・公開リポジトリによる絞り込み
- 全角文字・機関名検索、0件表示、リセット
- URLからの状態復元、ブラウザーの戻る操作
- 1440・768・390・320px幅のレイアウト
- モバイルメニューとEscapeキー、フォーカス、参画機関への移動
- JavaScriptを無効にした状態でのナビゲーションと成果詳細への移動
- ブラウザーのスクリプトエラー・HTTPエラー
- axe-core指定時: 主要5種類のページでWCAG 2 A/AA・2.1 AAの自動チェック

スクリーンショットは `test-results/` に保存されます。自動チェックはアクセシビリティへの完全な適合を保証するものではありません。GitHub Actionsの公開ジョブそのものは、リモートへのpush後に確認してください。

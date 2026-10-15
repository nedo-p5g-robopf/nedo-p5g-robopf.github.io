# ロボティクスソフトウェア開発基盤

NEDO P5G ロボットプラットフォームPJ Webページ。

NEDO ポスト5G事業のロボティクスソフトウェア開発基盤を紹介するJekyllサイトです。プロジェクトページでは産総研・川崎重工業・竹中工務店の3つのコンソの取組と参画機関を紹介し、成果一覧では産総研コンソの16の開発項目を掲載しています。

## ローカル開発

Rubyのバージョンは `.ruby-version`、依存関係は `Gemfile.lock` に固定しています。

```bash
cd nedo-p5g-robopf.github.io
bundle config set --local path vendor/bundle
BUNDLE_FROZEN=true bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

このクラウド環境ではRubyを `/workspace/site-tools` に用意しています。上記コマンドの前に `export PATH=/workspace/site-tools/bin:$PATH` を実行してください。新しい開発環境ではRuby 3.3.12とBundlerをインストールしてください。

## ビルド・検証

```bash
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 scripts/check_site.py _site
```

リンク先ファイル・ページ内アンカー、見出し、サイトマップを生成後のHTMLに対して検証します。ブラウザーでの追加検証は [検証手順](docs/validation.md) を参照してください。

## GitHub Pagesへの公開

1. このサイトのファイルを対象リポジトリの `main` にコミット・pushします。
2. GitHubの **Settings → Pages → Build and deployment → Source** で **GitHub Actions** を選びます。
3. **Actions** の **Build and deploy Jekyll to GitHub Pages** を実行します。以降は `main` へのpush時に自動ビルド・公開されます。

公開URLは `https://nedo-p5g-robopf.github.io/` です。公開設定とビルド・デプロイが正常に完了すると、このURLで閲覧できます。ワークフローの実行結果はGitHub Actionsで確認してください。

プロジェクトサイトのサブパスに配置する場合は、`_config.yml` の `url`・`baseurl` を変更してください。内部リンク・静的アセットは `relative_url` フィルターに対応しています。

## 編集する場所

| 内容 | ファイル |
| --- | --- |
| トップページ | `index.html` |
| プロジェクト紹介 | `project/index.html` |
| 研究成果一覧 | `research/index.html` |
| 各成果の内容・公開先 | `_research/*.md` |
| コンソの取組 | `_data/consortia.yml` |
| 参画機関・所属コンソ | `_data/members.yml` |
| 工程別の分類 | `_data/stages.yml` |
| 配色・レイアウト | `assets/css/site.css` |
| 絞り込み・メニュー | `assets/js/site.js` |
| サイト名・公開URL | `_config.yml` |

各成果のMarkdownの `resource_url` に公開先を設定すると、一覧の公開ラベルと詳細ページのボタンが表示されます。公開先がない場合は、技術紹介ページとして表示します。`number` は文字列の通し番号、`stages` は `design`・`develop`・`verify`・`deploy` の配列です。新しい成果を追加するときはトップページの開発項目数と紹介文も合わせて更新してください。

検索はブラウザー内だけで動作し、検索語は外部に送信されません。検索条件はURLに保存され、共有できます。外部フォント・解析サービス・Cookie・問い合わせフォームは使用していません。

## コンテンツの更新

[コンテンツの編集ガイド](docs/content-sources.md) を参照してください。

# no05 — Docker Sandboxes⑤: 雲の檻で作らせて、閉じてもスマホで開く

Docker Cloud Sandboxes（`sbx --cloud`）の中の Claude Code に、旅行のしおりサイトを作らせ、公開 URL を発行し、Mac の蓋を閉じてからスマホで開くまでの手順です。このディレクトリには、動画で Claude に頼んだ依頼文の全文があります。

- [`prompt_prep.txt`](prompt_prep.txt) — 準備中ページを置いて配信させる依頼（最初に頼む）
- [`prompt_main.txt`](prompt_main.txt) — 本番（6ページのしおりサイト）の依頼

## 前提

- Docker Agentic Platform に申し込み済み（月額の購読料は無い従量制ですが、申し込みにカードの登録が要ります）
- `sbx` 0.45.0 以降（公式の要件）。うちで試した版は v0.48.0
- 試した日: 2026-10-15

手元の sandbox と cloud sandbox は別物です。手元で預けた鍵は cloud では使えません。

## 手順

1. サインインして、申し込みが有効か確かめる。`diagnose` が全項目通ることを確かめてから進む

   ```bash
   sbx login
   sbx --cloud diagnose
   ```

2. Claude の資格情報を cloud に預ける

   ```bash
   sbx --cloud secret set anthropic --oauth
   sbx --cloud secret ls
   ```

   出た URL をブラウザで開き、Claude にサインインして承認します。

   **リスクの注記:** 公式の手引きは、Claude Code には Anthropic の API キー（`sbx --cloud secret set anthropic`）を案内しています。うちでは API キーだと対話の画面で `Credit balance too low` で止まったため、`--oauth` で動かしました。`--oauth` は自分の Claude アカウントのトークンを Docker の cloud に、アカウント全体（global）の範囲で預ける方式です。規約の扱いとモデル代の数えられ方は自分で判断してください。使い終わったら必ず `secret rm` で消します（片付け）。

3. cloud sandbox で Claude Code を起こす（手元のフォルダは渡しません）

   ```bash
   sbx --cloud run claude --name shiori-trial
   ```

   入力欄が出たら、`prompt_prep.txt` を貼って送ります。

4. 別の端末で、公開 URL を発行する

   ```bash
   sbx --cloud ports shiori-trial --publish 8080
   ```

   `Port 8080 exposed at https://...` と URL が出ます。この URL には認証がかかりません。知っていれば誰でも開けるので、見せたくない物は置かないでください。

5. 入力欄に戻り、`prompt_main.txt` を貼って送る
6. 送ったらすぐ `Ctrl+\` を押して画面を切り離す（`detached; still running` と出れば、cloud 側の Claude は作業を続けています。戻るときは `sbx --cloud attach shiori-trial`）
7. Mac の蓋を閉じる
8. Wi-Fi を切ったスマホ（携帯回線）で、手順4の URL を開く。表紙が出ればできあがりです

起動画面の下の欄に `bypass permissions on` と出て、許可の確認なしで何でも実行されます。中には消えて困る物や秘密を置かないでください。

## 片付け

期限（既定1時間・最長24時間）には頼らず、自分で止めます。

```bash
sbx --cloud ports shiori-trial --unpublish 8080
sbx --cloud stop shiori-trial
sbx --cloud ls
```

`ls` で `stopped` になったのを確かめてから消します（止まりきる前の `rm` は失敗します）。`rm` は確認を求められるので手で答えます。

```bash
sbx --cloud rm shiori-trial
sbx --cloud secret rm anthropic -f
sbx --cloud ls
sbx --cloud secret ls
```

最後の2つが `No sandboxes found`・`No secrets found` になれば完了です。

## 料金と期限の注意

- 計算料は動いている時間に秒課金です（既定の Small で1時間あたり約 $0.14、2026年9月時点）。止めている間はかかりません
- モデルの料金は含まれず、提供元が別に請求します
- 期限が来ても止まらないことがありました（うちでは、つないで使っていた sandbox が期限を25分ほど過ぎても動いていました）。使い終わったら自分で `stop` → `rm` します

## 実測の時点

- 撮影: 2026-10-15、sbx v0.48.0、cloud sandbox 内の Claude Code 2.1.300（macOS）
- 手順は公式 docs（https://docs.docker.com/ai/sandboxes/cloud/）に従っています。版によって表記が変わることがあります

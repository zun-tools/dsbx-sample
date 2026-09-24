# no04 — 檻の中を、いつものエディタで直すのだ

`app.py` は Python の標準ライブラリだけで1ページ返すアプリです。リクエストのたびに自分のファイルを読み直すので、**保存してブラウザを再読み込みするだけ**で見出しが変わります。`0.0.0.0` の 3000 番で待ち受けます。

## 手順（動画と同じ）

前提: Docker Sandboxes の `sbx` が入っていて、ログイン済み。このフォルダで檻を作る。

```bash
sbx create --name demo shell .      # このフォルダで
sbx setup ssh                       # 一度だけ
```

1. VS Code の **Remote-SSH: Connect to Host...** で `demo.sbx` を手で入力（一覧には出ません）
2. VS Code のターミナル（檻の中）で `python3 app.py`
3. 手元の端末で `sbx ports demo --publish 8080:3000` → ブラウザで `http://127.0.0.1:8080`
4. `app.py` の `TITLE = "..."` を直して保存 → ブラウザを再読み込み

閉じ方: `sbx ports demo --unpublish 8080:3000`

### 初回の接続で止まったら

VS Code server の取り寄せが既定の拒否で止まることがあります（うちの環境では 2026-09-24 に止まりました）。

```bash
sbx policy log                                       # 止まった宛先を見る
sbx policy allow network --sandbox demo <ドメイン>   # --sandbox が無いと全部の檻に効きます
```

そのあと VS Code で **Developer: Reload Window**。

### エージェントに直させる（動画の2周目）

先に `demo` の公開を外し、Claude Code 入りの檻で同じ手順を踏みます。

```bash
sbx ports demo --unpublish 8080:3000
sbx create --name demo2 claude .
sbx ports demo2 --publish 8080:3000
```

`demo2.sbx` に VS Code でつなぎ、ターミナルで `claude` に「app.py の見出しを "Edited by the agent" に変えて」と頼む → ブラウザを再読み込み。

## 実測の時点

- 撮影: 2026-09-24、sbx v0.42.1、VS Code 1.137.0、Claude Code 2.1.280（macOS）
- 最新の sbx は v0.45.1（2026-09-22）。公開の既定が tcp4 になったので `http://localhost:8080` でも開きます（v0.42.0〜）
- 手順は公式 docs（https://docs.docker.com/ai/sandboxes/）に従っています。版によって表記が変わることがあります

# 見出しはリクエストごとに読み直す（保存 → 再読み込みだけで反映される）
from http.server import BaseHTTPRequestHandler, HTTPServer

TITLE = "Hello from the sandbox"


def page():
    # リクエストのたびにこのファイル自身を読み直して TITLE を取り出す
    src = open(__file__, encoding="utf-8").read()
    title = src.split('TITLE = "', 1)[1].split('"', 1)[0]
    return f"""<!doctype html><meta charset="utf-8"><title>{title}</title>
<body style="font-family:sans-serif;background:#f7f3ea;color:#222;margin:0;padding:80px">
<h1 style="font-size:72px;margin:0">{title}</h1>
<p style="font-size:28px">served from the sandbox : app.py</p></body>"""


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = page().encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 3000), H).serve_forever()

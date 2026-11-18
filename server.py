from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os, time

players = {}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Sonic Server is Live!")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length).decode("utf-8"))
        now = time.time()
        u = data.get("u", "")
        if u:
            players[u] = {"data": data, "t": now}
        for k in list(players.keys()):
            if now - players[k]["t"] > 5:
                del players[k]
        others = {k: v["data"] for k, v in players.items() if k != u}
        resp = json.dumps({"players": others}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, *args):
        pass

port = int(os.environ.get("PORT", 8080))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()

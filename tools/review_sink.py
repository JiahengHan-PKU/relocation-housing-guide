"""Receive reviews posted from the browser and save them locally."""

import json
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

HEADERS = {"Access-Control-Allow-Origin": "*",
           "Access-Control-Allow-Methods": "POST, OPTIONS",
           "Access-Control-Allow-Headers": "Content-Type",
           "Access-Control-Allow-Private-Network": "true"}


def review_sink(out_dir, port=8765):
    """Serve POST /reviews/<id> on 127.0.0.1 and write <id>.jsonl files.

    Args:
        out_dir: Folder for the review files.
        port: Local port to listen on.
    """
    class Handler(BaseHTTPRequestHandler):
        def _reply(self, code, body=b""):
            self.send_response(code)
            for key, value in HEADERS.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self):
            self._reply(204)

        def do_POST(self):
            match = re.fullmatch(r"/reviews/([a-z0-9-]+)", self.path)
            if not match:
                return self._reply(404)
            body = self.rfile.read(int(self.headers["Content-Length"]))
            reviews = json.loads(body)
            with open(f"{out_dir}/{match.group(1)}.jsonl", "w") as handle:
                for review in reviews:
                    handle.write(json.dumps(review, ensure_ascii=False) + "\n")
            print(match.group(1), len(reviews), flush=True)
            self._reply(200, str(len(reviews)).encode())

    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    review_sink(sys.argv[1])

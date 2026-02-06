from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

notes = [
    {"id": 1, "text": "hello world"},
    {"id": 2, "text": "python api"}
]

class API(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        keyword = query.get("search", [""])[0].lower()

        result = [n for n in notes if keyword in n["text"].lower()]

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

HTTPServer(("localhost", 8000), API).serve_forever()
# GET http://localhost:8000/notes?search=hello
# [
#   {"id": 1, "text": "hello world"}
# ]

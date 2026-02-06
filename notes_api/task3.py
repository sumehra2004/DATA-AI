from http.server import BaseHTTPRequestHandler, HTTPServer
import json

notes = [
    {"id": 1, "text": "hello"},
    {"id": 2, "text": "world"}
]

class API(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/notes":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(notes).encode())
        else:
            self.send_error(404)

HTTPServer(("localhost", 8000), API).serve_forever()
# GET http://localhost:8000/notes
# output :
# [
#   {"id": 1, "text": "hello"},
#   {"id": 2, "text": "world"}
# ]

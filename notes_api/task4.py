from http.server import BaseHTTPRequestHandler, HTTPServer
import json

notes = [
    {"id": 1, "text": "hello"},
    {"id": 2, "text": "world"}
]

class API(BaseHTTPRequestHandler):

    def do_GET(self):
        parts = self.path.strip("/").split("/")

        if len(parts) != 2 or parts[0] != "notes":
            self.send_error(404)
            return

        if not parts[1].isdigit():
            self.send_error(400, "Invalid ID")
            return

        note_id = int(parts[1])

        for note in notes:
            if note["id"] == note_id:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(note).encode())
                return

        self.send_error(404, "Not found")

HTTPServer(("localhost", 8000), API).serve_forever()
# GET http://localhost:8000/notes/1
#  output :{
#   "id": 1,
#   "text": "hello"
# }

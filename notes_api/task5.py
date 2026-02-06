from http.server import BaseHTTPRequestHandler, HTTPServer
import json

notes = [{"id": 1, "text": "hello"}]

class API(BaseHTTPRequestHandler):

    def do_PUT(self):
        parts = self.path.strip("/").split("/")

        if len(parts) != 2 or parts[0] != "notes":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))

        for note in notes:
            if note["id"] == int(parts[1]):
                note["text"] = data["text"]
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(note).encode())
                return

        self.send_error(404)

HTTPServer(("localhost", 8000), API).serve_forever()
# PUT http://localhost:8000/notes/1
# {
#   "id": 1,
#   "text": "updated"
# }

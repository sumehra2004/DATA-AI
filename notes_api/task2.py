from http.server import BaseHTTPRequestHandler, HTTPServer
import json

notes = []  # store notes in memory

class API(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/notes":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))

        # Validation
        if "text" not in data:
            self.send_error(400, "Text missing")
            return

        note = {
            "id": len(notes) + 1,
            "text": data["text"]
        }
        notes.append(note)

        self.send_response(201)  # Created
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(note).encode())

HTTPServer(("localhost", 8000), API).serve_forever()
# POST http://localhost:8000/notes
# {
#   "id": 1,
#   "text": "hello"
# }

from http.server import BaseHTTPRequestHandler, HTTPServer

notes = [{"id": 1, "text": "hello"}]

class API(BaseHTTPRequestHandler):

    def do_DELETE(self):
        parts = self.path.strip("/").split("/")

        for i, note in enumerate(notes):
            if str(note["id"]) == parts[1]:
                notes.pop(i)
                self.send_response(204)  # No Content
                self.end_headers()
                return

        self.send_error(404)

HTTPServer(("localhost", 8000), API).serve_forever()
# DELETE http://localhost:8000/notes/1
# (No Content – 204)

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

API_KEY = "mykey123"

class API(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):

        # Allow only /secret
        if self.path != "/secret":
            self.send_json(404, {"error": "Route not found"})
            return

        # Check API Key
        if self.headers.get("X-API-Key") != API_KEY:
            self.send_json(401, {"error": "Unauthorized"})
            return

        # Authorized access
        self.send_json(200, {"secret": "data"})


HTTPServer(("localhost", 8000), API).serve_forever()

# GET http://localhost:8000/secret
# output:{
#   "secret": "data"
# }
# | Key       | Value    |
# | --------- | -------- |
# | X-API-Key | mykey123 |


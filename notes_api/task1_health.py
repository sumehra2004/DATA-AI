# Health Check API
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class API(BaseHTTPRequestHandler):

    # Handle GET request
    def do_GET(self):
        # Only allow /health
        if self.path == "/health":
            self.send_response(200)  # HTTP 200 OK
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            # JSON response
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_error(404)  # Route not found

# Start server
HTTPServer(("localhost", 8000), API).serve_forever()
# http://localhost:8000/health
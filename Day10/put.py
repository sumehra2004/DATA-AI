# task6_put_users_fixed.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
    {
        "id": 6,
        "name": "Frank" 
    }
    
]


class API(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_PUT(self):
        parts = self.path.strip("/").split("/")

        # Validate route
        if len(parts) != 2 or parts[0] != "users":
            self.send_json(404, {"error": "Route not found"})
            return

        # Validate ID
        if not parts[1].isdigit():
            self.send_json(400, {"error": "Invalid user id"})
            return

        user_id = int(parts[1])

        # Validate body length
        length = self.headers.get("Content-Length")
        if not length:
            self.send_json(400, {"error": "Missing request body"})
            return

        try:
            data = json.loads(self.rfile.read(int(length)))
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
            return

        # Validate payload
        if "name" not in data or not data["name"]:
            self.send_json(400, {"error": "`name` is required"})
            return

        # Update user
        for user in users:
            if user["id"] == user_id:
                user["name"] = data["name"]
                self.send_json(200, user)
                return

        self.send_json(404, {"error": "User not found"})


HTTPServer(("localhost", 8000), API).serve_forever()
# http://localhost:8000/users/1
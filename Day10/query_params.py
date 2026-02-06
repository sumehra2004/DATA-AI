from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

HOST = "localhost"
PORT = 8000


ROUTES = {
    ("GET", "/users"): "get_users",
}


class SimpleAPI(BaseHTTPRequestHandler):

    # -------- Helpers --------
    def send_json(self, status=200, data=None):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    def get_query_params(self):
        parsed_url = urlparse(self.path)
        return parse_qs(parsed_url.query)

    # -------- Router --------
    def handle_route(self):
        parsed_url = urlparse(self.path)
        route = (self.command, parsed_url.path)

        handler_name = ROUTES.get(route)
        if not handler_name:
            self.send_json(404, {"error": "Route not found"})
            return

        handler = getattr(self, handler_name)
        handler()

    # -------- HTTP methods --------
    def do_GET(self):
        self.handle_route()

    # -------- Controller --------
    def get_users(self):
        params = self.get_query_params()

        # Defaults
        page = int(params.get("page", [1])[0])
        limit = int(params.get("limit", [10])[0])
        search = params.get("search", [None])[0]

        users = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
            {"id": 4, "name": "David"},
        ]

        # Search filter
        if search:
            users = [u for u in users if search.lower() in u["name"].lower()]

        # Pagination
        start = (page - 1) * limit
        end = start + limit
        paginated = users[start:end]

        self.send_json(200, {
            "page": page,
            "limit": limit,
            "total": len(users),
            "data": paginated
        })


def run():
    server = HTTPServer((HOST, PORT), SimpleAPI)
    print(f"Server running on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
'''
Pagination
curl "http://localhost:8000/users?page=2&limit=2"


Search
curl "http://localhost:8000/users?search=al"


Multiple values
curl "http://localhost:8000/users?role=admin&role=user"

'''
from http.server import BaseHTTPRequestHandler, HTTPServer

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Home OK")

        elif self.path == "/login":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Login OK")

        elif self.path == "/admin":
            self.send_response(401)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Nao autorizado")

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

def run():
    server = HTTPServer(("127.0.0.1", 8080), MockHandler)
    print("Mock HTTP rodando em http://127.0.0.1:8080")
    server.serve_forever()

if __name__ == "__main__":
    run()

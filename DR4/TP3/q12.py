from http.server import BaseHTTPRequestHandler, HTTPServer
import json, datetime
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = b"hello world!"
            self.send_response(200)
            self.send_header("Content-Type","text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/status":
            payload = {"status":"ok","time": datetime.datetime.utcnow().isoformat()}
            bts = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.send_header("Content-Length", str(len(bts)))
            self.end_headers()
            self.wfile.write(bts)
        else:
            self.send_error(404, "Not Found")
    def do_POST(self):
        if self.path == "/echo":
            n = int(self.headers.get("Content-Length","0"))
            data = self.rfile.read(n)[:10*1024]
            self.send_response(200)
            self.send_header("Content-Type","application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404, "Not Found")
if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), H).serve_forever()

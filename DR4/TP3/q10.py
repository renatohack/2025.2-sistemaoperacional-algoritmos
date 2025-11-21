import socket, os
HOST, PORT = "0.0.0.0", 8080
def make_resp(status, body: bytes, ctype="text/plain; charset=utf-8"):
    return (f"HTTP/1.1 {status}\r\n"
            f"Content-Type: {ctype}\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"\r\n").encode() + body

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT)); s.listen(5)
    print(f"HTTP estático em {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            req = conn.recv(4096).decode(errors="ignore")
            first = req.splitlines()[0] if req else ""
            method, path, *_ = (first.split() + ["", ""])[:3]
            if path == "/":
                if os.path.exists("index.html"):
                    body = open("index.html","rb").read()
                    resp = make_resp("200 OK", body, "text/html; charset=utf-8")
                else:
                    resp = make_resp("200 OK", b"no index.html")
            else:
                resp = make_resp("404 Not Found", b"Not Found")
            conn.sendall(resp)

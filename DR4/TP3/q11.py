import socket
import json
import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

HOST, PORT = "0.0.0.0", 8080

def now_sao_paulo_iso() -> str:
    tz = ZoneInfo("America/Sao_Paulo")
    return datetime.datetime.now(tz).isoformat()

def recv_http_request(conn) -> bytes:
    conn.settimeout(5)
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    if b"\r\n\r\n" not in data:
        return data

    head, body = data.split(b"\r\n\r\n", 1)
    headers_lines = head.decode(errors="ignore").split("\r\n")[1:]
    headers = {}
    for line in headers_lines:
        if not line.strip() or ":" not in line:
            continue
        k, v = line.split(":", 1)
        headers[k.strip().lower()] = v.strip()

    content_length = int(headers.get("content-length", "0") or "0")
    to_read = max(0, content_length - len(body))
    while to_read > 0:
        chunk = conn.recv(min(4096, to_read))
        if not chunk:
            break
        body += chunk
        to_read -= len(chunk)

    return head + b"\r\n\r\n" + body

def parse(req_bytes):
    req = req_bytes.decode(errors="ignore")
    if not req:
        raise ValueError("Requisição vazia")

    head, _, body_str = req.partition("\r\n\r\n")
    lines = head.split("\r\n")
    if not lines or len(lines[0].split()) < 2:
        raise ValueError("Request-Line inválida")

    method, path, *_ = (lines[0].split() + ["", ""])[:3]

    headers = {}
    for line in lines[1:]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Header inválido: {line!r}")
        k, v = line.split(":", 1)
        headers[k.strip().lower()] = v.strip()

    body = body_str.encode()
    return method, path, headers, body

def resp(status, body: bytes, ctype="text/plain; charset=utf-8"):
    return (f"HTTP/1.1 {status}\r\n"
            f"Content-Type: {ctype}\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Connection: close\r\n"
            f"\r\n").encode() + body

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    print(f"HTTP rotas em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            try:
                raw = recv_http_request(conn)
                method, path, headers, body = parse(raw)

                if method == "GET" and path == "/status":
                    payload = {
                        "status": "ok",
                        "time_sp": now_sao_paulo_iso(),   # horário em São Paulo (ex.: 2025-11-02T11:45:32-03:00)
                        "tz": "America/Sao_Paulo"
                    }
                    conn.sendall(resp("200 OK",
                                      json.dumps(payload).encode(),
                                      "application/json"))

                elif method == "POST" and path == "/echo":
                    body = body[:10 * 1024]  # limite 10 KiB
                    conn.sendall(resp("200 OK", body, "application/octet-stream"))

                else:
                    conn.sendall(resp("404 Not Found", b"Not Found"))

            except ValueError as e:
                conn.sendall(resp("400 Bad Request", f"Bad Request: {e}".encode()))
            except socket.timeout:
                conn.sendall(resp("408 Request Timeout", b"Timeout"))
            except Exception as e:
                conn.sendall(resp("500 Internal Server Error",
                                  f"Internal Server Error: {type(e).__name__}: {e}".encode()))
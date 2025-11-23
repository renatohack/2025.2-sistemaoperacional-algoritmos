import socket

HOST, PORT = "127.0.0.1", 8080

RESPONSE = (
    b"HTTP/1.1 200 OK\r\n"
    b"Content-Type: text/plain; charset=utf-8\r\n"
    b"Content-Length: 11\r\n"
    b"\r\n"
    b"Servidor OK"
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Servidor HTTP simples em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conexao de {addr}")
            _ = conn.recv(2048)  # lê e descarta a requisição HTTP
            conn.sendall(RESPONSE)  # sempre responde 200 OK + "Servidor OK"

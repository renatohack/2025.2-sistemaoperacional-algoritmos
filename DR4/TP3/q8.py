import socket, threading
HOST, PORT = "0.0.0.0", 5000
def handle(conn, addr):
    with conn:
        print("Conectado", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(20)
    print(f"Threads TCP em {HOST}:{PORT}")
    try:
        while True:
            c,a = srv.accept()
            threading.Thread(target=handle, args=(c,a), daemon=True).start()
    except KeyboardInterrupt:
        print("bye")
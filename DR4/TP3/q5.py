import socket, signal, sys
HOST, PORT = "0.0.0.0", 5000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print(f"Echo TCP ouvindo em {HOST}:{PORT}")
    try:
        while True:
            conn, addr = srv.accept()
            with conn:
                print("Conectado por", addr)
                data = conn.recv(1024)
                if not data:
                    continue
                conn.sendall(data)
    except KeyboardInterrupt:
        print("\nEncerrando.")

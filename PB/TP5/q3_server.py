import socket
import ssl
import threading

# ---------------------------------------------------------------------------
# Como testar localmente (detalhado):
# 1) Gere um certificado autoassinado (uma vez):
#    openssl req -x509 -nodes -newkey rsa:2048 -keyout q3_key.pem -out q3_cert.pem -days 365 -subj "/CN=localhost"
# 2) Inicie o servidor:
#    python q3_server.py
#    - Ele sobe em 127.0.0.1:4443.
#    - Ele carrega q3_cert.pem e q3_key.pem para o TLS.
#    - Ele aceita vários clientes ao mesmo tempo.
# 3) Em outros terminais, suba clientes:
#    python q3_client.py
#    - Cada cliente valida o cert do servidor usando q3_cert.pem.
#    - Digite mensagens e pressione Enter para enviar.
#    - Linha vazia encerra o cliente.
# 4) Cada mensagem recebida pelo servidor é retransmitida a todos os outros
#    clientes conectados (broadcast). O tráfego todo passa dentro do túnel TLS.
# ---------------------------------------------------------------------------


HOST = "127.0.0.1"
PORT = 4443
CERT_FILE = "q3_cert.pem"  # gerado via openssl
KEY_FILE = "q3_key.pem"

clients = []
lock = threading.Lock()


def broadcast(sender_conn, message):
    # Envia a mensagem para todos os clientes menos o remetente
    with lock:
        for conn in clients:
            if conn is sender_conn:
                continue
            try:
                conn.sendall(message)
            except Exception:
                pass


def handle_client(conn, addr):
    print(f"Cliente conectado: {addr}")
    with lock:
        clients.append(conn)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            broadcast(conn, data)
    except Exception as exc:
        print(f"Erro com {addr}: {exc}")
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"Cliente desconectado: {addr}")


def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"Servidor TLS ouvindo em {HOST}:{PORT}")

        with context.wrap_socket(sock, server_side=True) as tls_sock:
            while True:
                client_conn, addr = tls_sock.accept()
                thread = threading.Thread(target=handle_client, args=(client_conn, addr), daemon=True)
                thread.start()


if __name__ == "__main__":
    main()

import socket
import ssl
import threading
import sys

# ---------------------------------------------------------------------------
# Como testar localmente (detalhado):
# 1) Gere um certificado autoassinado (uma vez):
#    openssl req -x509 -nodes -newkey rsa:2048 -keyout q3_key.pem -out q3_cert.pem -days 365 -subj "/CN=localhost"
# 2) Inicie o servidor em outro terminal:
#    python q3_server.py
# 3) Rode este cliente em um ou mais terminais:
#    python q3_client.py
#    - Ele valida o servidor usando q3_cert.pem (CA local).
#    - Ele cria um túnel TLS, garantindo confidencialidade/integridade.
#    - Digite mensagens e Enter para enviar; linha vazia encerra o cliente.
# 4) Qualquer mensagem enviada por um cliente é recebida pelos demais via
#    broadcast no servidor. Todo conteúdo trafega criptografado via TLS.
# ---------------------------------------------------------------------------


HOST = "127.0.0.1"
PORT = 4443
CA_FILE = "q3_cert.pem"  # usado para validar o servidor


def recv_loop(conn):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            print(f"\nMensagem: {data.decode('utf-8', errors='replace')}")
    except Exception as exc:
        print(f"Erro no recebimento: {exc}")
    finally:
        conn.close()
        print("Conexão encerrada.")


def main():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_FILE)
    context.check_hostname = False  # aceitamos o CN do próprio cert local

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tls_conn = context.wrap_socket(raw_sock, server_hostname="localhost")
    tls_conn.connect((HOST, PORT))
    print(f"Conectado ao servidor {HOST}:{PORT} via TLS.")

    thread = threading.Thread(target=recv_loop, args=(tls_conn,), daemon=True)
    thread.start()

    try:
        for line in sys.stdin:
            msg = line.strip()
            if not msg:
                break
            tls_conn.sendall(msg.encode("utf-8"))
    finally:
        tls_conn.close()


if __name__ == "__main__":
    main()

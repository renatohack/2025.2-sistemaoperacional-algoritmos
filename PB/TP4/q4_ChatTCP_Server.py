"""
Q4 - Servidor de Chat TCP com múltiplos clientes (thread por conexão).

Como funciona:
- O servidor escuta em 127.0.0.1:5000 e aceita conexões continuamente.
- Cada cliente é atendido em uma thread dedicada e recebe eco das mensagens enviadas.
- Digite "/quit" no cliente para encerrar apenas aquela sessão.

Execução:
- Primeiro, rode este arquivo em um terminal:  python q4_ChatTCP_Server.py
- Depois, em outros terminais, rode quantos clientes desejar: python q4_ChatTCP_Client.py
"""

import socket
import threading


def atender_cliente(conn, addr):
    print("[Q4][Servidor] Cliente conectado:", addr)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                print("[Q4][Servidor] Cliente desconectou:", addr)
                break
            msg = data.decode('utf-8', errors='ignore').strip()
            print("[Q4][Servidor][{}] Recebido: {}".format(addr, msg))

            if msg == "/quit":
                conn.sendall(b"[Servidor] Encerrando a conexao.\n")
                print("[Q4][Servidor][{}] Encerrando por pedido do cliente.".format(addr))
                break

            resposta = "[Servidor ecoou] " + msg + "\n"
            conn.sendall(resposta.encode('utf-8'))
    finally:
        conn.close()
        print("[Q4][Servidor] Conexao finalizada para:", addr)


def main():
    host = '127.0.0.1'
    port = 5000

    # Cria o socket TCP (IPv4)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reutilizar a porta rapidamente após encerrar
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Faz bind no endereço e porta
    servidor.bind((host, port))
    servidor.listen(5)  # backlog padrão, aceita várias conexões simultâneas

    print("[Q4][Servidor] Aguardando conexões em {}:{}...".format(host, port))
    try:
        while True:
            conn, addr = servidor.accept()
            thread = threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n[Q4][Servidor] Encerrando servidor por KeyboardInterrupt.")
    finally:
        servidor.close()
        print("[Q4][Servidor] Servidor finalizado.")


if __name__ == "__main__":
    main()

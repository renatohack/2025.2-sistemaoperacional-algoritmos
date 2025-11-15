"""
Q4 - Cliente de Chat TCP (sem threads, 1 cliente).

Como funciona:
- Conecta no servidor 127.0.0.1:5000.
- Em laço, lê uma mensagem do usuário, envia ao servidor e mostra a resposta.
- Digite "/quit" para encerrar.

Execução:
- Abra outro terminal e rode: python q4_ChatTCP_Client.py
"""

import socket


def main():
    host = '127.0.0.1'
    port = 5000

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))
    print("[Q4][Cliente] Conectado ao servidor {}:{}".format(host, port))

    try:
        while True:
            msg = input("[Q4][Cliente] Digite uma mensagem (/quit para sair): ")
            cliente.sendall((msg + "\n").encode('utf-8'))

            # Se usuário pediu para sair, tentamos receber a resposta final e encerramos
            if msg == "/quit":
                resp = cliente.recv(4096)
                if resp:
                    print(resp.decode('utf-8', errors='ignore').strip())
                break

            # Recebe eco do servidor
            resp = cliente.recv(4096)
            if not resp:
                print("[Q4][Cliente] Servidor encerrou a conexão.")
                break
            print(resp.decode('utf-8', errors='ignore').strip())
    finally:
        cliente.close()
        print("[Q4][Cliente] Conexão encerrada.")


if __name__ == "__main__":
    main()


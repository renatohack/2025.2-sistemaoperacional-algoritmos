"""
Q5 - Envio de e-mail via Telnet (SMTP) em Python.

Observações importantes sobre portas e funcionamento:
- Porta 25: muitas redes/ISPs bloqueiam saída nessa porta. Vários servidores exigem TLS/Autenticação,
  então pode falhar.
- Porta 587 (submission): exige STARTTLS + autenticação (não dá para negociar com telnet puro).
- Porta 465: SMTPS (TLS direto), também não funciona com telnet puro.

Como testar de maneira confiável:
- Rode um servidor SMTP de depuração local que apenas imprime as mensagens recebidas, por exemplo:
    python -m smtpd -c DebuggingServer -n localhost:1025
  (Em algumas versões, o módulo pode ser "aiosmtpd". Alternativa: usar um SMTP real que aceite 25 sem TLS.)

Este script solicita destinatário, assunto, mensagem, host e porta SMTP, e envia comandos SMTP básicos:
HELO, MAIL FROM, RCPT TO, DATA, QUIT. Trata erros e imprime o resultado no terminal.
"""

import telnetlib


def send_line(tn, text):
    """Envia uma linha terminada com CRLF para o servidor via telnet."""
    tn.write((text + "\r\n").encode('utf-8'))


def read_response(tn):
    """Lê uma linha de resposta do servidor (até CRLF) e retorna como string."""
    resp = tn.read_until(b"\n", timeout=5)
    return resp.decode('utf-8', errors='ignore').strip()


def main():
    print("[Q5] Envio de e-mail via Telnet (SMTP)")
    to_addr = input("Destinatário (ex: teste@exemplo.com): ").strip()
    subject = input("Assunto: ").strip()
    print("Digite a mensagem. Finalize com uma linha contendo apenas um ponto '.' e Enter.")
    print("Ou deixe em branco para enviar uma mensagem simples gerada pelo script.")

    # Ler múltiplas linhas até encontrar um ponto sozinho, ou deixar vazio
    lines = []
    while True:
        line = input()
        if line == "":
            # Mensagem em branco: usa algo simples
            lines = [
                "Mensagem de teste enviada via Telnet/SMTP.",
                "Corpo de exemplo.",
            ]
            break
        if line == ".":
            break
        lines.append(line)

    host = input("SMTP host (ex: localhost): ").strip() or "localhost"
    try:
        port = int(input("SMTP porta (ex: 25 ou 1025): ").strip() or "1025")
    except ValueError:
        port = 1025

    from_addr = "remetente@local"  # Remetente simples para testes

    try:
        tn = telnetlib.Telnet(host, port, timeout=10)
        banner = read_response(tn)
        print("[Q5] Conectado. Resposta:", banner)

        send_line(tn, "HELO localhost")
        print("[Q5] -> HELO localhost")
        print("[Q5] <-", read_response(tn))

        send_line(tn, "MAIL FROM:<{}>".format(from_addr))
        print("[Q5] -> MAIL FROM:<{}>".format(from_addr))
        print("[Q5] <-", read_response(tn))

        send_line(tn, "RCPT TO:<{}>".format(to_addr))
        print("[Q5] -> RCPT TO:<{}>".format(to_addr))
        print("[Q5] <-", read_response(tn))

        send_line(tn, "DATA")
        print("[Q5] -> DATA")
        print("[Q5] <-", read_response(tn))

        # Cabeçalhos mínimos e corpo
        send_line(tn, "Subject: {}".format(subject))
        send_line(tn, "From: {}".format(from_addr))
        send_line(tn, "To: {}".format(to_addr))
        send_line(tn, "")  # linha em branco separa cabeçalhos do corpo
        for l in lines:
            send_line(tn, l)
        send_line(tn, ".")  # finaliza DATA
        print("[Q5] -> (corpo da mensagem) ... .")
        print("[Q5] <-", read_response(tn))

        send_line(tn, "QUIT")
        print("[Q5] -> QUIT")
        print("[Q5] <-", read_response(tn))

        tn.close()
        print("[Q5] E-mail processado pelo servidor SMTP (verifique o servidor de teste).")
    except Exception as e:
        print("[Q5][ERRO] Falha ao enviar via Telnet/SMTP:", str(e))
        print("Dica: para testar localmente, rode um SMTP de depuração em localhost:1025.")


if __name__ == "__main__":
    main()


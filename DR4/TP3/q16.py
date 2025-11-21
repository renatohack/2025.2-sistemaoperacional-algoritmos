import socket, ssl

HOST, PORT = "0.0.0.0", 8443

# 1 - Cria contexto TLS seguro
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

# 2 - Endurecimento mínimo
ctx.minimum_version = ssl.TLSVersion.TLSv1_2             # Bloqueia TLS 1.0/1.1
ctx.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!EXP:!DES')       # Ciphers seguros apenas
ctx.options |= ssl.OP_NO_COMPRESSION                     # Evita CRIME
ctx.options |= ssl.OP_CIPHER_SERVER_PREFERENCE            # Preferência do servidor

# 3 - Carrega certificado e chave
ctx.load_cert_chain(certfile="certificado.pem", keyfile="chave_privada.pem")

# 4 -  Cria socket TCP e encapsula em TLS
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Servidor HTTPS seguro em https://{HOST}:{PORT}")

    with ctx.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            print(f"Conexão segura de {addr}")
            with conn:
                req = conn.recv(2048).decode(errors="ignore")
                if not req:
                    continue
                # Resposta HTTP simples
                body = b"Conexao TLS segura com sucesso!"
                resp = (b"HTTP/1.1 200 OK\r\n"
                        b"Content-Type: text/plain; charset=utf-8\r\n"
                        + f"Content-Length: {len(body)}\r\n\r\n".encode()
                        + body)
                conn.sendall(resp)
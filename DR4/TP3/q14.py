import http.server, ssl

server = http.server.HTTPServer(('0.0.0.0', 8443), http.server.SimpleHTTPRequestHandler)

server.socket = ssl.wrap_socket(server.socket, certfile='certificado.pem', keyfile='chave_privada.pem', server_side=True)

print("Servidor HTTPS rodando na porta 8443...")

server.serve_forever()
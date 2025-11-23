import socket

HOST, PORT = "127.0.0.1", 6000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    mensagem = b"teste UDP"
    s.sendto(mensagem, (HOST, PORT))
    print("Mensagem UDP enviada para", HOST, PORT)
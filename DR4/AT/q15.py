import socket

PORTAS = [22, 80, 443]
HOST = "127.0.0.1"

def porta_aberta(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.connect((HOST, port))
            return True
        except:
            return False

for p in PORTAS:
    estado = "open" if porta_aberta(p) else "closed"
    print(f"Porta {p}: {estado}")

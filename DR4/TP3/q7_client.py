import socket
HOST, PORT = "127.0.0.1", 6000
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for m in [b"um", b"dois", b"tres"]:
        s.sendto(m, (HOST, PORT))
        resp, _ = s.recvfrom(2048)
        print(resp.decode())
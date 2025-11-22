#!/usr/bin/env python3
# server9090.py
import socket

HOST = "0.0.0.0"
PORT = 9090
MSG = "Hello\r\n"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Listening on {HOST}:{PORT} ...")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(MSG.encode("utf-8"))
            print(f"Sent: {MSG.strip()}")
            # opcional: fechar conexão imediatamente (o with faz isso)

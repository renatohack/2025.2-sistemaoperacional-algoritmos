import socket, time, sys
HOST, PORT = (sys.argv[1] if len(sys.argv)>1 else "127.0.0.1"), 5000
attempts = 3
for i in range(attempts):
    try:
        with socket.create_connection((HOST, PORT), timeout=2) as s:
            s.sendall(b"PING\n")
            print(s.recv(1024).decode(errors="ignore"))
            break
    except OSError as e:
        print(f"tentativa {i+1} falhou: {e}")
        time.sleep(1)
else:
    print("falhou apos 3 tentativas.")
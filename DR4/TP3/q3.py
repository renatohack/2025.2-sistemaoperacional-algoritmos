import socket, errno
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)
try:
    s.connect(("192.0.2.1", 12345))  # 192.0.2.0/24 é TEST-NET-1 (não roteável)
except socket.timeout:
    print("timeout após 2 segundos")
except OSError as e:
    if e.errno in (errno.EHOSTUNREACH, errno.ENETUNREACH, errno.ECONNREFUSED):
        print("rede inalcançável/recusada")
finally:
    s.close()

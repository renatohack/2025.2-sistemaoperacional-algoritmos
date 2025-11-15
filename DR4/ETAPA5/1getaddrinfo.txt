import socket

infos = socket.getaddrinfo("example.com", 80, proto=socket.IPPROTO_TCP, flags=socket.AI_CANONNAME)

print(f"{'Nº':<3} {'Família':<20} {'Tipo':<15} {'Protocolo':<10} {'Nome canônico':<30} {'Endereço':<40}")
print("-" * 130)

for i, info in enumerate(infos, 1):
    family, socktype, proto, canonname, sockaddr = info

    family_name = {
        socket.AF_INET: "AF_INET (IPv4)",
        socket.AF_INET6: "AF_INET6 (IPv6)"
    }.get(family, str(family))

    socktype_name = {
        socket.SOCK_STREAM: "SOCK_STREAM (TCP)",
        socket.SOCK_DGRAM: "SOCK_DGRAM (UDP)"
    }.get(socktype, str(socktype))

    proto_name = {
        socket.IPPROTO_TCP: "TCP",
        socket.IPPROTO_UDP: "UDP"
    }.get(proto, str(proto))

    print(f"{i:<3} {family_name:<20} {socktype_name:<15} {proto_name:<10} {canonname or '(não disponível)':<30} {str(sockaddr):<40}")

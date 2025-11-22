from scapy.all import sniff, IP, TCP


# ---------------------------------------------------------------------------
# Como usar (local):
# 1) Instale scapy se precisar: pip install scapy
# 2) Rode como admin/root (sniff precisa de permissao):
#    python q4.py
# 3) O script captura pacotes TCP na interface padrao e mostra 20 pacotes,
#    imprimindo IP origem/destino, portas, protocolo, flags, tamanho e TTL
#    em formato de tabela.
# ---------------------------------------------------------------------------


printed_header = False


def mostrar_pacote(pkt):
    # Imprime pacotes TCP com etiquetas e horário
    global printed_header
    if IP in pkt and TCP in pkt:
        ip = pkt[IP]
        tcp = pkt[TCP]
        from time import strftime

        timestamp = strftime("%H:%M:%S")
        proto = "TCP"
        length = len(pkt)
        ttl = ip.ttl

        if not printed_header:
            header = (
                f"{'TIME':<8} {'SRC':<15} {'SPORT':<6} "
                f"{'DST':<15} {'DPORT':<6} {'PROTO':<6} "
                f"{'FLAGS':<8} {'LEN':<5} {'TTL':<4}"
            )
            print(header)
            printed_header = True

        print(
            f"{timestamp:<8} {ip.src:<15} {tcp.sport:<6} "
            f"{ip.dst:<15} {tcp.dport:<6} {proto:<6} "
            f"{str(tcp.flags):<8} {length:<5} {ttl:<4}"
        )


def main():
    print("Capturando 20 pacotes TCP... (Ctrl+C para parar)")
    sniff(filter="tcp", prn=mostrar_pacote, count=20, store=False)
    print("Captura finalizada.")


if __name__ == "__main__":
    main()

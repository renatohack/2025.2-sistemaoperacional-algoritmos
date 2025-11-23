from scapy.all import rdpcap, TCP

PCAP_FILE = "captura.pcap"

def main():
    pacotes = rdpcap(PCAP_FILE)
    total = len(pacotes)
    tcp_count = sum(1 for p in pacotes if TCP in p)

    print(f"Arquivo analisado: {PCAP_FILE}")
    print(f"Total de pacotes: {total}")
    print(f"Pacotes com camada TCP: {tcp_count}")

if __name__ == "__main__":
    main()

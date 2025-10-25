import ipaddress
import numpy as np

try:
    import numba
except ImportError:  # pragma: no cover - ambiente sem numba usa fallback python
    numba = None


if numba is not None:

    @numba.njit
    def _int_to_bit_array_numba(valor: int, total_bits: int):
        """Converte inteiros de ate 64 bits usando numba para acelerar."""
        bits = np.empty(total_bits, dtype=np.uint8)
        for idx in range(total_bits):
            shift = total_bits - 1 - idx
            bits[idx] = (valor >> shift) & 1
        return bits

else:

    _int_to_bit_array_numba = None  # type: ignore


def _int_to_bit_array(valor: int, total_bits: int):
    """Gera vetor de bits; usa numba apenas para valores que cabem em int64."""
    if _int_to_bit_array_numba is not None and valor.bit_length() <= 63:
        return _int_to_bit_array_numba(valor, total_bits)
    bits = np.empty(total_bits, dtype=np.uint8)
    for idx in range(total_bits):
        shift = total_bits - 1 - idx
        bits[idx] = (valor >> shift) & 1
    return bits


def _bits_as_string(vetor, comprimento):
    """Transforma o vetor de bits nos primeiros `comprimento` caracteres "0"/"1"."""
    return "".join("1" if vetor[idx] else "0" for idx in range(comprimento))


def _network_to_bits(prefixo: str) -> str:
    """Recebe um prefixo IPv4/IPv6 e devolve apenas os bits relevantes."""
    rede = ipaddress.ip_network(prefixo, strict=False)
    vetor = _int_to_bit_array(int(rede.network_address), rede.max_prefixlen)
    return _bits_as_string(vetor, rede.prefixlen)


def _address_to_bits(endereco: str) -> str:
    """Converte um endereco arbitrario para seus bits completos."""
    addr = ipaddress.ip_address(endereco)
    vetor = _int_to_bit_array(int(addr), addr.max_prefixlen)
    return _bits_as_string(vetor, addr.max_prefixlen)


class Node:
    """Representa um ponto da trie, guardando filhos e o prefixo associado."""

    def __init__(self):
        self.children = {}
        self.prefix = None


class PrefixTree:
    """Implementa uma Trie para prefixos IPv4/IPv6."""

    def __init__(self):
        self.root = Node()

    def insert(self, prefixo: str) -> None:
        """Insere um prefixo convertendo-o para bits."""
        bits = _network_to_bits(prefixo)
        atual = self.root
        for bit in bits:
            if bit not in atual.children:
                atual.children[bit] = Node()
            atual = atual.children[bit]
        atual.prefix = prefixo

    def search(self, endereco: str):
        """Busca o prefixo mais longo que contem o endereco informado."""
        bits = _address_to_bits(endereco)
        atual = self.root
        melhor = None
        for bit in bits:
            if atual.prefix is not None:
                melhor = atual.prefix
            proximo = atual.children.get(bit)
            if proximo is None:
                break
            atual = proximo
        if atual.prefix is not None:
            melhor = atual.prefix
        return melhor

    def insert_many(self, prefixos):
        for prefixo in prefixos:
            self.insert(prefixo)


PREFIXOS_DEMO = [
    "10.0.0.0/8",
    "10.1.0.0/16",
    "172.16.0.0/12",
    "192.168.0.0/24",
    "192.168.1.0/24",
    "200.200.0.0/16",
    "203.0.113.0/24",
    "2001:db8::/32",
    "2001:db8:1234::/48",
    "2001:4860::/32",
    "2804:14d:1::/48",
]

ENDERECOS_DEMO = [
    "10.1.15.3",
    "10.2.0.1",
    "192.168.1.77",
    "192.0.2.1",
    "200.200.10.5",
    "8.8.8.8",
    "2001:db8:1234::abcd",
    "2001:4860:4860::8888",
    "2804:14d:1::abcd",
    "2001:db8:ffff::1",
]


def main():
    print("Inserindo prefixos de demonstracao na Trie...")
    arvore = PrefixTree()
    arvore.insert_many(PREFIXOS_DEMO)
    for prefixo in PREFIXOS_DEMO:
        print("  -", prefixo)

    print("\nBuscando alguns enderecos:")
    for endereco in ENDERECOS_DEMO:
        resultado = arvore.search(endereco)
        if resultado:
            print(f"{endereco:<39} -> {resultado}")
        else:
            print(f"{endereco:<39} -> nenhum prefixo correspondente")

    while True:
        print("\nMenu:")
        print("1 - Inserir novo prefixo")
        print("2 - Buscar endereco")
        print("0 - Encerrar")
        escolha = input("Opcao: ").strip()
        if escolha == "0":
            print("Encerrando questao 4.")
            break
        if escolha == "1":
            prefixo = input("Prefixo IPv4/IPv6 (ex: 192.168.2.0/24): ").strip()
            if prefixo:
                try:
                    arvore.insert(prefixo)
                    print("Prefixo inserido!")
                except ValueError as erro:
                    print("Prefixo invalido:", erro)
            else:
                print("Entrada vazia.")
        elif escolha == "2":
            endereco = input("Endereco para busca: ").strip()
            if endereco:
                try:
                    resposta = arvore.search(endereco)
                    if resposta:
                        print("Encontrado prefixo:", resposta)
                    else:
                        print("Nenhum prefixo cobre esse endereco.")
                except ValueError as erro:
                    print("Endereco invalido:", erro)
            else:
                print("Entrada vazia.")
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()


# (d) Inserir um prefixo na trie percorre apenas os bits definidos pelo comprimento
# do prefixo (L). Logo, a complexidade de tempo para insercao ou busca e O(L), onde
# L <= 32 para IPv4 e L <= 128 para IPv6. Essas operacoes nao dependem diretamente
# da quantidade total de prefixos armazenados, apenas do comprimento da chave.

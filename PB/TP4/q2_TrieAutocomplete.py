"""
Q2 - Sistema de Autocomplete usando Trie.

Funcionalidades:
- Inserção de palavras
- Busca de palavras por prefixo
- Contagem total de palavras armazenadas

Além disso, o script gera 10.000 strings aleatórias (8 letras minúsculas) para popular a Trie
e realiza buscas de exemplo para demonstrar o funcionamento.
"""

import random
import string


class TrieNode:
    """Nó básico da Trie. Guarda filhos e se é fim de palavra."""

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """Implementação simples de Trie para palavras ASCII minúsculas."""

    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0

    def insert(self, word):
        """Insere uma palavra na Trie. Marca o nó final como fim de palavra.

        Caso a palavra já exista, não incrementa a contagem de palavras.
        """
        node = self.root
        created_new = False
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                created_new = True
            node = node.children[ch]
        if not node.is_end:
            node.is_end = True
            # Consideramos uma palavra nova quando o estado final ainda não era fim.
            self.total_words += 1

    def _collect_from(self, node, prefix, result):
        """Coleta recursivamente todas as palavras abaixo de 'node' usando 'prefix'."""
        if node.is_end:
            result.append(prefix)
        for ch, child in node.children.items():
            self._collect_from(child, prefix + ch, result)

    def search_prefix(self, prefix):
        """Retorna uma lista com todas as palavras que começam com 'prefix'."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        result = []
        self._collect_from(node, prefix, result)
        return result

    def count_words(self):
        """Retorna o total de palavras armazenadas na Trie."""
        return self.total_words


def gerar_strings_aleatorias(qtd, tam):
    """Gera 'qtd' strings aleatórias de tamanho 'tam' com letras minúsculas."""
    alfabeto = string.ascii_lowercase
    itens = []
    for _ in range(qtd):
        s = ''.join(random.choice(alfabeto) for _ in range(tam))
        itens.append(s)
    return itens


if __name__ == "__main__":
    # Parte 1: exemplo dado no enunciado
    trie = Trie()
    palavras = ["apple", "banana", "apricot", "app", "appetizer", "bat", "ball", "batman"]
    for palavra in palavras:
        trie.insert(palavra)

    print("[Q2] Número total de palavras na Trie (exemplo 8 itens):", trie.count_words())
    prefixo = "app"
    print("[Q2] Palavras que começam com o prefixo '{}':".format(prefixo), trie.search_prefix(prefixo))

    # Parte 2: gerar 10.000 strings aleatórias e inserir
    trie2 = Trie()
    aleatorias = gerar_strings_aleatorias(10000, 8)
    for w in aleatorias:
        trie2.insert(w)

    # Exibir algumas estatísticas e uma busca por prefixo
    print("[Q2] Total de palavras após inserir 10.000 strings aleatórias:", trie2.count_words())
    # Escolher um prefixo aleatório de 2 letras para maior chance de resultados
    prefixo2 = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
    resultados = trie2.search_prefix(prefixo2)
    print("[Q2] Prefixo aleatório usado:", prefixo2)
    print("[Q2] Quantidade de sugestões encontradas:", len(resultados))
    # Mostrar só as 10 primeiras para não poluir o terminal
    print("[Q2] Primeiras sugestões:", resultados[:10])


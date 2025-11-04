"""Implementação simples de uma Trie com suporte a autocompletar."""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        if not word:
            raise ValueError("Não é possível inserir palavra vazia.")

        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.is_end_of_word = True

    def search(self, word):
        if not word:
            return False

        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def autocomplete(self, prefix):
        if prefix is None:
            raise ValueError("O prefixo não pode ser None.")

        node = self._find_node(prefix)
        if node is None:
            return []

        words = []
        self._collect_words(node, prefix, words)
        return words

    def _find_node(self, text):
        node = self.root
        for letter in text:
            if letter not in node.children:
                return None
            node = node.children[letter]
        return node

    def _collect_words(self, node, prefix, words):
        if node.is_end_of_word:
            words.append(prefix)

        for letter in sorted(node.children.keys()):
            self._collect_words(node.children[letter], prefix + letter, words)


if __name__ == "__main__":
    trie = Trie()
    palavras = ["carro", "casa", "cachorro", "caminho", "cacto", "banana"]

    for item in palavras:
        trie.insert(item)

    print("Palavras inseridas:", palavras)

    print("Busca por 'caminho':", trie.search("caminho"))
    print("Busca por 'cachorro':", trie.search("cachorro"))
    print("Busca por 'cachorrinho':", trie.search("cachorrinho"))
    print("Autocompletar 'ca':", trie.autocomplete("ca"))
    print("Autocompletar 'cac':", trie.autocomplete("cac"))
    print("Autocompletar 'cachor':", trie.autocomplete("cachor"))
    print("Autocompletar 'b':", trie.autocomplete("b"))

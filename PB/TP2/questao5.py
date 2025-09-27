"""Questão 5: árvore binária de busca e lista encadeada simples."""


# (a) Classe para nós da árvore binária com operações básicas.
class TreeNode:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None

    def inserir(self, novo_valor):
        """Insere `novo_valor` na subárvore respeitando a ordem da BST."""
        if novo_valor < self.valor:
            if self.esquerda is None:
                self.esquerda = TreeNode(novo_valor)
            else:
                self.esquerda.inserir(novo_valor)
        else:
            if self.direita is None:
                self.direita = TreeNode(novo_valor)
            else:
                self.direita.inserir(novo_valor)

    def buscar(self, procurado):
        """Retorna True se `procurado` estiver na subárvore, caso contrário False."""
        if procurado == self.valor:
            return True
        if procurado < self.valor and self.esquerda is not None:
            return self.esquerda.buscar(procurado)
        if procurado > self.valor and self.direita is not None:
            return self.direita.buscar(procurado)
        return False

    def em_ordem(self):
        """Retorna uma lista com os valores em ordem crescente."""
        resultado = []
        if self.esquerda is not None:
            resultado.extend(self.esquerda.em_ordem())
        resultado.append(self.valor)
        if self.direita is not None:
            resultado.extend(self.direita.em_ordem())
        return resultado

    def imprimir_em_ordem(self):
        """Imprime os valores da subárvore em ordem crescente."""
        print(" ".join(str(v) for v in self.em_ordem()))


# (c) Classe de nó para lista encadeada simples com operações básicas.
class ListNode:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

    def inserir_no_final(self, novo_valor):
        """Insere um novo nó ao final da lista que começa neste nó."""
        atual = self
        while atual.proximo is not None:
            atual = atual.proximo
        atual.proximo = ListNode(novo_valor)

    def buscar(self, procurado):
        """Retorna True se `procurado` estiver em algum nó a partir deste."""
        atual = self
        while atual is not None:
            if atual.valor == procurado:
                return True
            atual = atual.proximo
        return False

    def imprimir(self):
        """Imprime os valores da lista separados por setas."""
        atual = self
        valores = []
        while atual is not None:
            valores.append(str(atual.valor))
            atual = atual.proximo
        print(" -> ".join(valores))


'''(d) Complexidade de busca: em uma árvore binária de busca balanceada, a busca custa
O(log n) porque a cada passo descartamos metade do espaço de busca. Já na lista
encadeada, a busca é O(n) pois precisamos percorrer elemento a elemento até achar
ou chegar ao fim. Se a árvore estiver degenerada (como uma lista), a busca também
vira O(n), mostrando que a estrutura influencia diretamente o desempenho.'''


'''(e) Exemplo real: um sistema que mantém dados indexados por chaves numéricas (ex. IDs
ordenados) se beneficia de uma árvore binária para inserir e consultar rapidamente.
Com uma lista encadeada, cada consulta exigiria percorrer todos os elementos até achar
um ID específico. A árvore binária mantém os dados ordenados e permite saltos
logarítmicos, tornando consultas frequentes muito mais eficientes.'''


if __name__ == "__main__":
    # (b) Demonstração com alguns valores.
    valores_arvore = [50, 30, 70, 20, 40, 60, 80]
    raiz = TreeNode(valores_arvore[0])
    for valor in valores_arvore[1:]:
        raiz.inserir(valor)

    print("Busca 40 na árvore:", raiz.buscar(40))
    print("Busca 99 na árvore:", raiz.buscar(99))
    print("Árvore em ordem:", raiz.em_ordem())

    cabeca = ListNode(10)
    cabeca.inserir_no_final(20)
    cabeca.inserir_no_final(30)
    cabeca.inserir_no_final(40)

    print("Busca 30 na lista:", cabeca.buscar(30))
    print("Busca 99 na lista:", cabeca.buscar(99))
    print("Lista completa:", end=" ")
    cabeca.imprimir()

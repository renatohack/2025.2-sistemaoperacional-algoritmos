import time
from collections import deque


class Node:
    """Representa um nó da árvore.

    Cada nó guarda um `valor` (o nome do registro) e tem referências para
    filhos à esquerda e à direita. Se o filho não existir, fica como None.
    """

    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


class BinaryTree:
    """Implementa uma árvore binária de busca com operações básicas."""

    def __init__(self):
        self.raiz = None

    def inserir(self, valor):
        """Insere um novo valor seguindo a regra da BST (menores à esquerda).

        Caso a raiz ainda não exista, o novo nó passa a ser a raiz. Caso já
        exista, navegamos recursivamente até achar a posição correta.
        """

        if self.raiz is None:
            self.raiz = Node(valor)
            return
        self._inserir_rec(self.raiz, valor)

    def _inserir_rec(self, atual, valor):
        if valor < atual.valor:
            if atual.esquerda is None:
                atual.esquerda = Node(valor)
            else:
                self._inserir_rec(atual.esquerda, valor)
        else:
            if atual.direita is None:
                atual.direita = Node(valor)
            else:
                self._inserir_rec(atual.direita, valor)

    def inserir_varios(self, valores):
        """Insere uma lista de valores e devolve o tempo total gasto."""
        inicio = time.perf_counter()
        for valor in valores:
            self.inserir(valor)
        return time.perf_counter() - inicio

    def buscar(self, valor):
        """Procura um valor exatamente igual ao informado."""
        return self._buscar_rec(self.raiz, valor)

    def _buscar_rec(self, atual, valor):
        if atual is None:
            return None
        if valor == atual.valor:
            return atual
        if valor < atual.valor:
            return self._buscar_rec(atual.esquerda, valor)
        return self._buscar_rec(atual.direita, valor)

    def buscar_primeiro_por_prefixo(self, prefixo):
        """Retorna o primeiro valor encontrado que começa com `prefixo`.

        A busca faz uma varredura em ordem (esquerda, raiz, direita) para
        encontrar o primeiro nome que corresponda ao critério informado.
        """

        resultados = []
        self._buscar_in_order_por_prefixo(self.raiz, prefixo, resultados)
        return resultados[0] if resultados else None

    def _buscar_in_order_por_prefixo(self, atual, prefixo, resultados):
        if atual is None or resultados:
            return
        self._buscar_in_order_por_prefixo(atual.esquerda, prefixo, resultados)
        if atual.valor.startswith(prefixo):
            resultados.append(atual.valor)
            return
        self._buscar_in_order_por_prefixo(atual.direita, prefixo, resultados)

    def remover(self, valor):
        """Remove o valor indicado, se existir."""
        self.raiz, removido = self._remover_rec(self.raiz, valor)
        return removido

    def _remover_rec(self, atual, valor):
        if atual is None:
            return atual, False
        removido = False
        if valor < atual.valor:
            atual.esquerda, removido = self._remover_rec(atual.esquerda, valor)
        elif valor > atual.valor:
            atual.direita, removido = self._remover_rec(atual.direita, valor)
        else:
            removido = True
            # Caso 1: nó sem filhos
            if atual.esquerda is None and atual.direita is None:
                return None, True
            # Caso 2: apenas um filho
            if atual.esquerda is None:
                return atual.direita, True
            if atual.direita is None:
                return atual.esquerda, True
            # Caso 3: dois filhos -> usa sucessor em ordem
            sucessor = self._menor_no(atual.direita)
            atual.valor = sucessor.valor
            atual.direita, _ = self._remover_rec(atual.direita, sucessor.valor)
        return atual, removido

    def _menor_no(self, atual):
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def remover_primeiro_por_prefixo(self, prefixo):
        """Procura o primeiro valor com o prefixo e remove da árvore."""
        alvo = self.buscar_primeiro_por_prefixo(prefixo)
        if alvo is None:
            return False, None
        removido = self.remover(alvo)
        return removido, alvo

    def imprimir_ate_altura(self, altura_maxima=5):
        """Imprime a árvore até a altura informada (nível 0 é a raiz).

        Utilizo uma fila (deque) para fazer uma busca em largura, o que
        facilita imprimir nível a nível. Nós ausentes são mostrados como
        "-" para manter a estrutura visual."""

        if self.raiz is None:
            print("[árvore vazia]")
            return

        fila = deque([(self.raiz, 0)])
        nivel_atual = 0
        linha = []
        while fila:
            no, nivel = fila.popleft()
            if nivel > altura_maxima:
                break
            if nivel != nivel_atual:
                print("Nível", nivel_atual, ":", " ".join(linha))
                linha = []
                nivel_atual = nivel
            linha.append(no.valor if no else '-')
            if no:
                fila.append((no.esquerda, nivel + 1))
                fila.append((no.direita, nivel + 1))
        if linha:
            print("Nível", nivel_atual, ":", " ".join(linha))

    def contar_nos(self):
        """Conta quantos nós existem na árvore (usado em métricas)."""
        return self._contar_rec(self.raiz)

    def _contar_rec(self, atual):
        if atual is None:
            return 0
        return 1 + self._contar_rec(atual.esquerda) + self._contar_rec(atual.direita)


def carregar_registros(caminho):
    """Carrega nomes a partir de um arquivo texto (um por linha).

    Caso o arquivo não exista, devolve uma lista vazia e informa o erro.
    """

    registros = []
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                nome = linha.strip()
                if nome:
                    registros.append(nome)
    except FileNotFoundError:
        print("Arquivo não encontrado:", caminho)
    return registros


def sugerir_melhor_raiz(registros):
    """Sugere uma raiz equilibrada escolhendo o elemento central da lista ordenada.

    Quando usamos o elemento do meio como raiz, a árvore de busca tende a ficar
    mais balanceada, reduzindo o número de comparações médias nas operações.
    """

    if not registros:
        return None
    ordenados = sorted(registros)
    meio = len(ordenados) // 2
    return ordenados[meio]


'''(e) Para minimizar a altura da árvore (e, consequentemente, o número médio de
comparações), a melhor escolha prática para o nó raiz é um elemento central da
lista ordenada. Dessa forma distribuímos quantidades parecidas de registros nos
ramos esquerdo e direito, aproximando o comportamento de uma árvore balanceada.'''


def exibir_tabela_tempos(tempo_insercao, qtd_registros):
    """Mostra uma tabela simples com o tempo medido nas inserções iniciais."""

    print("\nResumo de tempos (exemplo):")
    print("+----------------------+----------------------+")
    print("| Operação             | Tempo (segundos)     |")
    print("+----------------------+----------------------+")
    print(f"| Inserção de {qtd_registros:5d} nós | {tempo_insercao:>20.6f} |")
    print("+----------------------+----------------------+")


def menu():
    print("\nEscolha uma operação:")
    print("1 - Inserir novo registro")
    print("2 - Remover primeiro registro que começa com 'M'")
    print("3 - Buscar primeiro registro que começa com 'Z'")
    print("4 - Imprimir árvore até altura 5")
    print("5 - Mostrar sugestão de melhor raiz")
    print("0 - Sair")


def main():
    caminho = input("Informe o caminho do arquivo gerado na TP1 (enter para usar 'dados_tp1.txt'): ")
    if not caminho:
        caminho = "dados_tp1.txt"

    registros = carregar_registros(caminho)
    arvore = BinaryTree()

    if registros:
        tempo = arvore.inserir_varios(registros)
        exibir_tabela_tempos(tempo, len(registros))
    else:
        print("Nenhum registro carregado. Você pode inserir manualmente pelo menu.")

    while True:
        menu()
        escolha = input("Opção: ")
        if escolha == "0":
            print("Encerrando...")
            break
        if escolha == "1":
            nome = input("Digite o nome a inserir: ").strip()
            if nome:
                arvore.inserir(nome)
                registros.append(nome)
                print("Inserido com sucesso!")
            else:
                print("Nome vazio não foi inserido.")
        elif escolha == "2":
            removido, valor = arvore.remover_primeiro_por_prefixo("M")
            if removido:
                if valor in registros:
                    registros.remove(valor)
                print("Removido:", valor)
            else:
                print("Nenhum registro começando com 'M' foi encontrado.")
        elif escolha == "3":
            encontrado = arvore.buscar_primeiro_por_prefixo("Z")
            if encontrado:
                print("Encontrado:", encontrado)
            else:
                print("Nenhum registro começando com 'Z' foi encontrado.")
        elif escolha == "4":
            arvore.imprimir_ate_altura(altura_maxima=5)
        elif escolha == "5":
            sugestao = sugerir_melhor_raiz(registros)
            if sugestao:
                print("Sugestão para raiz equilibrada:", sugestao)
            else:
                print("Carregue registros primeiro para gerar uma sugestão.")
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()

import time
from collections import deque
from pathlib import Path


class Node:
    """Representa um unico registro dentro da arvore."""

    def __init__(self, valor: str):
        self.valor = valor
        self.esquerda = None
        self.direita = None


class BinaryTree:
    """Implementa uma arvore binaria de busca basica."""

    def __init__(self):
        self.raiz = None

    def inserir(self, valor: str) -> None:
        """Insere um novo valor usando uma busca iterativa."""
        if self.raiz is None:
            self.raiz = Node(valor)
            return

        atual = self.raiz
        while True:
            if valor < atual.valor:
                if atual.esquerda is None:
                    atual.esquerda = Node(valor)
                    return
                atual = atual.esquerda
            else:
                if atual.direita is None:
                    atual.direita = Node(valor)
                    return
                atual = atual.direita

    def inserir_varios(self, valores) -> float:
        """Insere uma colecao de valores e devolve o tempo total."""
        inicio = time.perf_counter()
        for valor in valores:
            self.inserir(valor)
        return time.perf_counter() - inicio

    def buscar(self, valor: str):
        """Localiza um valor exato na arvore."""
        atual = self.raiz
        while atual is not None:
            if valor == atual.valor:
                return atual
            if valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def buscar_primeiro_por_prefixo(self, prefixo: str):
        """Percorre a arvore em ordem e devolve o primeiro valor com o prefixo."""
        pilha = []
        atual = self.raiz
        while pilha or atual is not None:
            while atual is not None:
                pilha.append(atual)
                atual = atual.esquerda
            atual = pilha.pop()
            if atual.valor.startswith(prefixo):
                return atual.valor
            atual = atual.direita
        return None

    def remover(self, valor: str) -> bool:
        """Remove o valor indicado, se existir."""
        atual = self.raiz
        pai = None

        while atual is not None and atual.valor != valor:
            pai = atual
            if valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita

        if atual is None:
            return False

        if atual.esquerda is not None and atual.direita is not None:
            pai_sucessor = atual
            sucessor = atual.direita
            while sucessor.esquerda is not None:
                pai_sucessor = sucessor
                sucessor = sucessor.esquerda
            atual.valor = sucessor.valor
            filho = sucessor.direita
            if pai_sucessor.esquerda is sucessor:
                pai_sucessor.esquerda = filho
            else:
                pai_sucessor.direita = filho
            return True

        filho = atual.esquerda if atual.esquerda is not None else atual.direita
        if pai is None:
            self.raiz = filho
        elif pai.esquerda is atual:
            pai.esquerda = filho
        else:
            pai.direita = filho
        return True

    def remover_primeiro_por_prefixo(self, prefixo: str):
        """Localiza e remove o primeiro valor com o prefixo indicado."""
        alvo = self.buscar_primeiro_por_prefixo(prefixo)
        if alvo is None:
            return False, None
        removido = self.remover(alvo)
        return removido, alvo if removido else None

    def imprimir_ate_altura(self, altura_maxima: int = 5) -> None:
        """Imprime a arvore ate o nivel informado."""
        if self.raiz is None:
            print("[arvore vazia]")
            return

        fila = deque([(self.raiz, 0)])
        nivel_atual = 0
        linha = []

        while fila:
            no, nivel = fila.popleft()
            if nivel > altura_maxima:
                break

            if nivel != nivel_atual:
                print(f"Nivel {nivel_atual}: {' '.join(linha)}")
                linha = []
                nivel_atual = nivel

            linha.append(no.valor if no is not None else "-")
            if no is not None:
                fila.append((no.esquerda, nivel + 1))
                fila.append((no.direita, nivel + 1))

        if linha:
            print(f"Nivel {nivel_atual}: {' '.join(linha)}")

    def contar_nos(self) -> int:
        """Conta o total de nos presentes na arvore."""
        if self.raiz is None:
            return 0

        pilha = [self.raiz]
        quantidade = 0
        while pilha:
            no = pilha.pop()
            quantidade += 1
            if no.esquerda is not None:
                pilha.append(no.esquerda)
            if no.direita is not None:
                pilha.append(no.direita)
        return quantidade


def carregar_registros(caminho: Path):
    """Ler o arquivo texto e devolver apenas linhas validas."""
    registros = []
    try:
        with caminho.open("r", encoding="ascii") as arquivo:
            for linha in arquivo:
                nome = linha.strip()
                if nome:
                    registros.append(nome)
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {caminho}")
    return registros


def sugerir_melhor_raiz(registros):
    """Seleciona o elemento central da lista ordenada."""
    if not registros:
        return None
    ordenados = sorted(registros)
    return ordenados[len(ordenados) // 2]


def executar_menu(arvore: BinaryTree) -> None:
    """Permite testar as operacoes manualmente depois da carga inicial."""
    while True:
        print("\nMenu de operacoes:")
        print("1 - Inserir novo nome")
        print("2 - Remover primeiro nome com prefixo")
        print("3 - Buscar primeiro nome com prefixo")
        print("4 - Imprimir arvore ate altura 5")
        print("0 - Sair do menu")
        opcao = input("Opcao: ").strip()

        if opcao == "0":
            print("Encerrando menu.")
            break
        if opcao == "1":
            nome = input("Nome para inserir: ").strip()
            if nome:
                arvore.inserir(nome)
                print("Nome inserido.")
            else:
                print("Nome vazio nao foi inserido.")
        elif opcao == "2":
            prefixo = input("Prefixo a remover: ").strip()
            if not prefixo:
                print("Prefixo vazio nao e valido.")
                continue
            removido, valor = arvore.remover_primeiro_por_prefixo(prefixo)
            if removido:
                print(f"Nome removido: {valor}")
            else:
                print("Nenhum nome encontrado com esse prefixo.")
        elif opcao == "3":
            prefixo = input("Prefixo a buscar: ").strip()
            if not prefixo:
                print("Prefixo vazio nao e valido.")
                continue
            encontrado = arvore.buscar_primeiro_por_prefixo(prefixo)
            if encontrado:
                print(f"Nome encontrado: {encontrado}")
            else:
                print("Nenhum nome encontrado com esse prefixo.")
        elif opcao == "4":
            arvore.imprimir_ate_altura(altura_maxima=5)
        else:
            print("Opcao invalida.")


def main() -> None:
    """Carrega os dados, executa as operacoes pedidas e mostra os resultados."""
    caminho_arquivo = Path("dados_tp1.txt")
    registros = carregar_registros(caminho_arquivo)
    if not registros:
        print("Lista de registros vazia. Gere o arquivo antes de rodar a questao.")
        return

    print(f"Total de registros carregados: {len(registros)}")

    arvore = BinaryTree()
    tempo_insercao = arvore.inserir_varios(registros)
    print(f"Tempo para inserir {len(registros)} nomes: {tempo_insercao:.6f} segundos")
    print(f"Total de nos apos a insercao: {arvore.contar_nos()}")

    removido, nome_removido = arvore.remover_primeiro_por_prefixo("M")
    if removido:
        print(f"Primeiro nome removido com prefixo 'M': {nome_removido}")
    else:
        print("Nenhum nome com prefixo 'M' foi encontrado para remocao.")

    encontrado = arvore.buscar_primeiro_por_prefixo("Z")
    if encontrado:
        print(f"Primeiro nome encontrado com prefixo 'Z': {encontrado}")
    else:
        print("Nenhum nome com prefixo 'Z' foi encontrado.")

    print("\nArvore ate a altura 5:")
    arvore.imprimir_ate_altura(altura_maxima=5)

    sugestao = sugerir_melhor_raiz(registros)
    if sugestao is not None:
        print(f"\nSugestao de melhor raiz: {sugestao}")
    else:
        print("\nNao foi possivel sugerir uma raiz.")

    executar_menu(arvore)


if __name__ == "__main__":
    main()


# (e) Escolher o elemento central da lista ordenada como raiz inicial distribui os valores
# de forma mais equilibrada entre os lados esquerdo e direito da arvore, reduzindo a altura
# final quando comparado a insercoes sequenciais ja ordenadas. Isso diminui o numero medio
# de comparacoes nas operacoes de busca e remocao.

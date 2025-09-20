import os
import random

random.seed(42)


class BSTNode:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


def inserir(raiz, valor):
    # Exercicio 3b: inserir valores na arvore binaria de busca.
    if raiz is None:
        return BSTNode(valor)
    if valor < raiz.valor:
        raiz.esquerda = inserir(raiz.esquerda, valor)
    else:
        raiz.direita = inserir(raiz.direita, valor)
    return raiz


def altura(raiz):
    # Exercicio 3c: calcular altura da arvore.
    if raiz is None:
        return 0
    altura_esquerda = altura(raiz.esquerda)
    altura_direita = altura(raiz.direita)
    return 1 + max(altura_esquerda, altura_direita)


def esta_balanceada(raiz):
    # Exercicio 3c: verificar se a arvore esta balanceada.
    if raiz is None:
        return True
    altura_esquerda = altura(raiz.esquerda)
    altura_direita = altura(raiz.direita)
    if abs(altura_esquerda - altura_direita) > 1:
        return False
    return esta_balanceada(raiz.esquerda) and esta_balanceada(raiz.direita)


def percurso_pre_ordem(raiz, resultado):
    # Exercicio 3d-i: percurso pre-ordem.
    if raiz is None:
        return
    resultado.append(raiz.valor)
    percurso_pre_ordem(raiz.esquerda, resultado)
    percurso_pre_ordem(raiz.direita, resultado)


def percurso_pos_ordem(raiz, resultado):
    # Exercicio 3d-ii: percurso pos-ordem.
    if raiz is None:
        return
    percurso_pos_ordem(raiz.esquerda, resultado)
    percurso_pos_ordem(raiz.direita, resultado)
    resultado.append(raiz.valor)


def percurso_em_ordem(raiz, resultado):
    # Exercicio 3d-iii: percurso em ordem.
    if raiz is None:
        return
    percurso_em_ordem(raiz.esquerda, resultado)
    resultado.append(raiz.valor)
    percurso_em_ordem(raiz.direita, resultado)


def percurso_em_nivel(raiz):
    # Exercicio 3d-iv: percurso em nivel usando lista como fila.
    if raiz is None:
        return []
    fila = [raiz]
    resultado = []
    while len(fila) > 0:
        atual = fila.pop(0)
        resultado.append(atual.valor)
        if atual.esquerda is not None:
            fila.append(atual.esquerda)
        if atual.direita is not None:
            fila.append(atual.direita)
    return resultado


def encontrar_minimo(raiz):
    atual = raiz
    while atual.esquerda is not None:
        atual = atual.esquerda
    return atual


def deletar(raiz, valor):
    # Exercicio 3f: remocao em arvore binaria de busca.
    if raiz is None:
        return None
    if valor < raiz.valor:
        raiz.esquerda = deletar(raiz.esquerda, valor)
    elif valor > raiz.valor:
        raiz.direita = deletar(raiz.direita, valor)
    else:
        if raiz.esquerda is None:
            return raiz.direita
        if raiz.direita is None:
            return raiz.esquerda
        sucessor = encontrar_minimo(raiz.direita)
        raiz.valor = sucessor.valor
        raiz.direita = deletar(raiz.direita, sucessor.valor)
    return raiz


def garantir_pasta_saidas():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")


def salvar_relatorio(linhas):
    caminho = os.path.join("outputs", "bst_report.txt")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")
    return caminho


def main():
    garantir_pasta_saidas()

    # Exercicio 3a: gerar lista com 100 elementos aleatorios.
    valores = []
    for _ in range(100):
        valores.append(random.randint(1, 1000))

    linhas = []
    linhas.append("Lista inicial de valores: " + str(valores))

    raiz = None
    for numero in valores:
        raiz = inserir(raiz, numero)

    altura_arvore = altura(raiz)
    linhas.append("Altura da arvore: " + str(altura_arvore))

    if esta_balanceada(raiz):
        linhas.append("A arvore esta balanceada (diferenca de alturas ate 1).")
    else:
        linhas.append("A arvore NAO esta balanceada (ha diferencas maiores que 1).")

    pre_ordem = []
    percurso_pre_ordem(raiz, pre_ordem)
    linhas.append("Percurso pre-ordem: " + str(pre_ordem))

    pos_ordem = []
    percurso_pos_ordem(raiz, pos_ordem)
    linhas.append("Percurso pos-ordem: " + str(pos_ordem))

    em_ordem = []
    percurso_em_ordem(raiz, em_ordem)
    linhas.append("Percurso em ordem: " + str(em_ordem))

    nivel = percurso_em_nivel(raiz)
    linhas.append("Percurso em nivel: " + str(nivel))

    if raiz is not None:
        # Exercicio 3g-i: deletar a raiz original.
        valor_raiz = raiz.valor
        linhas.append("Valor da raiz removida: " + str(valor_raiz))
        raiz = deletar(raiz, valor_raiz)
        linhas.append("Nivel apos deletar a raiz: " + str(percurso_em_nivel(raiz)))

    if raiz is not None and raiz.esquerda is not None:
        # Exercicio 3g-ii.
        valor_esquerda = raiz.esquerda.valor
        linhas.append("Valor removido da subarvore esquerda: " + str(valor_esquerda))
        raiz = deletar(raiz, valor_esquerda)
        linhas.append(
            "Nivel apos deletar a raiz da esquerda: " + str(percurso_em_nivel(raiz))
        )
    else:
        linhas.append("Nao havia subarvore esquerda apos a primeira remocao.")

    if raiz is not None and raiz.direita is not None:
        # Exercicio 3g-iii.
        valor_direita = raiz.direita.valor
        linhas.append("Valor removido da subarvore direita: " + str(valor_direita))
        raiz = deletar(raiz, valor_direita)
        linhas.append(
            "Nivel apos deletar a raiz da direita: " + str(percurso_em_nivel(raiz))
        )
    else:
        linhas.append("Nao havia subarvore direita apos as remocoes anteriores.")

    caminho = salvar_relatorio(linhas)
    print("Relatorio salvo em: " + caminho)


if __name__ == "__main__":
    main()

import os


def explicar_estrutura_otima():
    # Exercicio 4a: descrever a estrutura de uma solucao otima.
    texto = (
        "Se as ultimas letras das cadeias forem iguais, elas pertencem a uma subsequencia comum "
        "maxima e o problema continua com os prefixos. Caso contrario, comparamos as respostas "
        "obtidas ao ignorar a ultima letra de cada cadeia."
    )
    return texto


def lcs_recursiva(x, y):
    # Exercicio 4b: solucao recursiva com memoizacao manual para evitar repeticao de calculos.
    memoria = {}

    def resolver(i, j):
        chave = (i, j)
        if chave in memoria:
            return memoria[chave]
        if i == 0 or j == 0:
            memoria[chave] = 0
        elif x[i - 1] == y[j - 1]:
            memoria[chave] = 1 + resolver(i - 1, j - 1)
        else:
            valor1 = resolver(i - 1, j)
            valor2 = resolver(i, j - 1)
            memoria[chave] = valor1 if valor1 >= valor2 else valor2
        return memoria[chave]

    return resolver(len(x), len(y))


def lcs_dinamica(x, y):
    # Exercicio 4d: programacao dinamica iterativa.
    m = len(x)
    n = len(y)
    dp = []
    for _ in range(m + 1):
        dp.append([0] * (n + 1))

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                if dp[i - 1][j] >= dp[i][j - 1]:
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = dp[i][j - 1]

    subsequencia = []
    i = m
    j = n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            subsequencia.append(x[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    subsequencia.reverse()
    return dp[m][n], "".join(subsequencia)


def salvar_relatorio(texto):
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    caminho = os.path.join("outputs", "lcs_report.txt")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
    return caminho


def main():
    cadeia_a = "ABCBDAB"
    cadeia_b = "BDCABA"

    explicacao = explicar_estrutura_otima()
    comprimento_recursivo = lcs_recursiva(cadeia_a, cadeia_b)
    comprimento_dp, subsequencia = lcs_dinamica(cadeia_a, cadeia_b)

    linhas = []
    linhas.append("Exercicio 4a: " + explicacao)
    linhas.append("Exercicio 4b: comprimento encontrado pela recursao = " + str(comprimento_recursivo))
    linhas.append("Exercicio 4c: comprimento otimo = " + str(comprimento_dp))
    linhas.append("Exercicio 4d: subsequencia reconstruida = " + subsequencia)

    caminho = salvar_relatorio("\n".join(linhas))
    print("Relatorio salvo em: " + caminho)


if __name__ == "__main__":
    main()

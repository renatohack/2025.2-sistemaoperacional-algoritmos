import os
import random
import sys
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Exercicio 1a: criar lista grande com 100000 numeros aleatorios.
REFERENCE_SIZE = 100000
REFERENCE_LIMIT = 1000000

# Exercicio 1c: tamanhos de teste indo ate 100000 elementos.
SAMPLE_SIZES = [100, 500, 1000, 5000, 10000, 20000, 50000, 100000]

# Conjuntos auxiliares para separar os graficos por complexidade observada.
QUADRATIC_ALGORITHMS = ["Selection Sort", "Insertion Sort", "Bubble Sort"]
LINEARITHMIC_ALGORITHMS = ["Merge Sort", "Quick Sort"]

random.seed(42)


def selection_sort(arr):
    # Exercicio 1b-i: Selection Sort basico.
    n = len(arr)
    for i in range(0, n - 1):
        min_pos = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_pos]:
                min_pos = j
        arr[i], arr[min_pos] = arr[min_pos], arr[i]
    return arr


def insertion_sort(arr):
    # Exercicio 1b-ii: Insertion Sort basico.
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = chave
    return arr


def bubble_sort(arr):
    # Exercicio 1b-iii: Bubble Sort simples com parada se nao houver trocas.
    n = len(arr)
    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                trocou = True
        if not trocou:
            break
    return arr


def merge_sort(arr):
    # Exercicio 1b-iv: Merge Sort recursivo.
    if len(arr) <= 1:
        return arr
    meio = len(arr) // 2
    esquerda = merge_sort(arr[:meio])
    direita = merge_sort(arr[meio:])
    return merge_listas(esquerda, direita)


def merge_listas(esquerda, direita):
    resultado = []
    i = 0
    j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1
    return resultado


def quick_sort(arr):
    # Exercicio 1b-v: Quick Sort usando o ultimo elemento como pivo.
    particiona_quick(arr, 0, len(arr) - 1)
    return arr


def particiona_quick(arr, inicio, fim):
    if inicio < fim:
        pivo = arr[fim]
        i = inicio - 1
        for j in range(inicio, fim):
            if arr[j] <= pivo:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[fim] = arr[fim], arr[i + 1]
        pos_pivo = i + 1
        particiona_quick(arr, inicio, pos_pivo - 1)
        particiona_quick(arr, pos_pivo + 1, fim)


ALGORITHMS = [
    ("Selection Sort", selection_sort),
    ("Insertion Sort", insertion_sort),
    ("Bubble Sort", bubble_sort),
    ("Merge Sort", merge_sort),
    ("Quick Sort", quick_sort),
]


def garantir_pasta_saidas():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")


def criar_lista_referencia():
    # Exercicio 1a: lista base a partir da qual pegamos os prefixos.
    numeros = []
    for _ in range(REFERENCE_SIZE):
        numeros.append(random.randint(0, REFERENCE_LIMIT))
    return numeros


def executar_algoritmo(funcao, dados):
    # Exercicio 1d: executar cada algoritmo e medir o tempo gasto.
    copia = dados[:]
    inicio = time.perf_counter()
    resultado = funcao(copia)
    fim = time.perf_counter()
    if resultado != sorted(dados):
        raise ValueError("Resultado incorreto encontrado em " + funcao.__name__)
    return fim - inicio


def salvar_csv(resultados):
    caminho = os.path.join("outputs", "sorting_results.csv")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("algorithm,size,time_seconds\n")
        for linha in resultados:
            arquivo.write(f"{linha[0]},{linha[1]},{linha[2]:.6f}\n")
    return caminho


def plotar_grafico(resultados, nomes_algoritmos, nome_arquivo, titulo):
    # Exercicio 1e: plotar graficos com escalas separadas por grupo de algoritmos.
    caminho = os.path.join("outputs", nome_arquivo)
    plt.figure(figsize=(10, 6))
    for nome in nomes_algoritmos:
        xs = []
        ys = []
        for item in resultados:
            if item[0] == nome:
                xs.append(item[1])
                ys.append(item[2])
        if xs:
            plt.plot(xs, ys, marker="o", label=nome)
    plt.xlabel("Tamanho da entrada")
    plt.ylabel("Tempo (s)")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    return caminho


def escrever_relatorio(resultados, linhas_log):
    # Exercicio 1f: registrar uma discussao simples sobre os resultados.
    caminho = os.path.join("outputs", "sorting_report.txt")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in linhas_log:
            arquivo.write(linha + "\n")
        arquivo.write("\nResumo geral:\n")
        for nome, _ in ALGORITHMS:
            escolhidos = [item for item in resultados if item[0] == nome]
            if escolhidos:
                ultimo = escolhidos[-1]
                arquivo.write(
                    f"{nome}: executado ate n={ultimo[1]} com tempo final de {ultimo[2]:.4f}s\n"
                )
        arquivo.write(
            "\nConclusao: algoritmos quadraticos demoram muito para entradas grandes, "
            "enquanto Merge Sort e Quick Sort mantem tempos baixos mesmo com 100000 elementos.\n"
        )
        arquivo.write(
            "Graficos gerados: `sorting_times_n2.png` para os algoritmos O(n^2) e "
            "`sorting_times_nlogn.png` para os algoritmos com comportamento proximo de n log n.\n"
        )
    return caminho


def salvar_log(linhas_log):
    caminho = os.path.join("outputs", "sorting_log.txt")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in linhas_log:
            arquivo.write(linha + "\n")
    return caminho


def executar_benchmarks():
    garantir_pasta_saidas()
    referencia = criar_lista_referencia()
    resultados = []
    linhas_log = []
    for tamanho in SAMPLE_SIZES:
        subconjunto = referencia[:tamanho]
        for nome, funcao in ALGORITHMS:
            tempo_gasto = executar_algoritmo(funcao, subconjunto)
            resultados.append((nome, tamanho, tempo_gasto))
            registro = f"{nome} | n={tamanho} | tempo={tempo_gasto:.4f}s"
            print(registro)
            linhas_log.append(registro)
    salvar_log(linhas_log)
    salvar_csv(resultados)
    plotar_grafico(
        resultados,
        QUADRATIC_ALGORITHMS,
        "sorting_times_n2.png",
        "Tempos de algoritmos O(n^2)",
    )
    plotar_grafico(
        resultados,
        LINEARITHMIC_ALGORITHMS,
        "sorting_times_nlogn.png",
        "Tempos de algoritmos O(n log n)",
    )
    escrever_relatorio(resultados, linhas_log)


def main():
    executar_benchmarks()
    print("Arquivos gerados na pasta outputs.")


if __name__ == "__main__":
    # Aumenta o limite de recursao para o Quick Sort lidar com listas maiores.
    sys.setrecursionlimit(300000)
    main()

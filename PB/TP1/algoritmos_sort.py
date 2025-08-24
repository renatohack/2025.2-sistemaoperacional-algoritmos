import time

def bubble_sort(arr):
    n = len(arr)
    for right_index in range(n):
        trocou = False
        for left_index in range(0, n - right_index - 1):
            if arr[left_index] > arr[left_index + 1]:
                aux = arr[left_index]
                arr[left_index] = arr[left_index + 1]
                arr[left_index + 1] = aux
                trocou = True
        if not trocou:
            break
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        aux = arr[i]
        arr[i] = arr[min_index]
        arr[min_index] = aux
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = chave
    return arr



def carregar_listagem(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]

def medir_tempo(func, dados):
    copia = list(dados)
    inicio = time.perf_counter()
    ordenado = func(copia)
    duracao = time.perf_counter() - inicio
    return ordenado, duracao

def salvar_tempos(registros, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        for nome_alg, t in registros:
            f.write(f"{nome_alg}: {t:.6f} segundos\n")

if __name__ == "__main__":
    LIST_FILE = "listagem_completa.txt"
    OUT_LOG = "tempos_ordenacao_sort.txt"

    arquivos = carregar_listagem(LIST_FILE)

    resultados = []

    _, t_bubble = medir_tempo(bubble_sort, arquivos)
    resultados.append(("Bubble Sort", t_bubble))

    _, t_selection = medir_tempo(selection_sort, arquivos)
    resultados.append(("Selection Sort", t_selection))

    ordenado_insertion, t_insertion = medir_tempo(insertion_sort, arquivos)
    resultados.append(("Insertion Sort", t_insertion))

    salvar_tempos(resultados, OUT_LOG)
    print("\nTempos de execução:")
    for nome_alg, t in resultados:
        print(f"{nome_alg}: {t:.6f} s")
    print(f"\nTempos também salvos em: {OUT_LOG}")

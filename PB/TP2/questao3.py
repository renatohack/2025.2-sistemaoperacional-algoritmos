"""Questão 3: QuickSort e QuickSelect aplicados à lista da TP1."""

# (a) Implementação do algoritmo QuickSort in-place usando partição Lomuto.
def quicksort(valores, inicio=0, fim=None):
    """Classifica `valores` in-place entre os índices `inicio` e `fim` usando QuickSort."""
    if fim is None:
        fim = len(valores) - 1
    if inicio >= fim:
        return

    pivo_idx = _particionar(valores, inicio, fim)
    quicksort(valores, inicio, pivo_idx - 1)
    quicksort(valores, pivo_idx + 1, fim)


def _particionar(valores, inicio, fim):
    """Posiciona o pivo e devolve seu índice final."""
    pivo = valores[fim]
    i = inicio
    for j in range(inicio, fim):
        if valores[j] <= pivo:
            valores[i], valores[j] = valores[j], valores[i]
            i += 1
    valores[i], valores[fim] = valores[fim], valores[i]
    return i


# (b) Implementação do QuickSelect para achar o k-ésimo menor elemento.
def quickselect(valores, k):
    """Retorna o k-ésimo menor elemento (0-indexado) de `valores` usando QuickSelect."""
    if k < 0 or k >= len(valores):
        raise IndexError("k fora do intervalo da sequência")

    lista = list(valores)
    inicio, fim = 0, len(lista) - 1
    while True:
        pivo_idx = _particionar(lista, inicio, fim)
        if pivo_idx == k:
            return lista[pivo_idx]
        if pivo_idx > k:
            fim = pivo_idx - 1
        else:
            inicio = pivo_idx + 1


'''(c) Complexidade: QuickSort tem tempo médio O(n log n) e pior caso O(n^2) quando a
partição fica desbalanceada; espaço O(log n) no caso médio pelo uso recursivo da pilha.
QuickSelect tem tempo médio O(n) e pior caso O(n^2), usando espaço O(1) além da pilha se
implementado iterativamente como acima. QuickSort é mais interessante quando precisamos
da lista inteira ordenada, enquanto QuickSelect é preferível quando só precisamos de um
único elemento k-ésimo, evitando ordenar tudo.'''


if __name__ == "__main__":
    # Exemplos simples para validar comportamento sem precisar do arquivo real.
    dados_exemplo = [3, 6, 1, 8, 4, 2]
    quicksort(dados_exemplo)
    print("Lista ordenada:", dados_exemplo)
    print("Elemento na posição 2 (0-indexado):", quickselect(dados_exemplo, 2))

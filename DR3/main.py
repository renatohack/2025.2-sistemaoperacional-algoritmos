from heap_utils import MaxHeap, merge_sorted_lists, heapsort


def demonstrate_heap_operations() -> None:
    """Mostra passo a passo como inserir, consultar e remover elementos da max-heap."""
    print("=== Demonstracao da manutencao da max-heap ===")
    heap = MaxHeap()
    numbers_to_insert = [42, 29, 18, 14, 7, 18, 12, 11, 13]
    print(f"Numeros inseridos: {numbers_to_insert}")

    for number in numbers_to_insert:
        # Insere cada numero e deixa a estrutura ajustar o maior para a raiz.
        heap.insert(number)

    print(f"Estado interno da heap: {heap.list_values()}")
    print(f"Heap esta vazia? {heap.is_empty()}")
    print(f"A heap contem o valor 18? {heap.contains(18)}")
    print(f"A heap contem o valor 30? {heap.contains(30)}")

    removed_first = heap.remove()
    removed_second = heap.remove()
    print(f"Maior valor removido (1a remocao): {removed_first}")
    print(f"Maior valor removido (2a remocao): {removed_second}")
    print(f"Estado interno apos remocoes: {heap.list_values()}")
    print(f"Heap esta vazia? {heap.is_empty()}")


def demonstrate_heapsort() -> None:
    """Aplica o HeapSort na lista exemplo e mostra antes e depois."""
    print("\n=== Demonstracao do HeapSort ===")
    values = [21, 1, 45, 78, 3, 5]
    print(f"Vetor original: {values}")
    sorted_values = heapsort(values)
    print(f"Vetor ordenado: {sorted_values}")


def demonstrate_merge_sorted_lists() -> None:
    """Usa a max-heap para juntar listas ordenadas sem perder a ordem final crescente."""
    print("\n=== Demonstracao da combinacao de listas ordenadas com max-heap ===")
    sorted_lists = [
        [1, 4, 9],
        [2, 3, 8],
        [0, 5, 7, 10],
    ]
    print(f"Listas de entrada: {sorted_lists}")
    merged = merge_sorted_lists(sorted_lists)
    print(f"Lista final combinada: {merged}")


if __name__ == "__main__":
    demonstrate_heap_operations()
    demonstrate_heapsort()
    demonstrate_merge_sorted_lists()

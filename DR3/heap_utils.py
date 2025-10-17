"""Funcoes de heap usando max-heap para o trabalho."""


class MaxHeap:
    """Mantem uma heap de maximo usando apenas uma lista Python."""

    def __init__(self):
        self._values = []

    def insert(self, value):
        """Insere o valor no fim e sobe enquanto for maior que o pai."""
        self._values.append(value)
        self._bubble_up(len(self._values) - 1)

    def is_empty(self):
        """Retorna True quando nao ha elementos armazenados."""
        return not self._values

    def remove(self):
        """Remove o maior valor, traz o ultimo para a raiz e desce ate a posicao correta."""
        if not self._values:
            return None

        largest_value = self._values[0]
        last_value = self._values.pop()

        if self._values:
            self._values[0] = last_value
            self._bubble_down(0)

        return largest_value

    def list_values(self):
        """Retorna uma copia da lista interna para inspecao."""
        return list(self._values)

    def contains(self, value):
        """Busca linear pelos valores armazenados."""
        return value in self._values

    def _bubble_up(self, index):
        """Compara o novo elemento com o pai e troca enquanto for maior."""
        while index > 0:
            parent_index = (index - 1) // 2
            # Se o filho for maior que o pai, troca para levar o maior rumo a raiz.
            if self._values[index] > self._values[parent_index]:
                self._values[index], self._values[parent_index] = (
                    self._values[parent_index],
                    self._values[index],
                )
                index = parent_index
            else:
                break

    def _bubble_down(self, index):
        """Compara o elemento com os filhos e troca com o maior deles ate recuperar a propriedade."""
        size = len(self._values)
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            largest = index

            # Checa qual filho possui o maior valor e guarda o indice dele.
            if left_child < size and self._values[left_child] > self._values[largest]:
                largest = left_child

            if right_child < size and self._values[right_child] > self._values[largest]:
                largest = right_child

            if largest != index:
                self._values[index], self._values[largest] = (
                    self._values[largest],
                    self._values[index],
                )
                index = largest
            else:
                break


def heapsort(values):
    """Ordena construindo uma max-heap e extraindo o maior elemento passo a passo."""
    copied_values = list(values)
    size = len(copied_values)

    # Primeiro passo: transformar toda a lista em uma max-heap.
    _build_max_heap(copied_values, size)

    for end in range(size - 1, 0, -1):
        # Move o maior elemento (na raiz) para o final da parte ativa.
        copied_values[0], copied_values[end] = copied_values[end], copied_values[0]
        # Reajusta a subarvore restante para continuar sendo uma max-heap.
        _heapify_down(copied_values, 0, end)

    return copied_values


def _build_max_heap(values, size):
    """Comeca pelos pais mais a direita e aplica o ajuste para baixo em cada subarvore."""
    last_parent = (size // 2) - 1
    for index in range(last_parent, -1, -1):
        # Cada chamada transforma a subarvore com raiz em index em uma max-heap.
        _heapify_down(values, index, size)


def _heapify_down(values, index, size):
    """Compara um no com os filhos e desce trocando sempre com o maior filho."""
    while True:
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        largest = index

        if left_child < size and values[left_child] > values[largest]:
            largest = left_child

        if right_child < size and values[right_child] > values[largest]:
            largest = right_child

        if largest != index:
            # Troca o pai com o maior filho e continua a checagem na nova posicao.
            values[index], values[largest] = values[largest], values[index]
            index = largest
        else:
            break


def merge_sorted_lists(sorted_lists):
    """Combina listas ordenadas usando uma max-heap. Assume listas de entrada em ordem crescente."""
    heap = MaxHeap()
    result_desc = []

    # Insere o ultimo elemento de cada lista, que e o maior daquela lista.
    for list_id, values in enumerate(sorted_lists):
        if values:
            last_index = len(values) - 1
            heap.insert((values[last_index], list_id, last_index))

    # Remove sempre o maior valor disponivel e adiciona ao resultado em ordem decrescente.
    while not heap.is_empty():
        packed_value = heap.remove()
        if packed_value is None:
            break

        value, list_id, element_index = packed_value
        result_desc.append(value)

        next_index = element_index - 1
        if next_index >= 0:
            next_value = sorted_lists[list_id][next_index]
            # Insere o proximo valor da mesma lista para continuar a intercalacao.
            heap.insert((next_value, list_id, next_index))

    # Como extraimos sempre o maior, o resultado esta em ordem decrescente. Reverte para ordem crescente.
    result_desc.reverse()
    return result_desc


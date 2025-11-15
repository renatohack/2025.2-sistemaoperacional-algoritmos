"""
Q1 - Heap Binária para fila de pacientes por prioridade.

Regras:
- Quanto menor o valor em 'priority', maior a prioridade (1 é a maior prioridade).
- Usaremos uma min-heap simples baseada em lista.

Observação importante sobre empates:
- Quando dois pacientes têm a mesma prioridade, a ordem entre eles pode variar.
- Isso acontece porque a heap organiza por prioridade e não garante estabilidade.
"""


class BinaryHeap:
    """Heap binária mínima para dicionários com chaves 'name' e 'priority'."""

    def __init__(self):
        # Armazena os itens (dicionários) internamente em uma lista
        self.data = []

    def is_empty(self):
        # Retorna True se a heap não tem elementos
        return len(self.data) == 0

    def _compare(self, a, b):
        """Retorna True se 'a' deve vir antes de 'b' na heap (menor priority).

        Critério:
        - priority menor vem antes
        """
        return a['priority'] < b['priority']

    def _swap(self, i, j):
        # Troca dois elementos de posição
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _heapify_up(self, index):
        # Sobe o elemento na posição 'index' até restaurar a propriedade da heap
        while index > 0:
            parent = (index - 1) // 2
            if self._compare(self.data[index], self.data[parent]):
                self._swap(index, parent)
                index = parent
            else:
                break

    def _heapify_down(self, index):
        # Desce o elemento na posição 'index' até restaurar a propriedade da heap
        n = len(self.data)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < n and self._compare(self.data[left], self.data[smallest]):
                smallest = left
            if right < n and self._compare(self.data[right], self.data[smallest]):
                smallest = right

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def insert(self, item):
        """Insere um novo elemento (dict com name e priority) na heap."""
        self.data.append(item)
        self._heapify_up(len(self.data) - 1)

    def find_min(self):
        """Retorna o elemento mínimo sem removê-lo (ou None se vazio)."""
        if self.is_empty():
            return None
        return self.data[0]

    def extract_min(self):
        """Remove e retorna o elemento de maior prioridade (menor priority)."""
        if self.is_empty():
            return None
        root = self.data[0]
        last = self.data.pop()
        if not self.is_empty():
            self.data[0] = last
            self._heapify_down(0)
        return root

    def build_heap(self, items):
        """Constrói a heap a partir de uma lista de itens."""
        self.data = list(items)
        # Heapify bottom-up
        for i in range((len(self.data) // 2) - 1, -1, -1):
            self._heapify_down(i)


if __name__ == "__main__":
    # Exemplo de uso conforme enunciado
    patients = [
        {'name': 'João', 'priority': 3},
        {'name': 'Maria', 'priority': 1},
        {'name': 'Pedro', 'priority': 4},
        {'name': 'Ana', 'priority': 2},
        {'name': 'Mariana', 'priority': 5},
        {'name': 'Rafael', 'priority': 2},
        {'name': 'Carolina', 'priority': 3},
    ]

    heap = BinaryHeap()
    heap.build_heap(patients)

    print("[Q1] find_min deve ser Maria (1):", heap.find_min())
    print("[Q1] extract_min deve ser Maria (1):", heap.extract_min())
    heap.insert({'name': 'Carlos', 'priority': 2})

    print("[Q1] Removendo todos em ordem de prioridade:")
    while not heap.is_empty():
        print(heap.extract_min())


# Trabalho: Heap e HeapSort

## 1. Vantagens e desvantagens do uso de uma heap

**Vantagens**
- Inserção e remoção do maior elemento acontecem em `O(log n)` gracas à altura limitada da arvore binária completa.
- Recuperação do elemento de maior prioridade é `O(1)` porque ele fica na raiz.
- Estrutura compacta: armazenada em um vetor contínuo, aproveitando bem a memória e a localidade de referência.
- Implementação simples quando comparada com outras árvores balanceadas.

**Desvantagens**
- Não há suporte eficiente para busca geral: encontrar um valor arbitrário ainda é `O(n)`, diferente de árvores binárias de busca balanceadas (`O(log n)`).
- Estrutura nao mantém os elementos totalmente ordenados, apenas parcialmente. Percorrer em ordem exige remover vários elementos ou usar outra estrutura de apoio.
- Operações como remoção de elementos internos ou atualização de prioridades exigem localizar o item primeiro, o que volta ao custo linear.
- Para conjuntos muito pequenos, o custo constante das trocas pode ser maior que o de uma lista simples.

## 2. Programa de manutenção da heap

O arquivo `heap_utils.py` implementa a classe `MaxHeap`, que oferece:
- `insert(valor)`: insere com correção via bubble-up, levando o maior valor para cima.
- `remove()`: remove a raiz (maior elemento) e reorganiza com bubble-down.
- `list_values()`: retorna o estado interno do vetor.
- `contains(valor)`: busca linear simples.
- `is_empty()`: indica se a heap está vazia.

A funcao `demonstrate_heap_operations()` do arquivo `main.py` aciona esses métodos e mostra o comportamento da estrutura.

## 3. HeapSort

### 3.a Funcionamento
1. Transformamos o vetor inicial em uma max-heap, garantindo que cada nó seja maior que seus filhos.
2. Trocamos a raiz (maior elemento) com o último elemento da área útil do vetor.
3. Reduzimos o limite da area útil em uma posição e restabelecemos a propriedade de max-heap a partir da raiz.
4. Repetimos o processo ate que toda a area útil seja de tamanho 1.

### 3.b Uso da propriedade de heap
- A raiz de uma max-heap contém sempre o maior elemento da porção ainda nao ordenada.
- Após mover a raiz para o final do vetor, a propriedade de heap garante que o próximo maior elemento suba para a raiz depois do heapify.
- Esse reuso da propriedade mantém a maior prioridade acessível a cada passo, permitindo ordenar o vetor in-place.

### 3.c Implementação

```python
def heapsort(values):
    copied_values = list(values)
    size = len(copied_values)
    _build_max_heap(copied_values, size)
    for end in range(size - 1, 0, -1):
        copied_values[0], copied_values[end] = copied_values[end], copied_values[0]
        _heapify_down(copied_values, 0, end)
    return copied_values
```

As funcoes auxiliares `_build_max_heap` e `_heapify_down` tambem estao em `heap_utils.py`.

### 3.d Complexidade

1. Construcao da max-heap: para cada posição que atua como pai, aplicamos `_heapify_down`. O custo total é `O(n)` porque os niveis mais profundos tem mais nós porem subárvores menores.
2. Laço principal: executa `n - 1` iterações.
   - Cada iteração realiza uma troca `O(1)` e um `_heapify_down` com custo `O(log n)` (altura da heap).
   - Custo do laço: `(n - 1) * O(log n)` -> `O(n log n)`.
3. Somando as etapas: `O(n) + O(n log n)` -> complexidade total `O(n log n)`.
4. Espaco auxiliar adicional é `O(1)` porque a ordenação ocorre sobre o próprio vetor.

## 4. Combinacao de k listas ordenadas

### Ideia
- Inserimos o último elemento de cada lista (maior daquela lista) na max-heap para inicializar a estrutura, guardando também de qual lista e posição veio.
- Repetimos: removemos o maior elemento da heap (raiz), adicionamos a um vetor auxiliar em ordem decrescente e inserimos o próximo maior valor (da mesma lista de origem daquele elemento) na heap.
- Ao final invertemos o vetor auxiliar para obter a lista final em ordem crescente.
- A complexidade continua sendo `O(N log k)`, onde `N` e o total de elementos das listas.

### Implementação

```python
from heap_utils import MaxHeap

def merge_sorted_lists(sorted_lists):
    heap = MaxHeap()
    resultado_decrescente = []
    for list_id, values in enumerate(sorted_lists):
        if values:
            last_index = len(values) - 1
            heap.insert((values[last_index], list_id, last_index))
    while not heap.is_empty():
        packed_value = heap.remove()
        if packed_value is None:
            break
        value, list_id, element_index = packed_value
        resultado_decrescente.append(value)
        next_index = element_index - 1
        if next_index >= 0:
            next_value = sorted_lists[list_id][next_index]
            heap.insert((next_value, list_id, next_index))
    resultado_decrescente.reverse()
    return resultado_decrescente
```

### Demonstração prática

Saida relevante do script `python3 main.py`:

```
=== Demonstracao da manutencao da max-heap ===
Numeros inseridos: [42, 29, 18, 14, 7, 18, 12, 11, 13]
Estado interno da heap: [42, 29, 18, 14, 7, 18, 12, 11, 13]
Heap esta vazia? False
A heap contem o valor 18? True
A heap contem o valor 30? False
Maior valor removido (1a remocao): 42
Maior valor removido (2a remocao): 29
Estado interno apos remocoes: [18, 14, 18, 13, 7, 11, 12]
Heap esta vazia? False

=== Demonstracao do HeapSort ===
Vetor original: [21, 1, 45, 78, 3, 5]
Vetor ordenado: [1, 3, 5, 21, 45, 78]

=== Demonstracao da combinacao de listas ordenadas com max-heap ===
Listas de entrada: [[1, 4, 9], [2, 3, 8], [0, 5, 7, 10]]
Lista final combinada: [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]
```

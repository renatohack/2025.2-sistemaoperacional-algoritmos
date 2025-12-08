import heapq
from q5_coordenadas import EDGES


def construir_grafo(arestas):
    """
    Monta um grafo nao direcionado em lista de adjacencia.
    Cada chave e um vertice, e o valor e uma lista de pares (peso, vizinho).
    """
    grafo = {}
    for origem, destino, peso in arestas:
        if origem not in grafo:
            grafo[origem] = []
        if destino not in grafo:
            grafo[destino] = []
        grafo[origem].append((peso, destino))
        grafo[destino].append((peso, origem))
    return grafo


def dijkstra(grafo, inicio, fim):
    """
    Algoritmo de Dijkstra com heapq para encontrar o menor caminho.

    Ideia:
    - Mantemos uma fila de prioridades (heap) com pares (custo_atual, vertice).
    - Sempre expandimos o vertice de menor custo acumulado ate agora.
    - Atualizamos distancias para vizinhos quando encontramos um caminho melhor.
    - Paramos quando esvaziar a fila ou quando o destino for extraido.
    """
    dist = {vertice: float("inf") for vertice in grafo}
    anterior = {vertice: None for vertice in grafo}
    dist[inicio] = 0

    heap = [(0, inicio)]

    while heap:
        custo_atual, vertice = heapq.heappop(heap)

        if custo_atual > dist[vertice]:
            continue  # Ja temos caminho melhor registrado; descartamos este.

        if vertice == fim:
            break  # Ja chegamos ao destino com o menor custo possivel.

        for peso, vizinho in grafo.get(vertice, []):
            novo_custo = custo_atual + peso
            if novo_custo < dist[vizinho]:
                dist[vizinho] = novo_custo
                anterior[vizinho] = vertice
                heapq.heappush(heap, (novo_custo, vizinho))

    return dist, anterior


def reconstruir_caminho(anterior, inicio, fim):
    """
    Remonta o caminho do fim ate o inicio usando o dicionario 'anterior'.
    Se nao houver caminho, retorna lista vazia.
    """
    if anterior[fim] is None and inicio != fim:
        return []

    caminho = [fim]
    atual = fim
    while atual != inicio:
        atual = anterior[atual]
        if atual is None:
            return []
        caminho.append(atual)
    caminho.reverse()
    return caminho


def main():
    grafo = construir_grafo(EDGES)
    origem = "a"
    destino = "z"

    distancias, anterior = dijkstra(grafo, origem, destino)
    caminho = reconstruir_caminho(anterior, origem, destino)

    if not caminho:
        print(f"Nao foi encontrado caminho de {origem} ate {destino}.")
        return

    custo_total = distancias[destino]
    print("Caminho minimo de a ate z (Dijkstra):")
    print(" ", " -> ".join(caminho))
    print(f"Custo total: {custo_total}")


if __name__ == "__main__":
    main()

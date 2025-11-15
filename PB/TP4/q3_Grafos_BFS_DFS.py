"""
Q3 - Grafo (sem pesos) com DFS e BFS.

Objetivo:
- DFS (todos os caminhos entre duas cidades/vértices)
- BFS (menor caminho em número de arestas entre duas cidades)

Usaremos um grafo não ponderado (lista de adjacência) e as funções pedidas.
"""

from collections import deque


class Graph:
    """Grafo simples não direcionado usando dicionário de adjacência."""

    def __init__(self):
        self.adj = {}

    def add_vertex(self, v):
        # Adiciona um vértice ao grafo
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, a, b):
        # Adiciona aresta não direcionada entre a e b
        if a not in self.adj:
            self.adj[a] = []
        if b not in self.adj:
            self.adj[b] = []
        self.adj[a].append(b)
        self.adj[b].append(a)

    def dfs(self, start, end):
        """Retorna lista com TODOS os caminhos de start até end usando busca em profundidade.

        Implementação recursiva simples guardando caminho atual e coletando resultados.
        """
        resultados = []

        def _dfs(atual, destino, visitados, caminho):
            visitados.add(atual)
            caminho.append(atual)

            if atual == destino:
                resultados.append(list(caminho))
            else:
                for viz in self.adj.get(atual, []):
                    if viz not in visitados:
                        _dfs(viz, destino, visitados, caminho)

            caminho.pop()
            visitados.remove(atual)

        _dfs(start, end, set(), [])
        return resultados

    def bfs(self, start, end):
        """Retorna o caminho mais curto (em arestas) entre start e end usando BFS.

        Reconstrói o caminho final usando um dicionário de predecessores.
        """
        fila = deque([start])
        visitado = {start}
        predecessor = {start: None}

        while fila:
            atual = fila.popleft()
            if atual == end:
                break
            for viz in self.adj.get(atual, []):
                if viz not in visitado:
                    visitado.add(viz)
                    predecessor[viz] = atual
                    fila.append(viz)

        # Reconstruir caminho
        if end not in predecessor:
            return []
        caminho = []
        cur = end
        while cur is not None:
            caminho.append(cur)
            cur = predecessor[cur]
        caminho.reverse()
        return caminho


if __name__ == "__main__":
    # Exemplo sugerido no enunciado
    graph = Graph()
    for v in ['A', 'B', 'C', 'D', 'E']:
        graph.add_vertex(v)

    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('C', 'D')
    graph.add_edge('C', 'E')
    graph.add_edge('D', 'E')

    print("[Q3] DFS - todos os caminhos de A até D:")
    todos = graph.dfs('A', 'D')
    for caminho in todos:
        print(caminho)

    print("[Q3] BFS - menor caminho de A até E:")
    print(graph.bfs('A', 'E'))


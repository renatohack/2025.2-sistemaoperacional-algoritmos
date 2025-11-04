"""Exemplo simples de grafo não orientado e cálculo de graus de separação."""
from collections import deque


class Grafo:
    def __init__(self):
        self.vizinhos = {}

    def adicionar_usuario(self, usuario):
        if usuario not in self.vizinhos:
            self.vizinhos[usuario] = []

    def adicionar_amizade(self, usuario_a, usuario_b):
        self.adicionar_usuario(usuario_a)
        self.adicionar_usuario(usuario_b)

        if usuario_b not in self.vizinhos[usuario_a]:
            self.vizinhos[usuario_a].append(usuario_b)
        if usuario_a not in self.vizinhos[usuario_b]:
            self.vizinhos[usuario_b].append(usuario_a)


def grau_de_separacao(grafo, origem, destino):
    """Retorna o menor número de saltos entre origem e destino. None se não houver caminho."""
    if origem not in grafo.vizinhos or destino not in grafo.vizinhos:
        return None

    if origem == destino:
        return 0

    visitados = set([origem])
    fila = deque([(origem, 0)])

    while fila:
        usuario_atual, distancia = fila.popleft()

        for vizinho in grafo.vizinhos[usuario_atual]:
            if vizinho == destino:
                return distancia + 1

            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, distancia + 1))

    return None


if __name__ == "__main__":
    grafo = Grafo()

    amizades = [
        ("Ana", "Bruno"),
        ("Ana", "Carla"),
        ("Bruno", "Daniel"),
        ("Carla", "Daniel"),
        ("Daniel", "Eduardo"),
        ("Eduardo", "Fernanda"),
        ("Fernanda", "Guilherme"),
        ("Guilherme", "Helena"),
        ("Carla", "Fernanda"),
    ]

    for a, b in amizades:
        grafo.adicionar_amizade(a, b)

    testes = [
        ("Ana", "Daniel"),
        ("Ana", "Fernanda"),
        ("Bruno", "Helena"),
        ("Ana", "Ana"),
        ("Helena", "João"),  # João não está na rede
    ]

    for origem, destino in testes:
        distancia = grau_de_separacao(grafo, origem, destino)
        print(f"Distância entre {origem} e {destino}: {distancia}")

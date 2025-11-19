import heapq
from collections import defaultdict

# Arestas com pesos (distancias) conforme o desenho do grafo.
# Sinta-se livre para ajustar valores se precisar seguir outra fonte.
EDGES = [
    ("Coruna", "Vigo", 171),
    ("Coruna", "Valladolid", 455),
    ("Vigo", "Valladolid", 356),
    ("Valladolid", "Bilbao", 280),
    ("Valladolid", "Madrid", 193),
    ("Bilbao", "Oviedo", 304),
    ("Bilbao", "Madrid", 395),
    ("Bilbao", "Zaragoza", 324),
    ("Madrid", "Zaragoza", 325),
    ("Madrid", "Badajoz", 403),
    ("Madrid", "Jaen", 335),
    ("Madrid", "Albacete", 251),
    ("Zaragoza", "Barcelona", 296),
    ("Barcelona", "Gerona", 100),
    ("Barcelona", "Valencia", 349),
    ("Valencia", "Murcia", 241),
    ("Valencia", "Albacete", 191),
    ("Murcia", "Albacete", 150),
    ("Murcia", "Granada", 278),
    ("Granada", "Sevilla", 256),
    ("Granada", "Jaen", 99),
    ("Sevilla", "Jaen", 242),
    ("Sevilla", "Cadiz", 125)
]


def build_graph():
    graph = defaultdict(list)
    for a, b, w in EDGES:
        graph[a].append((b, w))
        graph[b].append((a, w))
    return graph


def normalize_city(name: str):
    return name.strip().lower()


def dijkstra(graph, start, goal):
    """Retorna (distancia, caminho) ou (None, None) se nao houver caminho."""
    distances = {start: 0}
    predecessors = {start: None}
    priority_queue = [(0, start)]  # (distancia acumulada, cidade)

    while priority_queue:
        current_distance, current_city = heapq.heappop(priority_queue)
        if current_city == goal:
            break
        if current_distance != distances.get(current_city, float("inf")):
            continue
        for neighbor_city, edge_distance in graph[current_city]:
            candidate_distance = current_distance + edge_distance
            if candidate_distance < distances.get(neighbor_city, float("inf")):
                distances[neighbor_city] = candidate_distance
                predecessors[neighbor_city] = current_city
                heapq.heappush(priority_queue, (candidate_distance, neighbor_city))
    else:
        return None, None

    # Reconstrucao do caminho
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = predecessors[cur]
    path.reverse()
    return distances[goal], path


def escolher_cidade(validas):
    nomes = sorted(validas)
    normalizado = {normalize_city(n): n for n in validas}
    print("Cidades disponiveis:")
    print(", ".join(nomes))
    while True:
        cidade = input("Digite o nome da cidade: ").strip()
        key = normalize_city(cidade)
        if key in normalizado:
            return normalizado[key]
        print("Cidade invalida, tente novamente.")


def main():
    graph = build_graph()
    cidades = set(graph.keys())
    print("=== Rota mais curta com Dijkstra (Grafo Espanha) ===")
    print()
    print("Ponto de partida:")
    start = escolher_cidade(cidades)
    print("Destino:")
    goal = escolher_cidade(cidades)

    if start == goal:
        print("Partida e destino sao a mesma cidade. Distancia 0.")
        return

    total_distance, best_path = dijkstra(graph, start, goal)
    if total_distance is None:
        print("Nao existe caminho entre as cidades selecionadas.")
        return

    print(f"\nMelhor rota: {' -> '.join(best_path)}")
    print(f"Distancia total: {total_distance} km")


if __name__ == "__main__":
    main()

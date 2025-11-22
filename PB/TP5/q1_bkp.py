import math
import matplotlib.pyplot as plt


def build_graph():
    cities = ["A", "B", "C", "D", "E", "F"]
    dist_matrix = [
        [0, 10, 5, 7, 3, 2],
        [10, 0, 8, 4, 6, 9],
        [5, 8, 0, 1, 2, 3],
        [7, 4, 1, 0, 5, 6],
        [3, 6, 2, 5, 0, 4],
        [2, 9, 3, 6, 4, 0],
    ]

    graph = {}
    size = len(cities)
    for i in range(size):
        city_i = cities[i]
        graph[city_i] = {}
        for j in range(size):
            if i == j:
                continue
            city_j = cities[j]
            graph[city_i][city_j] = dist_matrix[i][j]
    return graph, cities


def dijkstra(graph, source):
    dist = {}
    prev = {}
    unvisited = set(graph.keys())

    for node in graph:
        dist[node] = math.inf
        prev[node] = None
    dist[source] = 0

    # Busca repetida pelo nó não visitado com menor distância
    while unvisited:
        current = None
        current_dist = math.inf
        for node in unvisited:
            if dist[node] < current_dist:
                current_dist = dist[node]
                current = node

        if current is None:
            break

        unvisited.remove(current)

        for neighbor, weight in graph[current].items():
            if neighbor not in unvisited:
                continue
            new_dist = dist[current] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current

    return dist, prev


def build_paths(prev, source):
    paths = {}
    for node in prev:
        if node == source:
            paths[node] = [source]
            continue

        # Reconstrói caminho voltando pelos predecessores
        path = []
        current = node
        while current is not None:
            path.append(current)
            if current == source:
                break
            current = prev[current]
        paths[node] = list(reversed(path))
    return paths


def build_tree_edges(prev):
    edges = []
    for node, parent in prev.items():
        if parent is None:
            continue
        edges.append((parent, node))
    return edges


def plot_tree(cities, edges, graph, output_path="arvore_geradora.png"):
    # Posiciona nós em círculo simples
    pos = {}
    total = len(cities)
    radius = 1.0
    for idx, city in enumerate(cities):
        angle = 2 * math.pi * idx / total
        pos[city] = (radius * math.cos(angle), radius * math.sin(angle))

    plt.figure(figsize=(6, 6))
    for u, v in edges:
        x_values = [pos[u][0], pos[v][0]]
        y_values = [pos[u][1], pos[v][1]]
        plt.plot(x_values, y_values, color="#555555")

        # Mostra peso no meio da aresta
        mid_x = (pos[u][0] + pos[v][0]) / 2
        mid_y = (pos[u][1] + pos[v][1]) / 2
        weight = graph[u][v]
        plt.text(mid_x, mid_y, str(weight), color="darkred", fontsize=9, ha="center", va="center")

    for city, (x, y) in pos.items():
        plt.scatter(x, y, color="#4c72b0", s=500)
        plt.text(x, y, city, color="white", ha="center", va="center", fontsize=12, fontweight="bold")

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def main():
    graph, cities = build_graph()
    source = "A"

    dist, prev = dijkstra(graph, source)
    paths = build_paths(prev, source)

    print("Menores distancias a partir de A:")
    for city in sorted(dist.keys()):
        print(f"A -> {city}: {dist[city]} via {paths[city]}")

    tree_edges = build_tree_edges(prev)
    image_path = plot_tree(cities, tree_edges, graph)
    print(f"\nArvore geradora (caminhos minimos) salva em: {image_path}")


if __name__ == "__main__":
    main()

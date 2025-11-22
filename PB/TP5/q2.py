import math
import matplotlib.pyplot as plt


def build_graph():
    cities = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    dist_matrix = [
        [0, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [20, 0, 40, 50, 60, 70, 80, 90, 100, 110],
        [30, 40, 0, 60, 70, 80, 90, 100, 110, 120],
        [40, 50, 60, 0, 80, 90, 100, 110, 120, 130],
        [50, 60, 70, 80, 0, 100, 110, 120, 130, 140],
        [60, 70, 80, 90, 100, 0, 120, 130, 140, 150],
        [70, 80, 90, 100, 110, 120, 0, 140, 150, 160],
        [80, 90, 100, 110, 120, 130, 140, 0, 160, 170],
        [90, 100, 110, 120, 130, 140, 150, 160, 0, 180],
        [100, 110, 120, 130, 140, 150, 160, 170, 180, 0],
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


def nearest_neighbor(graph, cities, start="A"):
    # Começa em start e sempre vai para o vizinho mais próximo não visitado
    unvisited = set(cities)
    tour = [start]
    unvisited.remove(start)
    total_distance = 0

    current = start
    while unvisited:
        next_city = None
        best_dist = math.inf
        for city in unvisited:
            d = graph[current][city]
            if d < best_dist:
                best_dist = d
                next_city = city
        tour.append(next_city)
        total_distance += best_dist
        unvisited.remove(next_city)
        current = next_city

    # Volta para o início para fechar o ciclo
    total_distance += graph[current][start]
    tour.append(start)
    return tour, total_distance


def plot_tour(cities, tour, graph, output_path="caminho_vizinho_mais_proximo.png"):
    # Posiciona nós em círculo para visualização simples
    pos = {}
    total = len(cities)
    radius = 1.0
    for idx, city in enumerate(cities):
        angle = 2 * math.pi * idx / total
        pos[city] = (radius * math.cos(angle), radius * math.sin(angle))

    plt.figure(figsize=(7, 7))

    # Desenha arestas na ordem visitada
    for i in range(len(tour) - 1):
        u = tour[i]
        v = tour[i + 1]
        x_values = [pos[u][0], pos[v][0]]
        y_values = [pos[u][1], pos[v][1]]
        plt.plot(x_values, y_values, color="#555555", zorder=1)

        # Anota peso no meio da aresta
        mid_x = (pos[u][0] + pos[v][0]) / 2
        mid_y = (pos[u][1] + pos[v][1]) / 2
        weight = graph[u][v]
        plt.text(mid_x, mid_y, str(weight), color="darkred", fontsize=8, ha="center", va="center", zorder=3)

    # Desenha nós e etiquetas
    for idx, city in enumerate(tour[:-1]):  # ignora último A duplicado na contagem
        x, y = pos[city]
        plt.scatter(x, y, color="#4c72b0", s=500, zorder=2)
        plt.text(x, y, city, color="white", ha="center", va="center", fontsize=12, fontweight="bold", zorder=4)
        # Marca ordem de visita um pouco acima do nó
        plt.text(x, y + 0.08, f"{idx+1}", color="black", ha="center", va="bottom", fontsize=9, zorder=5)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def main():
    graph, cities = build_graph()
    tour, total_distance = nearest_neighbor(graph, cities, start="A")

    print("Ordem de visita (vizinho mais proximo):")
    print(" -> ".join(tour))
    print(f"Distancia total: {total_distance}")

    image_path = plot_tour(cities, tour, graph)
    print(f"Grafico salvo em: {image_path}")


if __name__ == "__main__":
    main()

from collections import defaultdict, deque

# Lista de arestas nao direcionadas (pesos ignorados para BFS/DFS)
EDGES = [
    ("Albany", "Champlain"),
    ("Albany", "Newburgh"),
    ("Albany", "Springfield"),
    ("Newburgh", "New York"),
    ("Newburgh", "Hartford"),
    ("New York", "New Haven"),
    ("New Haven", "Hartford"),
    ("New Haven", "Providence"),
    ("Hartford", "Springfield"),
    ("Hartford", "Sturbridge"),
    ("Springfield", "Sturbridge"),
    ("Springfield", "White River Jct."),
    ("White River Jct.", "Highgate Springs"),
    ("White River Jct.", "St. Johnsbury"),
    ("White River Jct.", "Concord"),
    ("St. Johnsbury", "Derby Line"),
    ("St. Johnsbury", "Concord"),
    ("Concord", "Reading"),
    ("Sturbridge", "Weston"),
    ("Providence", "Canton"),
    ("Reading", "Weston"),
    ("Reading", "Boston"),
    ("Reading", "Bangor"),
    ("Weston", "Boston"),
    ("Weston", "Canton"),
    ("Canton", "Boston"),
    ("Bangor", "Houlton"),
]


def build_graph():
    """Monta uma lista de adjacencia ordenada alfabeticamente para cada cidade."""
    graph = defaultdict(list)
    for a, b in EDGES:
        graph[a].append(b)
        graph[b].append(a)
    for neighbors in graph.values():
        neighbors.sort()
    return graph


def bfs(graph, start, goal):
    """BFS que para ao encontrar goal e reconstrui o caminho mais curto (arestas nao ponderadas)."""
    visited = []
    queue = deque([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        visited.append(node)
        if node == goal:
            break
        for neighbor in graph[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
    else:
        return visited, None  # nao ha caminho

    # reconstrucao do caminho
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return visited, path


def dfs(graph, start, goal):
    """DFS (iterativa) que para ao encontrar goal e reconstrui o caminho achado (nao necessariamente o mais curto)."""
    visited = []
    stack = [(start, None)]  # (nodo, pai)
    parent = {}

    while stack:
        node, par = stack.pop()
        if node in parent:
            continue
        parent[node] = par
        visited.append(node)
        if node == goal:
            break
        # percorre em ordem alfabetica; stack e LIFO, por isso insere na ordem inversa
        for neighbor in reversed(graph[node]):
            stack.append((neighbor, node))
    else:
        return visited, None  # nao ha caminho

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return visited, path


if __name__ == "__main__":
    graph = build_graph()
    start = "Champlain"
    goal = "Houlton"

    bfs_order, bfs_path = bfs(graph, start, goal)
    dfs_order, dfs_path = dfs(graph, start, goal)

    #print("Sequencia BFS (visita):")
    #print(" -> ".join(bfs_order))
    print("Caminho mais curto BFS:")
    print(" -> ".join(bfs_path) if bfs_path else "Nao ha caminho")

    #print("\nSequencia DFS (visita):")
    #print(" -> ".join(dfs_order))
    print("Caminho encontrado DFS:")
    print(" -> ".join(dfs_path) if dfs_path else "Nao ha caminho")

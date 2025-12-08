import matplotlib

matplotlib.use("Agg")

import math
import matplotlib.pyplot as plt
import networkx as nx
from q2_coordenadas import EDGES


def construir_grafo(lista_arestas):
    """Cria um grafo nao direcionado a partir das arestas fornecidas."""
    grafo = {}
    for origem, destino in lista_arestas:
        if origem not in grafo:
            grafo[origem] = []
        if destino not in grafo:
            grafo[destino] = []

        grafo[origem].append(destino)
        grafo[destino].append(origem)

    return grafo


def bfs_encontrar_caminho(grafo, inicio, fim):
    """Busca em largura: garante o caminho mais curto em numero de passos."""
    fila = [inicio]
    visitados = set([inicio])
    anterior = {}

    while fila:
        atual = fila.pop(0)
        if atual == fim:
            break

        for vizinho in grafo.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                anterior[vizinho] = atual
                fila.append(vizinho)

    if fim not in visitados:
        return []

    caminho = [fim]
    while caminho[-1] != inicio:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


def dfs_encontrar_caminho(grafo, inicio, fim):
    """Busca em profundidade: explora um caminho ate nao poder mais."""
    pilha = [inicio]
    visitados = set([inicio])
    anterior = {}

    while pilha:
        atual = pilha.pop()
        if atual == fim:
            break

        for vizinho in grafo.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                anterior[vizinho] = atual
                pilha.append(vizinho)

    if fim not in visitados:
        return []

    caminho = [fim]
    while caminho[-1] != inicio:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


def imprimir_caminho(titulo, caminho):
    print(titulo)
    if not caminho:
        print("  Nenhum caminho encontrado.")
        return
    print("  Passos:", " -> ".join(str(no) for no in caminho))
    print("  Tamanho do caminho:", len(caminho) - 1, "movimentos")


def gerar_imagem_grafo(grafo, caminho_destacado, nome_arquivo):
    """Gera uma imagem PNG do grafo, destacando o caminho indicado."""
    grafo_nx = nx.Graph()
    for origem, vizinhos in grafo.items():
        for destino in vizinhos:
            grafo_nx.add_edge(origem, destino)

    posicoes = _posicionamento_em_camadas(grafo_nx)

    caminho_arestas = set()
    for i in range(len(caminho_destacado) - 1):
        par = caminho_destacado[i], caminho_destacado[i + 1]
        par_ordenado = tuple(sorted(par))
        caminho_arestas.add(par_ordenado)

    cores_arestas = []
    for origem, destino in grafo_nx.edges():
        par_ordenado = tuple(sorted((origem, destino)))
        if par_ordenado in caminho_arestas:
            cores_arestas.append("red")
        else:
            cores_arestas.append("lightgray")

    cores_nos = []
    for no in grafo_nx.nodes():
        if caminho_destacado:
            if no == caminho_destacado[0]:
                cores_nos.append("green")
            elif no == caminho_destacado[-1]:
                cores_nos.append("red")
            elif no in caminho_destacado:
                cores_nos.append("orange")
            else:
                cores_nos.append("lightblue")
        else:
            cores_nos.append("lightblue")

    fig, eixo = plt.subplots(figsize=(18, 12))
    nx.draw_networkx_edges(
        grafo_nx,
        posicoes,
        ax=eixo,
        edge_color=cores_arestas,
        width=1.1,
        alpha=0.5,
    )
    nx.draw_networkx_nodes(
        grafo_nx,
        posicoes,
        ax=eixo,
        node_color=cores_nos,
        node_size=320,
        edgecolors="black",
        linewidths=0.6,
    )
    nx.draw_networkx_labels(grafo_nx, posicoes, ax=eixo, font_size=7)

    eixo.set_title("Grafo do labirinto (nodos 0 a 71)")
    eixo.axis("off")
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300)
    plt.close(fig)


def _posicionamento_em_camadas(grafo_nx):
    """Organiza os nós por camadas de BFS a partir da entrada (0)."""
    inicio = 0
    distancias = {inicio: 0}
    fila = [inicio]
    while fila:
        atual = fila.pop(0)
        for vizinho in grafo_nx.neighbors(atual):
            if vizinho not in distancias:
                distancias[vizinho] = distancias[atual] + 1
                fila.append(vizinho)

    camadas = {}
    for no, dist in distancias.items():
        camadas.setdefault(dist, []).append(no)

    pos = {}
    distancia_max = max(camadas.keys())
    espacamento_y = 1.5
    espacamento_x = 1.2

    for camada, nos in camadas.items():
        largura = (len(nos) - 1) * espacamento_x
        inicio_x = -largura / 2
        for indice, no in enumerate(sorted(nos)):
            x = inicio_x + indice * espacamento_x
            y = -camada * espacamento_y
            pos[no] = (x, y)

    # Caso haja nós não alcançáveis, posiciona no final
    nao_alcancados = set(grafo_nx.nodes()) - set(pos.keys())
    if nao_alcancados:
        camada_extra = distancia_max + 1
        largura = (len(nao_alcancados) - 1) * espacamento_x
        inicio_x = -largura / 2
        for indice, no in enumerate(sorted(nao_alcancados)):
            x = inicio_x + indice * espacamento_x
            y = -camada_extra * espacamento_y
            pos[no] = (x, y)

    return pos


def main():
    """Executa BFS e DFS no labirinto e mostra o caminho encontrado."""
    grafo_labirinto = construir_grafo(EDGES)
    entrada = 0
    saida = 71

    caminho_bfs = bfs_encontrar_caminho(grafo_labirinto, entrada, saida)
    caminho_dfs = dfs_encontrar_caminho(grafo_labirinto, entrada, saida)

    print(
        "Cada ponto do labirinto foi numerado de 0 (entrada) a 71 (saida). "
        "A imagem do grafo sera salva em q2_coordenadas.png."
    )
    imprimir_caminho("Caminho encontrado com BFS:", caminho_bfs)
    imprimir_caminho("Caminho encontrado com DFS:", caminho_dfs)

    gerar_imagem_grafo(grafo_labirinto, caminho_bfs, "q2_coordenadas.png")
    print("\nImagem do grafo gerada em q2_coordenadas.png.")

    if caminho_bfs and caminho_dfs:
        if caminho_bfs == caminho_dfs:
            print("\nAmbos chegaram ao mesmo caminho, como esperado (apenas uma saida).")
        else:
            print("\nBFS e DFS chegaram a caminhos diferentes, mas ambos levam a saida.")
    else:
        print("\nNao foi possivel encontrar um caminho com uma das buscas.")

    print(
        "\nGarantia de melhor caminho: a BFS retorna o caminho mais curto em numero de arestas"
        " porque expande nivel por nivel a partir da entrada. Em um grafo sem pesos,"
        " isso significa o menor numero de movimentos ate a saida."
    )


if __name__ == "__main__":
    main()

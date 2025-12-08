import heapq
import matplotlib

# Backend "Agg" permite salvar a figura em PNG sem precisar de display
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
from q4_coordenadas import EDGES


def construir_grafo(arestas):
    """Cria um grafo nao direcionado a partir da lista de arestas (u, v, peso)."""
    grafo = {}
    for origem, destino, peso in arestas:
        # Garante que cada nodo apareca no dicionario
        if origem not in grafo:
            grafo[origem] = []
        if destino not in grafo:
            grafo[destino] = []
        # Adiciona aresta nas duas direcoes, pois o grafo e nao direcionado
        grafo[origem].append((peso, destino))
        grafo[destino].append((peso, origem))
    return grafo


def prim_mst(grafo, inicio):
    """
    Implementacao do algoritmo de Prim usando heapq.

    Ideia geral:
    - Comecamos em um nodo qualquer (inicio) e marcamos como visitado.
    - Mantemos uma fila de prioridades (heap) com todas as arestas que saem
      do conjunto de nos ja visitados.
    - Repetidamente, escolhemos a aresta de menor custo que conecta um no
      visitado a um no ainda nao visitado. Adicionamos essa aresta à MST.
    - Continuamos ate visitar todos os nos ou acabar as arestas.
    """
    visitados = set([inicio])
    arestas_escolhidas = []
    custo_total = 0

    # Heap com as arestas que saem do conjunto visitado.
    # Cada item: (peso, origem, destino)
    heap = []
    for peso, vizinho in grafo[inicio]:
        heapq.heappush(heap, (peso, inicio, vizinho))

    while heap:
        peso, origem, destino = heapq.heappop(heap)
        if destino in visitados:
            continue  # Ignoramos arestas que voltam para nos ja visitados

        # Escolhemos essa aresta para a MST
        visitados.add(destino)
        arestas_escolhidas.append((origem, destino, peso))
        custo_total += peso

        # Adicionamos novas arestas que saem do novo no visitado
        for peso_vizinho, outro in grafo[destino]:
            if outro not in visitados:
                heapq.heappush(heap, (peso_vizinho, destino, outro))

    return arestas_escolhidas, custo_total


def gerar_imagem_grafo(grafo, mst_arestas, nome_arquivo="q4_mst.png"):
    """
    Desenha o grafo e destaca as arestas que compoem a MST.

    - Usa networkx para montar o grafo.
    - Usa spring_layout para posicionar os nos.
    - Arestas da MST ficam em vermelho; demais em cinza claro.
    - Salva a figura em PNG.
    """
    grafo_nx = nx.Graph()

    # Adiciona arestas com pesos ao grafo do networkx
    for origem, vizinhos in grafo.items():
        for peso, destino in vizinhos:
            grafo_nx.add_edge(origem, destino, weight=peso)

    # Cria um conjunto com as arestas da MST para colorir
    mst_normalizadas = set()
    for origem, destino, peso in mst_arestas:
        chave = tuple(sorted((origem, destino)))
        mst_normalizadas.add(chave)

    # Calcula posicoes; seed fixa o layout para repetibilidade
    pos = nx.spring_layout(grafo_nx, seed=7, k=0.4, iterations=200)

    # Determina cores e larguras das arestas
    cores_arestas = []
    larguras = []
    for u, v in grafo_nx.edges():
        chave = tuple(sorted((u, v)))
        if chave in mst_normalizadas:
            cores_arestas.append("red")
            larguras.append(2.5)
        else:
            cores_arestas.append("lightgray")
            larguras.append(1.2)

    # Desenha o grafo
    fig, ax = plt.subplots(figsize=(12, 10))
    nx.draw_networkx_nodes(
        grafo_nx, pos, ax=ax, node_size=900, node_color="lightblue", edgecolors="black"
    )
    nx.draw_networkx_edges(
        grafo_nx, pos, ax=ax, edge_color=cores_arestas, width=larguras, alpha=0.8
    )
    nx.draw_networkx_labels(grafo_nx, pos, ax=ax, font_size=9, font_weight="bold")

    # Rotula arestas com peso para facilitar leitura
    etiquetas = nx.get_edge_attributes(grafo_nx, "weight")
    nx.draw_networkx_edge_labels(
        grafo_nx, pos, edge_labels=etiquetas, font_size=8, ax=ax
    )

    ax.set_title("Arvore Geradora Minima (Prim)")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300)
    plt.close(fig)


def main():
    # Construcao do grafo a partir das arestas do arquivo
    grafo = construir_grafo(EDGES)

    # Escolhemos um ponto inicial arbitrario (o algoritmo de Prim funciona de qualquer no)
    inicio = next(iter(grafo.keys()))

    # Executa Prim
    mst_arestas, mst_custo = prim_mst(grafo, inicio)

    # Impressao dos segmentos selecionados
    print("Segmentos escolhidos para a arvore geradora minima (Prim):")
    for origem, destino, peso in mst_arestas:
        print(f" {origem} -- {destino} : {peso}")

    print(f"\nCusto total minimo do projeto: {mst_custo}")

    # Gera a imagem do grafo destacando a MST
    gerar_imagem_grafo(grafo, mst_arestas, nome_arquivo="q4_mst.png")
    print("\nImagem gerada: q4_mst.png")


if __name__ == "__main__":
    main()

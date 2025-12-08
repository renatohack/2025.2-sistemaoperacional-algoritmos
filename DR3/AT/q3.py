import itertools
import math


CIDADE_COORDENADAS = [
    (10, 10),
    (20, 15),
    (5, 25),
    (30, 5),
    (15, 40),
    (40, 30),
    (25, 35),
    (5, 5),
    (35, 45),
    (45, 15),
]


def distancia(ponto_a, ponto_b):
    dx = ponto_a[0] - ponto_b[0]
    dy = ponto_a[1] - ponto_b[1]
    return math.hypot(dx, dy)


def imprimir_tabela_cidades():
    print("Tabela de cidades (id, X, Y):")
    print(f"{'ID':<5}{'X':>6}{'Y':>6}")
    for indice, (x, y) in enumerate(CIDADE_COORDENADAS):
        print(f"{indice:<5}{x:>6}{y:>6}")
    print()


def construir_matriz_distancias(coordenada_deposito):
    nomes = ["CD"] + [str(i) for i in range(len(CIDADE_COORDENADAS))]
    coordenadas = [coordenada_deposito] + CIDADE_COORDENADAS
    matriz = []
    for origem in coordenadas:
        linha = []
        for destino in coordenadas:
            valor = distancia(origem, destino)
            linha.append(valor)
        matriz.append(linha)
    return nomes, matriz


def imprimir_matriz_distancias(nomes, matriz):
    print("Tabela de distancias (em unidades euclidianas):")
    largura = 7
    header = f"{'De/Para':<{largura}}" + "".join(f"{nome:>{largura}}" for nome in nomes)
    print(header)
    for i, nome_origem in enumerate(nomes):
        linha = f"{nome_origem:<{largura}}"
        for j, _ in enumerate(nomes):
            if i == j:
                linha += f"{'-':>{largura}}"
            else:
                linha += f"{matriz[i][j]:>{largura}.1f}"
        print(linha)
    print()


def calcular_custo_rota(permutacao, coordenada_deposito):
    custo = 0.0
    origem = coordenada_deposito
    for indice_cidade in permutacao:
        destino = CIDADE_COORDENADAS[indice_cidade]
        custo += distancia(origem, destino)
        origem = destino
    custo += distancia(origem, coordenada_deposito)
    return custo


def rotas_melhores_e_piores(coordenada_deposito, quantidade=3):
    total = len(CIDADE_COORDENADAS)
    melhores = []  # lista de tuplas (custo, permutacao)
    piores = []

    for permutacao in itertools.permutations(range(total)):
        custo = calcular_custo_rota(permutacao, coordenada_deposito)

        melhores.append((custo, permutacao))
        melhores.sort(key=lambda x: x[0])
        if len(melhores) > quantidade:
            melhores.pop()

        piores.append((custo, permutacao))
        piores.sort(key=lambda x: x[0], reverse=True)
        if len(piores) > quantidade:
            piores.pop()

    return melhores, piores


def imprimir_rotas(titulo, rotas):
    print(titulo)
    for indice, (custo, perm) in enumerate(rotas, start=1):
        nomes = ["CD"] + [str(i) for i in perm] + ["CD"]
        caminho = " -> ".join(nomes)
        print(f" {indice}. {caminho} | custo = {custo:.2f}")
    print()


def main():
    coordenada_deposito = (12, 12)  # altere aqui para testar outro CD

    imprimir_tabela_cidades()
    nomes, matriz = construir_matriz_distancias(coordenada_deposito)
    imprimir_matriz_distancias(nomes, matriz)

    melhores, piores = rotas_melhores_e_piores(coordenada_deposito, quantidade=3)
    imprimir_rotas("3 melhores rotas (menor custo):", melhores)
    imprimir_rotas("3 piores rotas (maior custo):", piores)


if __name__ == "__main__":
    main()

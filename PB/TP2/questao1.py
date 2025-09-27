"""Questão 1: otimização de soma de quadrados com Numba."""

import time
import numpy as np
from numba import njit, prange


# (a) Implementação original em Python puro.
def soma_quadrados(lista):
    """Retorna a soma dos quadrados dos elementos de uma lista."""
    soma = 0
    for num in lista:
        soma += num ** 2
    return soma


# (a) Versão otimizada com o decorador @njit(parallel=True) da Numba.
@njit(parallel=True)
def soma_quadrados_numba(lista):
    """Versão compilada com Numba que paraleliza o loop principal."""
    soma = 0
    for i in prange(len(lista)):
        soma += lista[i] ** 2
    return soma


def medir_tempo(func, dados: np.ndarray, repeticoes: int = 3) -> float:
    """Executa `func` repetidamente para reduzir ruído de medição."""
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        func(dados)
    return (time.perf_counter() - inicio) / repeticoes


'''(b) A Numba compila funções Python para código nativo em tempo de execução. Ao usar
@njit(parallel=True), loops elegíveis são transformados em versões paralelas com
vetorização e divisão de iteração entre múltiplos núcleos, reduzindo o tempo total
de execução em workloads grandes.'''


'''(c) O código no bloco principal mede o tempo médio das versões pura e otimizada
usando o mesmo conjunto de dados para permitir uma comparação direta.'''


'''(d) Resultados medidos no mesmo vetor de 1.000.000 elementos (float64):
Tempo médio Python puro: 0.145054 s
Tempo médio Numba: 0.000219 s
Aceleração estimada: 661.47x
Discussão: a implementação com Numba ficou cerca de 660x mais rápida, pois o loop
foi compilado para código nativo e distribuído em múltiplos núcleos. Já a versão
em Python puro executa cada iteração de forma interpretada, acumulando mais
sobrecarga. Diferenças menores podem surgir entre execuções por conta de ruído de
sistema, mas a vantagem da Numba permanece significativa.'''


'''(e) Vantagens da Numba: facilidade de uso (decoradores), manutenção simples
mesmo com código Python idiomático e boa portabilidade enquanto depender apenas da
biblioteca. Já abordagens com threads/processos exigem mais código, sincronização e
compreensão profunda de concorrência. 
Desvantagens: necessidade de tipos suportados 
pela Numba, compilação JIT inicial e menor controle fino sobre o escalonamento em
comparação com APIs paralelas explícitas.'''


if __name__ == "__main__":
    # (c) Conjunto de dados compartilhado pelas medições.
    tamanho = 1_000_000
    dados = np.arange(tamanho, dtype=np.float64)

    # Aquecimento para compilar a função Numba antes da medição real.
    soma_quadrados_numba(dados)

    tempo_python = medir_tempo(soma_quadrados, dados.tolist())
    tempo_numba = medir_tempo(soma_quadrados_numba, dados)

    print(f"Dados: vetor com {tamanho} elementos de float64")
    print(f"Tempo médio Python puro: {tempo_python:.6f} s")
    print(f"Tempo médio Numba: {tempo_numba:.6f} s")
    aceleracao = tempo_python / tempo_numba if tempo_numba else float('inf')
    print(f"Aceleração estimada: {aceleracao:.2f}x")
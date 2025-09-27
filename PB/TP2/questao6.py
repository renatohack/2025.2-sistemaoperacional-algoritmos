"""Questão 6: Fibonacci recursivo vs programação dinâmica."""

import time


# (a) Implementação recursiva direta.
def fibonacci_recursivo(n):
    """Retorna o n-ésimo número de Fibonacci usando recursão pura."""
    if n < 0:
        raise ValueError("n deve ser não negativo")
    if n in (0, 1):
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


'''(b) A abordagem recursiva direta recalcula os mesmos valores muitas vezes. A cada
chamada, expandimos duas chamadas novas, gerando uma árvore de cálculo exponencial:
para n grande, o tempo explode porque os subproblemas Fibonacci(n-1) e Fibonacci(n-2)
voltam a computar os mesmos Fibonacci(k) repetidas vezes.'''


# (c) Versão com programação dinâmica (bottom-up).
def fibonacci_dp(n):
    """Retorna o n-ésimo número de Fibonacci usando abordagem iterativa (DP)."""
    if n < 0:
        raise ValueError("n deve ser não negativo")
    if n in (0, 1):
        return n
    anterior, atual = 0, 1
    for _ in range(2, n + 1):
        anterior, atual = atual, anterior + atual
    return atual


'''(e) Outro problema clássico além de Fibonacci é calcular coeficientes binomiais C(n, k).
A forma recursiva usa C(n, k) = C(n-1, k-1) + C(n-1, k), gerando muitas recomputações.
Com programação dinâmica montamos uma tabela (triângulo de Pascal) em que cada entrada
usa duas já calculadas; assim evitamos recalcular as mesmas combinações várias vezes e o
desempenho deixa de ser exponencial.'''



def medir_tempo(funcao, valor, repeticoes=1):
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        funcao(valor)
    return (time.perf_counter() - inicio) / repeticoes


if __name__ == "__main__":
    valores = [10, 20, 30]

    print("n\tRecursivo (s)\tDP (s)")
    for n in valores:
        tempo_rec = medir_tempo(fibonacci_recursivo, n)
        tempo_dp = medir_tempo(fibonacci_dp, n, repeticoes=1000)
        print(f"{n}\t{tempo_rec:.6f}\t\t{tempo_dp:.9f}")

    '''(d) Os tempos acima exemplificam a diferença: fibonacci_recursivo cresce
    rapidamente ao aumentar n, enquanto fibonacci_dp mantém crescimento linear.
    A repetição 1000 para DP ajuda a medir números muito pequenos. 
    n       Recursivo (s)      DP (s)
    10      0.000025           0.000000509
    20      0.002081           0.000000802
    30      0.258201           0.000001123
    '''

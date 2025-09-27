"""Questão 4: cálculo recursivo de fatorial."""

# (a) Função recursiva para fatorial.
def fatorial(n):
    """Retorna n! para n inteiro não negativo."""
    if n < 0:
        raise ValueError("n deve ser não negativo")
    if n in (0, 1):
        return 1
    return n * fatorial(n - 1)


'''(b) Testes usados: confere fatorial(0), fatorial(1), fatorial(5) e fatorial(7).
A seção main executa essas chamadas e imprime os resultados.'''


'''(c) Complexidade temporal é O(n), pois a função cria uma chamada por nível até 0.
Complexidade espacial também é O(n) porque cada chamada permanece na pilha até as
retornos encadeados concluírem. Uma versão iterativa consegue espaço O(1), então a
recursiva usa mais memória em valores grandes e pode atingir o limite de recursão.'''


'''(d) Exemplo de problema adequado para recursão: percorrer uma árvore (ex.: estrutura
hierárquica de diretórios) visitando cada nó. A recursão vai descendo em cada filho e
retorna ao concluir, o que torna o código natural de ler sem pilhas manuais.'''


'''(e) Vantagens da recursão: código mais curto e alinhado ao raciocínio do problema,
principalmente em estruturas recursivas como árvores. Desvantagens: risco de estouro
de pilha, mais alocação de memória e desempenho inferior quando uma versão iterativa
simples está disponível. Iterações costumam ser mais seguras para entradas grandes.'''


if __name__ == "__main__":
    valores_teste = [0, 1, 5, 7]
    for valor in valores_teste:
        print(f"{valor}! = {fatorial(valor)}")

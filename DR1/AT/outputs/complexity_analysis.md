# Exercicio 2 - Analise de complexidade dos algoritmos de ordenacao

Os cinco algoritmos implementados na Questao 1b apresentam as seguintes caracteristicas teoricas:

Algoritmo | Melhor caso | Caso medio | Pior caso | Espaco auxiliar
--- | --- | --- | --- | ---
Selection Sort | O(n^2) | O(n^2) | O(n^2) | O(1)
Insertion Sort | O(n) | O(n^2) | O(n^2) | O(1)
Bubble Sort | O(n) | O(n^2) | O(n^2) | O(1)
Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n)
Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n)

## Comparacao com os resultados experimentais da Questao 1
- Selection Sort, Insertion Sort e Bubble Sort exibiram crescimento quadratic: ja em n = 20.000 o tempo passou de 8 segundos e em n = 100.000 o Bubble Sort levou cerca de 563 segundos. Esse salto confirma o comportamento O(n^2).
- Merge Sort manteve tempos abaixo de 0,4 segundo mesmo para n = 100.000, alinhado com o custo O(n log n).
- Quick Sort ficou proximo de Merge Sort e terminou em aproximadamente 0,19 segundo para n = 100.000. Como a lista eh aleatoria, obtemos particionamentos razoaveis que refletem o caso medio O(n log n) em vez do pior caso.
- A divisao em graficos separados ajudou a enxergar as duas escalas: os algoritmos quadraticos dispararam, enquanto Merge Sort e Quick Sort cresceram bem mais lentamente.

Conclusao: a analise teorica previa que Selection, Insertion e Bubble seriam impraticaveis em entradas grandes, o que foi confirmado pelo experimento. Merge Sort e Quick Sort permaneceram eficientes ate 100.000 elementos, reforcando a vantagem dos algoritmos O(n log n) nesse tamanho de dados.

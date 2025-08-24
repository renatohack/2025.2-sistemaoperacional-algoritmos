# arquivo: algoritmos_datastructure.py
# Ler "listagem_completa.txt", armazenar em Hashtable, Pilha e Fila,
# recuperar posições 1, 100, 1000, 5000 e última, medir tempo e memória,
# e também medir tempo/memória para adição e remoção de itens.

import time
import tracemalloc
from collections import deque

POSICOES = [1, 100, 1000, 5000, "ultima"]
ARQUIVO_ENTRADA = "listagem_completa.txt"
ARQUIVO_SAIDA = "tempos_estruturas.txt"
QTDE_OPS_ADICAO_REMOCAO = 100


def carregar_listagem(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]


def medir_tempo_memoria(func, *args, **kwargs):
    # mede duração (s) e pico de memória (bytes) da função
    tracemalloc.start()
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    duracao = time.perf_counter() - inicio
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return resultado, duracao, pico


# ---------- Construção das estruturas ----------
def construir_hashtable(lista):
    # Hashtable com chaves iniciando em 1 (facilita acesso por "posição")
    return {i + 1: nome for i, nome in enumerate(lista)}


def construir_pilha(lista):
    # Pilha usando list (topo no final)
    return list(lista)


def construir_fila(lista):
    # Fila usando deque (enqueue append / dequeue popleft)
    return deque(lista)


# ---------- Recuperação de itens ----------
def pegar_hashtable(ht, pos):
    if pos == "ultima":
        return ht.get(len(ht))
    return ht.get(pos)


def pegar_pilha(pilha, pos):
    if pos == "ultima":
        return pilha[-1] if pilha else None
    return pilha[pos - 1] if isinstance(pos, int) and 1 <= pos <= len(pilha) else None


def pegar_fila(fila, pos):
    if pos == "ultima":
        return fila[-1] if fila else None
    return fila[pos - 1] if isinstance(pos, int) and 1 <= pos <= len(fila) else None


def medir_recuperacoes(nome, estrutura, getter):
    registros = []
    for p in POSICOES:
        _, dur, mem = medir_tempo_memoria(getter, estrutura, p)
        registros.append((f"{nome} - get pos {p}", dur, mem))
    return registros


# ---------- Adição e Remoção ----------
def medir_add_remove_hashtable(ht, qtd):
    n = len(ht)

    def adicionar():
        for i in range(1, qtd + 1):
            ht[n + i] = f"novo_{i}"

    def remover():
        for i in range(n + qtd, n, -1):
            ht.pop(i, None)

    _, t_add, m_add = medir_tempo_memoria(adicionar)
    _, t_rem, m_rem = medir_tempo_memoria(remover)
    return [("Hashtable - add", t_add, m_add), ("Hashtable - remove", t_rem, m_rem)]


def medir_add_remove_pilha(pilha, qtd):
    def adicionar():
        for i in range(1, qtd + 1):
            pilha.append(f"novo_{i}")

    def remover():
        for _ in range(qtd):
            if pilha:
                pilha.pop()

    _, t_add, m_add = medir_tempo_memoria(adicionar)
    _, t_rem, m_rem = medir_tempo_memoria(remover)
    return [("Pilha - push", t_add, m_add), ("Pilha - pop", t_rem, m_rem)]


def medir_add_remove_fila(fila, qtd):
    def adicionar():
        for i in range(1, qtd + 1):
            fila.append(f"novo_{i}")

    def remover():
        for _ in range(qtd):
            if fila:
                fila.popleft()

    _, t_add, m_add = medir_tempo_memoria(adicionar)
    _, t_rem, m_rem = medir_tempo_memoria(remover)
    return [("Fila - enqueue", t_add, m_add), ("Fila - dequeue", t_rem, m_rem)]


# ---------- Main ----------
def salvar_metricas(registros, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        for nome, t, m in registros:
            f.write(f"{nome}: {t:.6f} s | pico {m/1024:.1f} KB\n")


if __name__ == "__main__":
    lista = carregar_listagem(ARQUIVO_ENTRADA)
    registros = []

    ht, t, m = medir_tempo_memoria(construir_hashtable, lista)
    registros.append(("Construção Hashtable", t, m))

    pilha, t, m = medir_tempo_memoria(construir_pilha, lista)
    registros.append(("Construção Pilha", t, m))

    fila, t, m = medir_tempo_memoria(construir_fila, lista)
    registros.append(("Construção Fila", t, m))

    registros += medir_recuperacoes("Hashtable", ht, pegar_hashtable)
    registros += medir_recuperacoes("Pilha", pilha, pegar_pilha)
    registros += medir_recuperacoes("Fila", fila, pegar_fila)

    registros += medir_add_remove_hashtable(ht, QTDE_OPS_ADICAO_REMOCAO)
    registros += medir_add_remove_pilha(pilha, QTDE_OPS_ADICAO_REMOCAO)
    registros += medir_add_remove_fila(fila, QTDE_OPS_ADICAO_REMOCAO)

    salvar_metricas(registros, ARQUIVO_SAIDA)

    print("\nMétricas (tempo | pico de memória):")
    for nome, t, m in registros:
        print(f"{nome}: {t:.6f} s | pico {m/1024:.1f} KB")
    print(f"\nTambém salvo em: {ARQUIVO_SAIDA}")

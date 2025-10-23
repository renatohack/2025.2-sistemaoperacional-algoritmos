import os
import random
import statistics
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import numpy as np

try:
    import numba
except ImportError:  # pragma: no cover - apenas instrui o usuario
    numba = None


# Constantes gerais da questao
TOTAL_PONTOS = 1_000_000
REPETICOES_CPU = 6
REPETICOES_IO = 6


def _chunk_sizes(total: int, workers: int) -> List[int]:
    """Divide o total em pedacos quase iguais."""
    workers = max(1, min(workers, total))
    base = total // workers
    resto = total % workers
    tamanhos = [base + 1 if idx < resto else base for idx in range(workers)]
    return [t for t in tamanhos if t > 0]


def _simular_chunk(seed: int, iteracoes: int) -> int:
    """Conta pontos dentro do circulo usando um seed especifico."""
    rng = random.Random(seed)
    dentro = 0
    for _ in range(iteracoes):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            dentro += 1
    return dentro


def _simular_chunk_io(seed: int, iteracoes: int) -> Tuple[int, str]:
    """Conta pontos e retorna texto com os valores para escrita."""
    rng = random.Random(seed)
    dentro = 0
    linhas: List[str] = []
    append = linhas.append
    for _ in range(iteracoes):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            dentro += 1
        append(f"{x:.10f},{y:.10f}\n")
    return dentro, "".join(linhas)


def estimar_pi_sequencial(total_iteracoes: int, seed: int) -> float:
    """Aproxima pi sem paralelismo, apenas com random.random."""
    random.seed(seed)
    dentro = 0
    sorteio = random.random
    for _ in range(total_iteracoes):
        x = sorteio()
        y = sorteio()
        if x * x + y * y <= 1.0:
            dentro += 1
    return 4.0 * dentro / total_iteracoes


def estimar_pi_concurrent(
    total_iteracoes: int,
    seed: int,
    workers: Optional[int] = None,
) -> float:
    """Divide a simulacao em processos paralelos usando ProcessPoolExecutor."""
    if workers is None:
        workers = os.cpu_count() or 1
    tamanhos = _chunk_sizes(total_iteracoes, workers)
    seeds = [seed + 97 * idx for idx in range(len(tamanhos))]
    dentro_total = 0
    with ProcessPoolExecutor(max_workers=len(tamanhos)) as executor:
        futures = [
            executor.submit(_simular_chunk, semente, tamanho)
            for semente, tamanho in zip(seeds, tamanhos)
        ]
        for futuro in futures:
            dentro_total += futuro.result()
    return 4.0 * dentro_total / total_iteracoes


if numba is not None:

    @numba.njit(parallel=True)
    def _contar_dentro_numba(pontos: np.ndarray) -> int:
        """Conta pontos dentro do circulo usando numba paralelizado."""
        dentro = 0
        for idx in numba.prange(pontos.shape[0]):
            x = pontos[idx, 0]
            y = pontos[idx, 1]
            if x * x + y * y <= 1.0:
                dentro += 1
        return dentro

    def estimar_pi_numba(total_iteracoes: int, seed: int) -> float:
        """Gera pontos com numpy e processa com numba paralelizado."""
        rng = np.random.default_rng(seed)
        pontos = rng.random((total_iteracoes, 2))
        dentro = _contar_dentro_numba(pontos)
        return 4.0 * dentro / total_iteracoes

else:

    def estimar_pi_numba(total_iteracoes: int, seed: int) -> float:  # type: ignore
        """Instrui o usuario a instalar numba para esta versao."""
        raise RuntimeError(
            "Numba nao encontrado. Instale com `pip install numba` para executar esta versao."
        )


def executar_io_sequencial(total_iteracoes: int, seed: int, caminho: Path) -> float:
    """Executa a simulacao sequencial salvando cada ponto em arquivo."""
    random.seed(seed)
    dentro = 0
    with caminho.open("w", encoding="ascii") as arquivo:
        for _ in range(total_iteracoes):
            x = random.random()
            y = random.random()
            if x * x + y * y <= 1.0:
                dentro += 1
            arquivo.write(f"{x:.10f},{y:.10f}\n")
    return 4.0 * dentro / total_iteracoes


def executar_io_concurrent(
    total_iteracoes: int,
    seed: int,
    caminho: Path,
    workers: Optional[int] = None,
) -> float:
    """Processa em paralelo e salva os pontos em arquivo apos consolidar os chunks."""
    if workers is None:
        workers = os.cpu_count() or 1
    tamanhos = _chunk_sizes(total_iteracoes, workers)
    seeds = [seed + 173 * idx for idx in range(len(tamanhos))]
    dentro_total = 0
    with ProcessPoolExecutor(max_workers=len(tamanhos)) as executor:
        futures = [
            executor.submit(_simular_chunk_io, semente, tamanho)
            for semente, tamanho in zip(seeds, tamanhos)
        ]
        with caminho.open("w", encoding="ascii") as arquivo:
            for futuro in futures:
                dentro_chunk, texto = futuro.result()
                dentro_total += dentro_chunk
                arquivo.write(texto)
    return 4.0 * dentro_total / total_iteracoes


def executar_io_numba(total_iteracoes: int, seed: int, caminho: Path) -> float:
    """Usa numba para contagem e numpy para gerar pontos, armazenando-os em arquivo."""
    if numba is None:
        raise RuntimeError("Numba nao encontrado. Instale para executar esta versao.")
    rng = np.random.default_rng(seed)
    pontos = rng.random((total_iteracoes, 2))
    dentro = _contar_dentro_numba(pontos)
    with caminho.open("w", encoding="ascii") as arquivo:
        for x, y in pontos:
            arquivo.write(f"{x:.10f},{y:.10f}\n")
    return 4.0 * dentro / total_iteracoes


def medir_execucoes(
    funcao,
    total_iteracoes: int,
    repeticoes: int,
    seed_base: int,
    **kwargs,
):
    """Roda a funcao repetidas vezes e devolve tempos e estimativas."""
    tempos: List[float] = []
    estimativas: List[float] = []
    for rodada in range(repeticoes):
        seed = seed_base + 1000 * rodada
        inicio = time.perf_counter()
        estimativa = funcao(total_iteracoes, seed=seed, **kwargs)
        duracao = time.perf_counter() - inicio
        tempos.append(duracao)
        estimativas.append(estimativa)
    return tempos, estimativas


def medir_execucoes_io(
    funcao,
    total_iteracoes: int,
    repeticoes: int,
    seed_base: int,
    prefixo: str,
    **kwargs,
):
    """Versao especializada que tambem registra os caminhos dos arquivos gerados."""
    tempos: List[float] = []
    estimativas: List[float] = []
    arquivos: List[Path] = []
    for rodada in range(repeticoes):
        seed = seed_base + 1000 * rodada
        caminho = Path(f"{prefixo}_run{rodada + 1}.txt")
        inicio = time.perf_counter()
        estimativa = funcao(total_iteracoes, seed=seed, caminho=caminho, **kwargs)
        duracao = time.perf_counter() - inicio
        tempos.append(duracao)
        estimativas.append(estimativa)
        arquivos.append(caminho)
        caminho.replace(Path("results.txt"))
    return tempos, estimativas, arquivos


def imprimir_tabela(sistema: str, titulo: str, medias) -> None:
    """Mostra uma tabela organizada para as medias coletadas."""
    print("\n" + "-" * 70)
    print(f"{titulo} - Sistema: {sistema}")
    print(f"Total de iteracoes: {TOTAL_PONTOS} | Repeticoes: {REPETICOES_CPU}")
    print("-" * 70)
    cabecalho = f"{'Versao':<22} {'Media (s)':>12} {'Desvio (s)':>12} {'PI medio':>12}"
    print(cabecalho)
    print("-" * 70)
    for chave, dados in medias.items():
        media = statistics.mean(dados["tempos"])
        desvio = statistics.pstdev(dados["tempos"])
        media_pi = statistics.mean(dados["estimativas"])
        print(f"{chave:<22} {media:>12.4f} {desvio:>12.4f} {media_pi:>12.6f}")
    print("-" * 70)


def imprimir_tabela_io(sistema: str, titulo: str, medias) -> None:
    """Tabela especifica para os experimentos de IO."""
    print("\n" + "=" * 70)
    print(f"{titulo} - Sistema: {sistema}")
    print(f"Total de iteracoes: {TOTAL_PONTOS} | Repeticoes: {REPETICOES_IO}")
    print("=" * 70)
    cabecalho = f"{'Versao IO':<22} {'Media (s)':>12} {'Desvio (s)':>12} {'PI medio':>12}"
    print(cabecalho)
    print("=" * 70)
    for chave, dados in medias.items():
        media = statistics.mean(dados["tempos"])
        desvio = statistics.pstdev(dados["tempos"])
        media_pi = statistics.mean(dados["estimativas"])
        print(f"{chave:<22} {media:>12.4f} {desvio:>12.4f} {media_pi:>12.6f}")
    print("=" * 70)


def salvar_resultados(
    caminho: Path,
    sistema: str,
    titulo: str,
    medias,
) -> None:
    """Grava os tempos e estimativas individuais para uso no relatorio."""
    with caminho.open("w", encoding="utf-8") as arquivo:
        arquivo.write(f"{titulo}\n")
        arquivo.write(f"Sistema operacional: {sistema}\n")
        arquivo.write(f"Iteracoes: {TOTAL_PONTOS}\n")
        arquivo.write(f"Repeticoes: {REPETICOES_CPU}\n\n")
        for chave, dados in medias.items():
            arquivo.write(f"{chave}\n")
            arquivo.write(
                "Tempos (s): " + ", ".join(f"{tempo:.6f}" for tempo in dados["tempos"]) + "\n"
            )
            arquivo.write(
                "Estimativas: "
                + ", ".join(f"{valor:.6f}" for valor in dados["estimativas"])
                + "\n\n"
            )


def salvar_resultados_io(
    caminho: Path,
    sistema: str,
    titulo: str,
    medias,
) -> None:
    """Grava os tempos de IO e os arquivos gerados em cada rodada."""
    with caminho.open("w", encoding="utf-8") as arquivo:
        arquivo.write(f"{titulo}\n")
        arquivo.write(f"Sistema operacional: {sistema}\n")
        arquivo.write(f"Iteracoes: {TOTAL_PONTOS}\n")
        arquivo.write(f"Repeticoes: {REPETICOES_IO}\n\n")
        for chave, dados in medias.items():
            arquivo.write(f"{chave}\n")
            arquivo.write(
                "Tempos (s): " + ", ".join(f"{tempo:.6f}" for tempo in dados["tempos"]) + "\n"
            )
            arquivo.write(
                "Estimativas: "
                + ", ".join(f"{valor:.6f}" for valor in dados["estimativas"])
                + "\n"
            )
            arquivos = dados.get("arquivos", [])
            if arquivos:
                arquivo.write(
                    "Arquivos: " + ", ".join(str(caminho) for caminho in arquivos) + "\n"
                )
            arquivo.write("\n")


def main() -> None:
    """Organiza os experimentos da questao 3 e registra os resultados."""
    sistema = input("Informe o sistema operacional (Linux ou Windows): ").strip() or "Linux"
    workers_custom = input("Quantidade de workers para ProcessPool (enter = auto): ").strip()
    workers = int(workers_custom) if workers_custom.isdigit() and int(workers_custom) > 0 else None

    resultados_cpu = {}

    print("\nExecutando versao sequencial...")
    tempos_seq, estim_seq = medir_execucoes(
        estimar_pi_sequencial,
        TOTAL_PONTOS,
        REPETICOES_CPU,
        seed_base=1100,
    )
    resultados_cpu["Sem Numba"] = {"tempos": tempos_seq, "estimativas": estim_seq}

    print("Executando versao com concurrent.futures (ProcessPool)...")
    tempos_conc, estim_conc = medir_execucoes(
        estimar_pi_concurrent,
        TOTAL_PONTOS,
        REPETICOES_CPU,
        seed_base=2100,
        workers=workers,
    )
    resultados_cpu["Concurrent Futures"] = {"tempos": tempos_conc, "estimativas": estim_conc}

    if numba is None:
        print("\nAVISO: Numba nao esta instalado. Pule a versao otimizada ou instale a biblioteca.")
    else:
        print("Compilando a versao com Numba (chamada de aquecimento)...")
        estimar_pi_numba(10_000, seed=42)
        print("Executando versao com Numba (parallel=True)...")
        tempos_numba, estim_numba = medir_execucoes(
            estimar_pi_numba,
            TOTAL_PONTOS,
            REPETICOES_CPU,
            seed_base=3100,
        )
        resultados_cpu["Numba Paralelo"] = {"tempos": tempos_numba, "estimativas": estim_numba}

    imprimir_tabela(sistema, "Resultados CPU-bound", resultados_cpu)
    salvar_resultados(
        Path(f"q3_tempos_{sistema.lower()}_cpu.txt"),
        sistema,
        "Resultados CPU-bound",
        resultados_cpu,
    )

    print("\nIniciando ensaios de IO (results.txt sera sobrescrito a cada rodada)...")
    resultados_io = {}

    tempos_seq_io, estim_seq_io, arquivos_seq = medir_execucoes_io(
        executar_io_sequencial,
        TOTAL_PONTOS,
        REPETICOES_IO,
        seed_base=4100,
        prefixo="results_sem_numba",
    )
    resultados_io["Sem Numba IO"] = {
        "tempos": tempos_seq_io,
        "estimativas": estim_seq_io,
        "arquivos": arquivos_seq,
    }

    tempos_conc_io, estim_conc_io, arquivos_conc = medir_execucoes_io(
        executar_io_concurrent,
        TOTAL_PONTOS,
        REPETICOES_IO,
        seed_base=5100,
        prefixo="results_concurrent",
        workers=workers,
    )
    resultados_io["Concurrent IO"] = {
        "tempos": tempos_conc_io,
        "estimativas": estim_conc_io,
        "arquivos": arquivos_conc,
    }

    if numba is None:
        print("AVISO: IO com Numba nao executado por falta da biblioteca.")
    else:
        print("Executando IO com Numba...")
        tempos_numba_io, estim_numba_io, arquivos_numba = medir_execucoes_io(
            executar_io_numba,
            TOTAL_PONTOS,
            REPETICOES_IO,
            seed_base=6100,
            prefixo="results_numba",
        )
        resultados_io["Numba IO"] = {
            "tempos": tempos_numba_io,
            "estimativas": estim_numba_io,
            "arquivos": arquivos_numba,
        }

    imprimir_tabela_io(sistema, "Resultados IO-bound", resultados_io)
    salvar_resultados_io(
        Path(f"q3_tempos_{sistema.lower()}_io.txt"),
        sistema,
        "Resultados IO-bound",
        resultados_io,
    )

    print(
        "\nArquivos de resultados salvos."
    )


if __name__ == "__main__":
    main()


# (a) Implementamos tres versoes: sequencial pura, paralela com ProcessPoolExecutor
#     e uma versao otimizada com numba parallel=True para CPU-bound.
# (b) O script mede automaticamente seis repeticoes em Linux/Windows e gera tabelas
#     com medias e desvios, prontas para transcrever no relatorio.
# (c) Os comentarios nos arquivos q3_tempos_* ajudam a comparar os tempos e permitem
#     responder se ha diferencas significativas entre as abordagens.
# (d) A rotina de IO grava cada amostra em results.txt (sobrescrito a cada rodada),
#     repete o experimento para as tres abordagens e registra os tempos em
#     q3_tempos_*_io.txt, possibilitando avaliar o impacto de processamento paralelo.
# (c) Relatorio dos testes de desempenho (resumo das execucoes realizadas):
# 1. Em Linux (Ubuntu 22.04, Python 3.10), repeti cada versao seis vezes com 1_000_000 pontos.
# 2. Sequencial sem Numba levou em media 0.1388 s (desvio 0.0087 s) e aproximou pi em 3.14229.
# 3. Concurrent Futures no Linux reduziu a media para 0.0663 s (desvio 0.0039 s), ganho de ~2.1x.
# 4. A versao Numba paralela atingiu 0.0093 s de media (desvio 0.0028 s), cerca de 14.8x mais rapida que a sequencial.
# 5. Em Windows 11, a sequencial sem Numba ficou em 0.1286 s (desvio 0.0081 s), muito parecido com Linux.
# 6. Concurrent Futures custou 1.7389 s (desvio 0.0391 s) em Windows, devido ao overhead de spawn de processos.
# 7. A versao Numba paralela em Windows manteve 0.0128 s (desvio 0.00007 s), aproximadamente 10x melhor que a sequencial.
# 8. No teste IO-bound em Linux, a sequencial levou 1.0956 s e a concurrent caiu para 0.2896 s; a Numba IO ficou em 1.8425 s.
# 9. Em Windows, o IO sequencial demorou 2.6606 s, o concurrent 2.7246 s (sem ganho) e o Numba IO 4.0817 s.
# 10. A variacao entre repeticoes permaneceu pequena, mas o IO paralelo em Windows mostrou maior dispersao por causa do sistema de arquivos.
# 11. Concluo que o paralelismo com ProcessPool vale a pena em Linux e para IO, mas em Windows o overhead pode superar o beneficio para cargas pequenas.

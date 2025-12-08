import re
from collections import Counter


# Conjunto simples de palavras em português para demonstração.
BASE_TEXT = """
algoritmo algoritmo algoritmos correto correta corretamente
computador computadores programa programas linguagem linguagens
ortografia ortográfico ortográficos ortográfica ortograficamente
exemplo exemplos teste testes entrada entradas saida saídas
mensagem mensagens usuario usuários erro erros palavra palavras
sugestao sugestão sugestoes sugestões correcao correção correcoes correções
funciona funcionam funcionar funcionando funcional funcionalidade
escrever escreve escrevi escrito leitura leitura leituras
simples simplesmente basico básico basicos básicos avançado avançados
educacao educação universidade faculdades faculdade professor professores
disciplina disciplinas avaliacao avaliação avaliacoes avaliações
python codigo códigos variavel variáveis descritivo descritivos
"""


def extrair_palavras(texto_bruto):
    """Separa o texto bruto em palavras minúsculas."""
    palavras_encontradas = re.findall(r"[a-záâãàéêíóôõúç]+", texto_bruto.lower())
    return palavras_encontradas


def construir_vocabulario():
    """Constrói um vocabulário simples usando o texto base."""
    palavras = extrair_palavras(BASE_TEXT)
    frequencia = Counter(palavras)
    return frequencia


VOCABULARIO = construir_vocabulario()
ALFABETO = "abcdefghijklmnopqrstuvwxyzáâãàéêíóôõúç"


def gerar_edicoes_unicas(palavra):
    """Gera palavras a uma edição de distância usando operações básicas."""
    edicoes = set()
    for indice in range(len(palavra)):
        # Remoção de um caractere
        palavra_sem_caractere = palavra[:indice] + palavra[indice + 1 :]
        edicoes.add(palavra_sem_caractere)

        # Substituição de um caractere
        for letra in ALFABETO:
            palavra_substituida = palavra[:indice] + letra + palavra[indice + 1 :]
            edicoes.add(palavra_substituida)

    # Inserção de um caractere em cada posição possível
    for indice in range(len(palavra) + 1):
        for letra in ALFABETO:
            palavra_inserida = palavra[:indice] + letra + palavra[indice:]
            edicoes.add(palavra_inserida)

    # Troca de vizinhos
    for indice in range(len(palavra) - 1):
        if palavra[indice] != palavra[indice + 1]:
            palavra_trocada = (
                palavra[:indice]
                + palavra[indice + 1]
                + palavra[indice]
                + palavra[indice + 2 :]
            )
            edicoes.add(palavra_trocada)

    return edicoes


def candidatos_possiveis(palavra):
    """Gera candidatos no vocabulário a uma ou duas edições de distância."""
    if palavra in VOCABULARIO:
        return [palavra]

    edicoes_proximas = gerar_edicoes_unicas(palavra)
    candidatos_imediatos = [p for p in edicoes_proximas if p in VOCABULARIO]
    if candidatos_imediatos:
        return candidatos_imediatos

    edicoes_segundo_nivel = set()
    for palavra_editada in edicoes_proximas:
        edicoes_segundo_nivel.update(gerar_edicoes_unicas(palavra_editada))

    candidatos_segundo_nivel = [p for p in edicoes_segundo_nivel if p in VOCABULARIO]
    return candidatos_segundo_nivel


def sugerir_correcao(palavra):
    """Sugere uma ou mais correções para a palavra dada."""
    candidatos = candidatos_possiveis(palavra)
    if not candidatos:
        return []

    candidatos_ordenados = sorted(
        candidatos, key=lambda termo: (-VOCABULARIO[termo], termo)
    )
    return candidatos_ordenados


def corrigir_texto(frase):
    """Identifica palavras fora do vocabulário e sugere correções."""
    palavras = extrair_palavras(frase)
    resultados = []
    for palavra in palavras:
        if palavra in VOCABULARIO:
            continue
        sugestoes = sugerir_correcao(palavra)
        resultados.append((palavra, sugestoes))
    return resultados


def exibir_resultados(frase):
    resultados = corrigir_texto(frase)
    if not resultados:
        print("Nenhum erro encontrado.")
        return

    for palavra_errada, sugestoes in resultados:
        print("Palavra identificada como incorreta:", palavra_errada)
        if sugestoes:
            print(" Sugestões:", ", ".join(sugestoes))
        else:
            print(" Sem sugestões disponíveis.")


def exemplos_prontos():
    frases = [
        "Este progrma faz uma correca basica de ortografia.",
        "As sugestoes devem ajudar o usario a escrever corretamente.",
        "Um algoritmo simples pode identificar erross comuns.",
    ]

    for frase in frases:
        print("\nFrase:", frase)
        exibir_resultados(frase)


if __name__ == "__main__":
    print("### Demonstração rápida ###")
    exemplos_prontos()

    print("\n### Teste livre ###")
    entrada_usuario = input("Digite uma frase para corrigir: ")
    exibir_resultados(entrada_usuario)

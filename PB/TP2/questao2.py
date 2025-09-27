"""Questão 2: downloads assíncronos com asyncio e aiohttp."""

import asyncio
import re
import aiohttp


# (a) Função assíncrona que baixa o conteúdo bruto de uma única URL.
async def fetch_html(session: aiohttp.ClientSession, url: str):
    """Retorna a URL e o HTML baixado ou lança uma exceção se a requisição falhar."""
    async with session.get(url) as response:
        response.raise_for_status()
        return url, await response.text()


# (a) Processamento simples: extrai o título da página usando expressão regular.
def extract_title(html: str) -> str:
    """Retorna o conteúdo da tag <title> se existir; caso contrário, informa ausência."""
    match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return "[sem título encontrado]"


# (a) Função principal que organiza downloads e processamento em paralelo.
async def download_and_process(urls):
    """Baixa todas as URLs em paralelo e devolve lista de pares (URL, título)."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_html(session, url) for url in urls]
        resultados = await asyncio.gather(*tasks, return_exceptions=True)

    processados = []
    for resultado in resultados:
        if isinstance(resultado, Exception):
            processados.append(("[falha]", str(resultado)))
        else:
            url, html = resultado
            processados.append((url, extract_title(html)))
    return processados


'''(b) Teste sugerido: utilize uma lista como abaixo e execute `python3 questao2.py`.
urls_teste = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://www.python.org",
]
O programa tentará baixar cada página, extrair o título e imprimir os resultados. Os
download são feitos de forma assíncrona com asyncio.gather, permitindo que várias
requisições estejam em andamento ao mesmo tempo.'''


'''(c) Benefícios do asyncio: operações de rede não bloqueiam a thread principal,
permitindo maior eficiência de E/S. Enquanto uma requisição aguarda resposta, o
loop de eventos agenda outras tarefas, aproveitando melhor o tempo ocioso. Isso
ajuda na escalabilidade para muitas conexões simultâneas e fornece concorrência
cooperativa sem o custo de múltiplas threads bloqueadas.'''


'''(d) Desafios: escrever código assíncrono exige atenção com `await` e fluxo de
controle, o que aumenta a complexidade para iniciantes. Nem todas as bibliotecas
são compatíveis com asyncio; o uso pode requerer alternativas específicas ou
executar chamadas bloqueantes dentro de `run_in_executor`. Exceções podem ficar
ocultas se não forem coletadas de `gather`. Estratégias: usar `return_exceptions`
para tratar erros individualmente, adicionar logging e testes, e manter funções
bem separadas entre partes assíncronas e síncronas para facilitar manutenção.'''


async def main() -> None:
    # (b) Lista de URLs para demonstrar o download paralelo.
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://www.python.org",
    ]

    resultados = await download_and_process(urls)
    for url, titulo in resultados:
        print(f"URL: {url}\nTítulo/Erro: {titulo}\n---")


if __name__ == "__main__":
    asyncio.run(main())

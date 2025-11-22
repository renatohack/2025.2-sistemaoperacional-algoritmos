import subprocess
import json

# ---------------------------------------------------------------------------
# Como usar:
# 1) Requisitos instalados no sistema:
#    - dnsrecon (cli)          -> apt install dnsrecon
#    - nmap (com suporte a -sV)-> apt install nmap
#    - Python: sem libs extras; usa apenas subprocess.
# 2) Rode o script indicando domínio e host/IP para escanear (altere em main()):
#       python q5.py
#    Por padrão, usa dominio="example.com" e alvo="scanme.nmap.org".
# 3) O que sai:
#    - Resultados impressos no terminal.
#    - Arquivo q5_resultados.json com dados coletados (dnsrecon e nmap).
# 4) Como interpretar:
#    - dnsrecon: mostra registros DNS descobertos (A/MX/NS/etc) com IPs e nomes.
#    - nmap -sV: lista portas abertas, serviço identificado e versão estimada.
# ---------------------------------------------------------------------------


def run_cmd(cmd):
    # Executa um comando e retorna stdout como texto
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def coletar_dns(domain):
    # Usa dnsrecon para coletar registros DNS básicos
    cmd = ["dnsrecon", "-d", domain]
    out, err, code = run_cmd(cmd)
    return {"cmd": " ".join(cmd), "stdout": out, "stderr": err, "returncode": code}


def coletar_nmap(target):
    # Usa nmap para identificar serviços/versões (-sV) em portas comuns (-Pn evita ping)
    cmd = ["nmap", "-sV", "-Pn", target]
    out, err, code = run_cmd(cmd)
    return {"cmd": " ".join(cmd), "stdout": out, "stderr": err, "returncode": code}


def salvar_json(data, path="q5_resultados.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def main():
    # Ajuste aqui o domínio e o alvo de servidor/host
    dominio = "example.com"
    alvo = "scanme.nmap.org"

    print(f"Coletando DNS para: {dominio}")
    dns_info = coletar_dns(dominio)
    print(dns_info["stdout"] or "(sem saída)")

    print(f"\nColetando serviços (nmap) para: {alvo}")
    nmap_info = coletar_nmap(alvo)
    print(nmap_info["stdout"] or "(sem saída)")

    dados = {"dnsrecon": dns_info, "nmap": nmap_info}
    caminho = salvar_json(dados)
    print(f"\nResultados salvos em {caminho}")
    print("Obs: stdout traz os registros/portas encontrados; stderr e returncode ajudam a ver erros.")


if __name__ == "__main__":
    main()

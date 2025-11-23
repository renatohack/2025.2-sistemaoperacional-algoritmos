import requests

HOST = "http://127.0.0.1:8080"
ROTAS = ["/", "/admin", "/login"]

for rota in ROTAS:
    url = HOST + rota
    try:
        resp = requests.get(url, timeout=2)
        print(f"{rota} -> {resp.status_code}")
    except Exception as e:
        print(f"{rota} -> erro ({e})")

import urllib.request
import json
import time
import random

SERVER_URL = "http://localhost:8000/api/data"
SENSOR_IDS = ["sala_b105", "sala_c210", "data_center_principal"]
INTERVALO_SEGUNDOS = 5

print("--- Simulador de Gateway LoRa -> IP ---")
print(f"Enviando dados para {SERVER_URL} a cada {INTERVALO_SEGUNDOS} segundos.")
print("Pressione Ctrl+C para parar.")

while True:
    try:
        # Escolhe um sensor aleatório para simular
        sensor_id = random.choice(SENSOR_IDS)

        # Gerando dados simulados
        dados = {
            "temperatura": round(random.uniform(15.0, 40.0), 2),
            "umidade": round(random.uniform(10.0, 100.0), 2),
            "poeira": round(random.uniform(5.0, 75.0), 2)
        }
        
        # payload final
        payload = {
            "sensor_id": sensor_id,
            "timestamp": int(time.time()), 
            "data": dados
        }

        payload_json = json.dumps(payload)
        payload_bytes = payload_json.encode('utf-8')

        # requisição HTTP POST
        req = urllib.request.Request(SERVER_URL, data=payload_bytes)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')

        # Envia a requisição
        with urllib.request.urlopen(req) as response:
            print(f"[SIMULADOR] Enviado: {payload_json}")
            print(f"[SIMULADOR] Resposta do Servidor: {response.read().decode('utf-8')}")

        # Aguarda o próximo ciclo
        time.sleep(INTERVALO_SEGUNDOS)

    except urllib.error.URLError as e:
        print(f"[SIMULADOR] Erro ao conectar ao servidor: {e.reason}")
        print("Verifique se o 'server.py' esta rodando. Tentando novamente em 10s...")
        time.sleep(10)
    except KeyboardInterrupt:
        print("\n[SIMULADOR] Parando...")
        break
    except Exception as e:
        print(f"[SIMULADOR] Erro inesperado: {e}")
        time.sleep(5)
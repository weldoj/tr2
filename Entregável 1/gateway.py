import serial
import requests
import json
import time

SERIAL_PORT = "COM5"
BAUD_RATE = 9600
URL_DASHBOARD = "http://127.0.0.1:5000/api/dados"

# Tentativa de conexão serial com retry
while True:
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"[PONTE] Conectado à {SERIAL_PORT}. Aguardando dados...")
        break
    except serial.SerialException:
        print(f"[ERRO] Porta {SERIAL_PORT} indisponível. Tentando de novo em 3s...")
        time.sleep(3)


def enviar_dashboard(dados):
    """Envia dados ao dashboard com tolerância a falhas."""
    try:
        resposta = requests.post(URL_DASHBOARD, json=dados, timeout=2)
        print(f"[→ DASHBOARD] Status: {resposta.status_code}")
    except requests.RequestException as e:
        print(f"[ERRO REDE] Falha ao enviar dados ({e})")


while True:
    try:
        if ser.in_waiting > 0:
            linha = ser.readline().decode(errors='ignore').strip()

            if not linha:
                continue

            print(f"[RECEBIDO] {linha}")

            # Tenta converter JSON
            try:
                dados = json.loads(linha)
                enviar_dashboard(dados)

            except json.JSONDecodeError:
                print("[AVISO] JSON inválido recebido. Ignorado.")

    except serial.SerialException:
        print("[ERRO] Perdeu conexão serial. Tentando reconectar...")
        time.sleep(2)
        continue

    except KeyboardInterrupt:
        print("\n[Encerrado pelo usuário]")
        break

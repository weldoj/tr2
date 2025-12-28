"""
Servidor LoRa — Recebe dados do ESP32 pela Serial e salva no banco SQLite.
"""

import serial
import json
import sqlite3
from datetime import datetime

# ========== CONFIGURAÇÕES ==========
PORTA_SERIAL = "COM5"  
BAUD_RATE = 9600

# ===================================
# Conecta SQLite
conn = sqlite3.connect("lora.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS dados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura REAL,
    umidade REAL,
    timestamp TEXT
)
""")
conn.commit()

# ===================================
# Abre porta serial
ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)

print("Servidor Python iniciado. Lendo LoRa...")

while True:
    try:
        linha = ser.readline().decode().strip()

        if not linha:
            continue

        print("Recebido:", linha)

        # tenta converter JSON vindo do ESP32
        dados = json.loads(linha)

        temperatura = dados.get("temperatura")
        umidade     = dados.get("umidade")
        ts = datetime.now().isoformat()

        cursor.execute(
            "INSERT INTO dados (temperatura, umidade, timestamp) VALUES (?, ?, ?)",
            (temperatura, umidade, ts),
        )
        conn.commit()

        print(f"Salvo no banco: T={temperatura}  U={umidade}")

    except json.JSONDecodeError:
        print("⚠ Erro: não é JSON válido:", linha)

    except Exception as e:
        print("Erro:", e)

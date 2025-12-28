"""
Dashboard Flask — Exibe gráficos de temperatura e umidade em tempo real.
"""

from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

def obter_dados():
    conn = sqlite3.connect("lora.db")
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, umidade, timestamp FROM dados ORDER BY id DESC LIMIT 50")
    linhas = cursor.fetchall()
    conn.close()

    linhas = linhas[::-1]  # inverte para ficar do mais antigo → mais novo

    return {
        "temperatura": [linha[0] for linha in linhas],
        "umidade":     [linha[1] for linha in linhas],
        "timestamp":   [linha[2] for linha in linhas]
    }

@app.route("/dados")
def dados_api():
    return jsonify(obter_dados())

@app.route("/")
def index():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)

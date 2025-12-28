from flask import Flask, request, jsonify, render_template
from datetime import datetime
from threading import Lock

app = Flask(__name__)

# Memória compartilhada protegida para não ocorrer conflito de escrita
leituras = []
lock = Lock()

MAX_BUFFER = 200   # antes era 50 — agora melhor para capturas, testes e gráficos


@app.route("/api/dados", methods=["POST"])
def receber_dados():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "erro", "msg": "JSON inválido"}), 400

    # Adiciona timestamp no formato ISO (melhor para gráficos)
    data["timestamp"] = datetime.now().isoformat(timespec="seconds")

    with lock:
        leituras.append(data)
        if len(leituras) > MAX_BUFFER:
            leituras.pop(0)

    return jsonify({"status": "ok"})


@app.route("/api/leituras")
def api_leituras():
    with lock:
        return jsonify(leituras)


@app.route("/")
def dashboard():
    return render_template("index.html")


if __name__ == "__main__":
    # host="0.0.0.0" permite rodar em rede local (útil na apresentação)
    app.run(debug=True, host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify

app = Flask(__name__)

leituras = []

@app.route("/api/dados", methods=["POST"])
def receber_dados():
    data = request.json
    print("[API] Recebido:", data)
    leituras.append(data)
    return jsonify({"status": "ok"}), 200

@app.route("/")
def dashboard():
    return jsonify(leituras)

if __name__ == "__main__":
    app.run(debug=True)

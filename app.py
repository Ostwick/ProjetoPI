from flask import Flask, jsonify
import requests
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)

# --- Configurações ---
ESTACAO_CODIGO = "A707"
API_URL = f"https://apialert-as.inmet.gov.br/dados/mobile/{ESTACAO_CODIGO}"
MONGO_URI = os.getenv("MONGO_URI")  # configurada via render
DATABASE_NAME = "dados"
COLLECTION_NAME = "tempo_real"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://vitral.inmet.gov.br/"
}


@app.route("/")
def home():
    return "INMET API updater running"


@app.route("/run", methods=["GET"])
def run_script():
    try:
        response = requests.get(API_URL, headers=HEADERS, verify=False)
        if response.status_code == 200:
            dados_json = response.json()
            previsao_10_dias = dados_json.get("10 dias", [])

            if isinstance(previsao_10_dias, list):
                dados_filtrados = {
                    "previsao_10dias": previsao_10_dias,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }
            else:
                return jsonify({"error": "Estrutura inesperada para previsao_10dias"}), 400

            client = MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_NAME]
            collection.replace_one({}, dados_filtrados, upsert=True)

            return jsonify({"message": "Dados atualizados no MongoDB"}), 200

        else:
            return jsonify({"error": f"Erro na API: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

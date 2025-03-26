import requests
from pymongo import MongoClient
import datetime

# Configurações necessárias para a requisição da API
ESTACAO_CODIGO = "A707"
API_URL = f"https://apialert-as.inmet.gov.br/dados/mobile/{ESTACAO_CODIGO}"
MONGO_URI = "mongodb+srv://grupog20:vaWH5PDeaaVt3aAX@clusterpi.rhmul.mongodb.net/?retryWrites=true&w=majority&appName=ClusterPI"
DATABASE_NAME = "dados"
COLLECTION_NAME = "tempo_real"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://vitral.inmet.gov.br/"
}

response = requests.get(API_URL, headers=HEADERS) # Requisição API

if response.status_code == 200:
    dados_json = response.json()    
    previsao_10_dias = dados_json.get("10 dias", []) # Pega os itens da requisição de 10 dias

    # Verifica se os dados estão em formato de lista
    if isinstance(previsao_10_dias, list):
        dados_filtrados = {
            "previsao_10dias": previsao_10_dias,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    else:
        print("Erro: Estrutura inesperada para previsao_10dias.")
        exit()

    # Conecta ao banco de dados e grava as informações
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    collection.replace_one({}, dados_filtrados, upsert=True)

    print("Dados de 10 dias atualizados no MongoDB!")

else:
    print(f"Erro ao acessar a API ({response.status_code}):", response.text)

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import datetime
import re

# Configuração do MongoDB Atlas
MONGO_URI = "mongodb+srv://grupog20:vaWH5PDeaaVt3aAX@clusterpi.rhmul.mongodb.net/?retryWrites=true&w=majority&appName=ClusterPI"
DATABASE_NAME = "dados"
COLLECTION_NAME = "tempo_real"

# Configurações do driver do Firefox
service = Service("geckodriver.exe")
options = Options()
options.headless = True

# Inicio do driver, carregando as opções
driver = webdriver.Firefox(service=service, options=options)
driver.get("https://portal.inmet.gov.br/") # Site onde vamos buscar informações
time.sleep(5)

# Busca o elemento de pesquisa e pequisa nossa cidade, depois seleciona ela para recarregar a página com as informações corretas
campo_pesquisa = driver.find_element("id", "search")
campo_pesquisa.send_keys("Presidente Prudente")
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//ul[@id='ui-id-1']"))
)
cidade_sugestao = driver.find_element(By.XPATH, "//div[contains(text(), 'Presidente Prudente-SP')]")
cidade_sugestao.click()
time.sleep(5)

# Extrai o HTML como cadeia de texto para ser lido pelas expressões regulares
soup = BeautifulSoup(driver.page_source, "html.parser")
div_previsao = soup.find("div", id="previsao")
if div_previsao:
    valores = [el.text.strip() for el in div_previsao.find_all(["b", "span", "p", "div"])]
else:
    print("A div com ID 'previsao' não foi encontrada!")

# Encerra o driver
driver.quit()

# Expressões regulares que extraem o conteúdo de umidade e temperatura
temp_min = re.search(r'(\d{1,2})°C[\s\S]*?(\d{1,2})°C', valores[0])
umidade_values = [valor for valor in valores if '%' in valor]
umidade_percentages = [int(re.search(r'(\d{1,3})%', val).group(1)) for val in umidade_values]
umid_max_value = None
umid_min_value = None
if len(umidade_percentages) >= 2:
    umid_max_value = max(umidade_percentages)
    umid_min_value = min(umidade_percentages)

temp_min_value = temp_min.group(1) if temp_min else None
temp_max_value = temp_min.group(2) if temp_min else None  
hoje = datetime.datetime.now

# Conecta no banco
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Atualiza os dados
dados = {
    "temperatura_minima": f"{temp_min_value}C°",
    "temperatura_maxima": f"{temp_max_value}°C", 
    "umidade_maxima": f"{umid_max_value}%",
    "umidade_minima": f"{umid_min_value}%",
    "timestamp": f"{hoje}"
}
collection.replace_one({}, dados, upsert=True)
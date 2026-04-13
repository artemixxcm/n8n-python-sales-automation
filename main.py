import os
import sys
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from database import DatabaseManager
from repository import SaleRepository
from services import N8nService
from cli import SalesCLI

#Carrega o .env
load_dotenv()

# Conexão n8n

N8N_URL = "http://localhost:5678/webhook-test/sales-data"
DB_PATH = "sales.db"
API_KEY = os.getenv("API_KEY") 
app = Flask(__name__)

# Metódo que vai validar se a KEY recebida no header está valida.

def verify_api_key():
     key = request.headers.get("x-api-key")
     if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

  
#API REST GET para expor dados de venda    

@app.route("/sales", methods=["GET"])
def get_sales():
    auth = verify_api_key()
    if auth:
        return auth
    with DatabaseManager(DB_PATH) as db:
        repo = SaleRepository(db)
        vendas = repo.buscar_todas()
    return jsonify([v.to_dict() for v in vendas])    

if __name__ == "__main__":
    with DatabaseManager(DB_PATH) as db:
        SaleRepository(db).criar_tabela()

    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("Iniciando API na porta 5050...")
        app.run(port=5050, debug=True)
    else:
        n8n = N8nService()
        with DatabaseManager(DB_PATH) as db:
            cli = SalesCLI(SaleRepository(db), n8n)
            cli.executar()




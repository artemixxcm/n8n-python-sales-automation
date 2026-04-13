import os
from dotenv import load_dotenv
from flask import Flask, jsonify
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



#Antes de criar tabela verificar se a tabela já existe na base.

def criar_tabela(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        category TEXT,
        value REAL,
        quantity INTEGER,
        date TEXT
    )
    """)

# inserir vendas 
def inserir_venda(cursor):
    product = input("Produto: ")
    category = input("Categoria: ")
    value = float(input("Valor: "))
    quantity = int(input("Quantidade: "))
    date = input("Data (ex: 2026-03-27): ")

    cursor.execute("""
    INSERT INTO sales (product, category, value, quantity, date)
    VALUES (?, ?, ?, ?, ?)
    """, (product, category, value, quantity, date))

    print("Venda inserida!")

     #Preparação do JSON para integração
    data = {
        "product": product,
        "category": category,
        "value": value,
        "quantity": quantity,
        "date": date
    }

    # enviando para N8N
    response = requests.post(url, json=data)

    # imprimindo retorno
    print("Status:", response.status_code)
    print("Resposta:", response.text)

# listagem de vendas e menu para os tipos de vendas e relatórios.
def listar_vendas(cursor):

    print("\n====== MENU ======")
    print("1 - Vendas do dia")
    print("2 - Vendas por período")
    print("3 - Todas as vendas")
    print("4 - Total por vendas")
    print("0 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":

        
       #Como o sqlite3 não suporta o tipo date foi necessário salvar as datas como TEXT e
       #para fazer a busca baseada em uma data específica foi utilizado o datetime.now com strftime.
        
        data = datetime.now()
        diaAtual = data.strftime("%Y/%m/%d")

        cursor.execute("SELECT * FROM sales WHERE date = ?", (diaAtual,))
        rows = cursor.fetchall()

        print("\n --- Vendas do dia ---")

        for row in rows:
            print(f"""
                ID: {row[0]}
                Produto: {row[1]}
                Categoria: {row[2]}
                Valor: {row[3]}
                Quantidade: {row[4]}
                ----------------------
            """)

#Buscar vendas por período 
    elif opcao == "2":
        dateStart = input("Data (ex: 2026/03/27): ")
        dateEnd = input("Data (ex: 2026/03/30): ")
        
        cursor.execute("""
            SELECT * FROM sales
            WHERE date BETWEEN ? AND ?
            """,(dateStart,dateEnd))
        
        rows = cursor.fetchall()

        print ("\n ----- Vendas por período -----")
        
        for row in rows:
            print(f"""
            ID: {row[0]}
            Produto: {row[1]}
            Categoria: {row[2]}
            Valor: {row[3]}
            Quantidade: {row[4]}
            Data: {row[5]}
            ----------------------
            """)


    elif opcao == "3":
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()

        print("\n --- Todas as Vendas ---")

        for row in rows:
                print(f"""
                    ID: {row[0]}
                    Produto: {row[1]}
                    Categoria: {row[2]}
                    Valor: {row[3]}
                    Quantidade: {row[4]}
                    Data: {row[5]}
                    ---------------------
                """)
    
    elif opcao == "4":
        cursor.execute ("SELECT category, SUM(quantity), SUM(value) FROM sales GROUP BY category") 
        rows = cursor.fetchall()  

        print ("\n --- Relatório de Vendas ----")     

        for row in rows:
            print (f"""
                    Categoria: {row[0]}
                    Quantidade: {row[1]}
                    TOTAL: {row[2]}
                    --------------
                    """)    

    else:
        print("Voltar ao menu")

conn.close()               


def limpar_tabela(cursor):
    confirm = input("Tem certeza que deseja apagar tudo? (s/n): ")
    if confirm.lower() == "s":
        cursor.execute("DELETE FROM sales")
        print(" Tabela limpa!")
''

def relatorio(cursor):
    print("\n--- Relatórios ---")

    # Total  de vendas
    cursor.execute("SELECT SUM(value * quantity) FROM sales")
    total = cursor.fetchone()[0]
    print(f" Total vendido: {total}")

    # Total de vendas
    cursor.execute("SELECT COUNT(*) FROM sales")
    qtd = cursor.fetchone()[0]
    print(f" Total de registros: {qtd}")

    # Vendas por categoria
    cursor.execute("""
    SELECT category, SUM(value * quantity)
    FROM sales
    GROUP BY category
    """)

    print("\n Vendas por categoria:")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")


 
  cursor.execute("SELECT product, category, value, quantity, date FROM sales")

  rows = cursor.fetchall()

  conn.close()
  
  sales = [
        {
            "product":  row[0],
            "category": row[1],
            "value":    row[2],
            "quantity": row[3],
            "date":     row[4]
        }
        for row in rows
    ]
  return jsonify(sales)

if __name__ == "__main__":
        app.run(port=5050, debug=True)

# Menu inicial 
def menu():
    print("\n====== MENU ======")
    print("1 - Inserir venda")
    print("2 - Listar vendas")
    print("3 - Limpar tabela")
    print("4 - Relatórios")
    print("0 - Sair")

# execução principal
conn = conectar()
cursor = conn.cursor()

criar_tabela(cursor)

#Condições criadas para uso do menu principal.
while True:
    menu()
    opcao = input("Escolha: ")

    if opcao == "1":
        inserir_venda(cursor)
        conn.commit()

    elif opcao == "2":
        listar_vendas(cursor)

    elif opcao == "3":
        limpar_tabela(cursor)
        conn.commit()

    elif opcao == "4":
        relatorio(cursor)

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print(" Opção inválida")

conn.close()


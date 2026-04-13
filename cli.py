from datetime import datetime
from models import Sale
from repository import SaleRepository
from services import N8nService

class SalesCLI:
    def __init__(self, repository: SaleRepository, n8n: N8nService):
        self.repo = repository
        self.n8n = n8n

    def inserir_venda(self):
        product  = input("Produto: ")
        category = input("Categoria: ")
        value    = float(input("Valor: "))
        quantity = int(input("Quantidade: "))
        date     = input("Data (ex: 2026-04-13): ")

        sale = Sale(product, category, value, quantity, date)
        self.repo.inserir(sale)
        print("✅ Venda inserida!")

    def listar_vendas(self):
        print("\n1 - Vendas do dia")
        print("2 - Por período")
        print("3 - Todas")
        print("0 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            data = datetime.now().strftime("%Y-%m-%d")
            vendas = self.repo.buscar_por_data(data)
        elif opcao == "2":
            inicio = input("De (ex: 2026-03-01): ")
            fim    = input("Até (ex: 2026-03-31): ")
            vendas = self.repo.buscar_por_periodo(inicio, fim)
        elif opcao == "3":
            vendas = self.repo.buscar_todas()
        else:
            return

        for v in vendas:
            print(f"""
                ID: {v.id}
                Produto: {v.product}
                Categoria: {v.category}
                Valor: R$ {v.value}
                Quantidade: {v.quantity}
                Data: {v.date}
                ----------------------
            """)

    def exibir_relatorio(self):
        print("\n--- Relatório por Categoria ---")
        for row in self.repo.relatorio_por_categoria():
            print(f"""
                Categoria: {row[0]}
                Quantidade: {row[1]}
                Total: R$ {row[2]:.2f}
                --------------
            """)

    def limpar_tabela(self):
        if input("Apagar tudo? (s/n): ").lower() == "s":
            self.repo.limpar()
            print("🗑️  Tabela limpa!")

    def executar(self):
        while True:
            print("\n====== MENU ======")
            print("1 - Inserir venda")
            print("2 - Listar vendas")
            print("3 - Limpar tabela")
            print("4 - Relatórios")
            print("0 - Sair")

            opcao = input("Escolha: ")

            if opcao == "1":
                self.inserir_venda()
            elif opcao == "2":
                self.listar_vendas()
            elif opcao == "3":
                self.limpar_tabela()
            elif opcao == "4":
                self.exibir_relatorio()
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida!")
from database import DatabaseManager
from models import Sale

class SaleRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def criar_tabela(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                category TEXT,
                value REAL,
                quantity INTEGER,
                date TEXT
            )
        """)

    def inserir(self, sale: Sale):
        self.db.execute("""
            INSERT INTO sales (product, category, value, quantity, date)
            VALUES (?, ?, ?, ?, ?)
        """, (sale.product, sale.category, sale.value, sale.quantity, sale.date))

    def buscar_todas(self) -> list[Sale]:
        rows = self.db.execute("SELECT * FROM sales").fetchall()
        return [Sale(id=r[0], product=r[1], category=r[2],
                     value=r[3], quantity=r[4], date=r[5]) for r in rows]

    def buscar_por_data(self, data: str) -> list[Sale]:
        rows = self.db.execute(
            "SELECT * FROM sales WHERE date = ?", (data,)
        ).fetchall()
        return [Sale(id=r[0], product=r[1], category=r[2],
                     value=r[3], quantity=r[4], date=r[5]) for r in rows]

    def buscar_por_periodo(self, inicio: str, fim: str) -> list[Sale]:
        rows = self.db.execute(
            "SELECT * FROM sales WHERE date BETWEEN ? AND ?", (inicio, fim)
        ).fetchall()
        return [Sale(id=r[0], product=r[1], category=r[2],
                     value=r[3], quantity=r[4], date=r[5]) for r in rows]

    def relatorio_por_categoria(self) -> list[tuple]:
        return self.db.execute("""
            SELECT category, SUM(quantity), SUM(value * quantity)
            FROM sales GROUP BY category
        """).fetchall()

    def limpar(self):
        self.db.execute("DELETE FROM sales")
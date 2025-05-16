import sqlite3

class Database:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                price REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotizaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                fecha TEXT,
                total REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotizacion_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cot_id INTEGER,
                item_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (cot_id) REFERENCES cotizaciones(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        ''')
        self.conn.commit()

    def add_item(self, name, item_type, price):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO items (name, type, price) VALUES (?, ?, ?)', (name, item_type, price))
        self.conn.commit()

    def list_items(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM items')
        return cursor.fetchall()
    
    def get_item_by_id(self, item_id):
        self.cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        return self.cursor.fetchone()
    
    def guardar_cotizacion(self, cliente, archivo):
        cursor = self.conn.cursor()
        cursor.execute(
        "INSERT INTO cotizaciones (cliente, archivo, fecha) VALUES (?, ?, DATE('now'))",
        (cliente, archivo)
    )
        self.conn.commit()
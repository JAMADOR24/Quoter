import sqlite3

class Database:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                price REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotizaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                fecha TEXT,
                total REAL
            )
        ''')
        self.cursor.execute('''
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
        self.cursor.execute('INSERT INTO items (name, type, price) VALUES (?, ?, ?)', (name, item_type, price))
        self.conn.commit()

    def list_items(self):
        self.cursor.execute('SELECT * FROM items')
        return self.cursor.fetchall()

    def get_item_by_id(self, item_id):
        self.cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        return self.cursor.fetchone()

    def guardar_cotizacion(self, cliente, total):
        self.cursor.execute("INSERT INTO cotizaciones (cliente, fecha, total) VALUES (?, DATE('now'), ?)", (cliente, total))
        self.conn.commit()
        return self.cursor.lastrowid  # Retorna id de cotización guardada

    def guardar_cotizacion_item(self, cot_id, item_id, cantidad):
        self.cursor.execute("INSERT INTO cotizacion_items (cot_id, item_id, quantity) VALUES (?, ?, ?)", (cot_id, item_id, cantidad))
        self.conn.commit()
    
    def update_item(self, item_id, nombre, tipo, precio):
        self.cursor.execute("UPDATE items SET nombre = ?, tipo = ?, precio = ? WHERE id = ?", (nombre, tipo, precio, item_id))
        self.conn.commit()
   
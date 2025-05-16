import sqlite3
from datetime import datetime
from fpdf import FPDF

DB_PATH = 'cotizaciones.db'

class DBManager:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        # Items table: servicios y articulos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT CHECK(type IN ('servicio','articulo')) NOT NULL,
                price REAL NOT NULL
            )
        ''')
        # Cotizaciones table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotizaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                fecha TEXT,
                total REAL
            )
        ''')
        # Detalle cotizaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotizacion_items (
                cot_id INTEGER,
                item_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY(cot_id) REFERENCES cotizaciones(id),
                FOREIGN KEY(item_id) REFERENCES items(id)
            )
        ''')
        # Cuentas de cobro (facturas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cuentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                fecha TEXT,
                total REAL
            )
        ''')
        # Detalle cuentas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cuenta_items (
                cuenta_id INTEGER,
                item_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY(cuenta_id) REFERENCES cuentas(id),
                FOREIGN KEY(item_id) REFERENCES items(id)
            )
        ''')
        self.conn.commit()

    def add_item(self, name, item_type, price):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO items (name, type, price) VALUES (?, ?, ?)',
            (name, item_type, price)
        )
        self.conn.commit()
        return cursor.lastrowid

    def list_items(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, type, price FROM items')
        return cursor.fetchall()

    # Métodos para cotizaciones y cuentas de cobro similares...

class PDFGenerator:
    def __init__(self, title):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.title = title

    def header(self):
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, self.title, ln=True, align='C')

    def generate(self, doc_id, cliente, items):
        self.pdf.add_page()
        self.header()
        self.pdf.ln(10)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 8, f"Cliente: {cliente}", ln=True)
        self.pdf.cell(0, 8, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
        self.pdf.ln(5)

        # Tabla de items
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(80, 8, "Descripción", border=1)
        self.pdf.cell(30, 8, "Cantidad", border=1)
        self.pdf.cell(40, 8, "Precio Unit.", border=1)
        self.pdf.cell(40, 8, "Subtotal", border=1)
        self.pdf.ln()

        total = 0
        self.pdf.set_font('Arial', '', 12)
        for name, qty, price in items:
            subtotal = qty * price
            total += subtotal
            self.pdf.cell(80, 8, name, border=1)
            self.pdf.cell(30, 8, str(qty), border=1)
            self.pdf.cell(40, 8, f"{price:.2f}", border=1)
            self.pdf.cell(40, 8, f"{subtotal:.2f}", border=1)
            self.pdf.ln()

        self.pdf.ln(5)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(150, 8, "Total", border=1)
        self.pdf.cell(40, 8, f"{total:.2f}", border=1)

        filename = f"{self.title.lower().replace(' ', '_')}_{doc_id}.pdf"
        self.pdf.output(filename)
        return filename

# Ejemplo de uso
if __name__ == '__main__':
    db = DBManager()
    # Agregar algunos items de ejemplo
    db.add_item('Consultoría IT', 'servicio', 150.0)
    db.add_item('Laptop Dell', 'articulo', 2500.0)

    # Listar items
    items = db.list_items()
    print("Items disponibles:", items)

    # Aquí iría la lógica de creación de cotizaciones y cuentas
    
    # Crear ítems si no existen
    items = db.list_items()
    if not items:
        db.add_item('Consultoría IT', 'servicio', 150.0)
        db.add_item('Laptop Dell', 'articulo', 2500.0)
        items = db.list_items()

    print("Items disponibles:", items)

    # Crear una cotización de ejemplo
    cliente = "Carlos Gómez"
    items_seleccionados = [
        (items[0][0], 2),  # 2 unidades del primer ítem
        (items[1][0], 1)   # 1 unidad del segundo ítem
    ]

    # Preparar detalles y total
    detalle = []
    total = 0
    for item_id, cantidad in items_seleccionados:
        for it in items:
            if it[0] == item_id:
                name = it[1]
                price = it[3]
                subtotal = cantidad * price
                detalle.append((name, cantidad, price))
                total += subtotal

    # Guardar cotización en la base de datos
    cursor = db.conn.cursor()
    fecha = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO cotizaciones (cliente, fecha, total) VALUES (?, ?, ?)', (cliente, fecha, total))
    cotizacion_id = cursor.lastrowid

    for item_id, cantidad in items_seleccionados:
        cursor.execute('INSERT INTO cotizacion_items (cot_id, item_id, quantity) VALUES (?, ?, ?)',
                       (cotizacion_id, item_id, cantidad))
    db.conn.commit()

    # Generar PDF
    pdf = PDFGenerator('Cotización')
    archivo_pdf = pdf.generate(cotizacion_id, cliente, detalle)
    print(f'Cotización generada: {archivo_pdf}')

    # y la llamada a PDFGenerator para generar el PDF correspondiente.

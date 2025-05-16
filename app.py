from flask import Flask, render_template, request, send_file
from database import Database
from pdf_generator import PDFGenerator

app = Flask(__name__)
db = Database('database.py')

@app.route('/', methods=['GET'])
def index():
    items = db.list_items()
    return render_template('index.html', items=items)

@app.route('/crear-item', methods=['GET', 'POST'])
def crear_item():
    if request.method == 'POST':
        data = request.form
        db.add_item(data['nombre'], data['tipo'], float(data['precio']))
        return render_template('item_creado.html', nombre=data['nombre'])
    return render_template('crear_item.html')

@app.route('/crear-cotizacion', methods=['POST'])
def crear_cotizacion():
    data = request.get_json()
    cliente = data['cliente']
    items = data['items']  

    # Obtener info actualizada de la base de datos
    items_info = []
    for item in items:
        db_item = db.get_item_by_id(item['item_id'])  # devuelve: (id, nombre, tipo, precio)
        if db_item:
            nombre = db_item[1]
            precio = db_item[3]
            cantidad = item['cantidad']
            items_info.append((nombre, cantidad, precio))

    # Generar PDF con los datos de la base
    pdf = PDFGenerator("Cotización")
    # Generar PDF
    from datetime import datetime

    doc_id = f"COT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    archivo = pdf.generar(doc_id, cliente, items_info)

    # Guardar cotización
    db.guardar_cotizacion(cliente, archivo)

    return {'success': True, 'archivo': archivo}
    
    # Lista de objetos con item_id y cantidad

    # Aquí va la misma lógica que usas para crear cotización y PDF
    # ...
    
    # Devuelve nombre del archivo generado
    return {'success': True, 'archivo': 'cotización_1.pdf'}

@app.route('/descargar/<filename>')
def descargar_pdf(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
# app.py
# Este archivo contiene la lógica de la aplicación Flask.
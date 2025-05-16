from flask import Flask, render_template, request, send_file
from database import Database
from pdf_generator import PDFGenerator
from datetime import datetime

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    items = db.list_items()
    return render_template('index.html', items=items)

@app.route('/items')
def lista_items():
    items = db.list_items()  # Lista todos los ítems, por ejemplo [(id, nombre, tipo, precio), ...]
    return render_template('items.html', items=items)


@app.route('/crear-item', methods=['GET', 'POST'])
def crear_item():
    if request.method == 'POST':
        data = request.form
        db.add_item(data['nombre'], data['tipo'], float(data['precio']))
        return render_template('item_creado.html', nombre=data['nombre'])
    return render_template('crear_item.html')

@app.route('/generate', methods=['POST'])
def generate():
    cliente = request.form.get('cliente')
    item_ids = request.form.getlist('items')

    if not cliente or not item_ids:
        return "Debe ingresar cliente y al menos un ítem.", 400

    items_info = []
    for item_id in item_ids:
        db_item = db.get_item_by_id(item_id)
        if db_item:
            nombre = db_item[1]
            precio = db_item[3]
            cantidad = int(request.form.get(f'cantidad_{item_id}', 1))
            items_info.append((nombre, cantidad, precio))

    doc_id = f"COT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    pdf = PDFGenerator("Cotización")
    archivo = pdf.generate(doc_id, cliente, items_info)

    db.guardar_cotizacion(cliente, archivo)

    return send_file(archivo, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

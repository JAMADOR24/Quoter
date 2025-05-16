from fpdf import FPDF
from datetime import datetime

class PDFGenerator:
    def __init__(self, titulo):
        self.pdf = FPDF()
        self.titulo = titulo

    def generar(self, doc_id, cliente, items):
        self.pdf.add_page()
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.cell(200, 10, self.titulo, ln=True, align='C')

        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(100, 10, f"ID: {doc_id}", ln=True)
        self.pdf.cell(100, 10, f"Cliente: {cliente}", ln=True)
        self.pdf.cell(100, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

        self.pdf.ln(10)
        self.pdf.cell(60, 10, "Item", 1)
        self.pdf.cell(40, 10, "Cantidad", 1)
        self.pdf.cell(40, 10, "Precio", 1)
        self.pdf.cell(40, 10, "Subtotal", 1)
        self.pdf.ln()

        total = 0
        for item_name, cantidad, precio in items:
            subtotal = cantidad * precio
            total += subtotal
            self.pdf.cell(60, 10, item_name, 1)
            self.pdf.cell(40, 10, str(cantidad), 1)
            self.pdf.cell(40, 10, f"${precio:,.2f}", 1)
            self.pdf.cell(40, 10, f"${subtotal:,.2f}", 1)
            self.pdf.ln()

        self.pdf.ln()
        self.pdf.cell(100, 10, f"Total: ${total:,.2f}", ln=True)

        filename = f"{self.titulo.lower()}_{doc_id}.pdf"
        self.pdf.output(filename)
        return filename

from flask import Flask, make_response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os

app = Flask(__name__)

@app.route("/relatorio")
def gerar_pdf():
    buffer = BytesIO()
    largura, altura = A4
    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Caminho da imagem (logo)
    logo_path = os.path.join(os.path.dirname(__file__), "logoifce.png")

    # Marca d'água (imagem centralizada e translúcida)
    if os.path.exists(logo_path):
        pdf.saveState()
        pdf.translate(largura / 2, altura / 2)
        pdf.rotate(0)
        pdf.setFillAlpha(0.1)  # Transparência
        pdf.drawImage(logo_path, -150, -150, width=300, height=300, preserveAspectRatio=True, mask='auto')
        pdf.restoreState()

    # Título
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, altura - 80, "Relatório de Pesquisas - Análise Sensorial")

    # Lista de nomes de pesquisas
    pesquisas = [
        "Análise sensorial de bolos sem glúten",
        "Estudo comparativo entre cafés orgânicos",
        "Avaliação de aceitação de sucos naturais",
        "Teste de preferência entre chocolates amargos",
        "Análise sensorial de iogurtes com probióticos",
        "Preferência de consumidores por leite vegetal",
        "Avaliação de crocância em snacks assados",
    ]

    y = altura - 120
    pdf.setFont("Helvetica", 12)

    for i, nome in enumerate(pesquisas, start=1):
        if y < 80:  # Se a página estiver cheia, cria nova página
            pdf.showPage()
            y = altura - 80
        pdf.drawString(70, y, f"{i}. {nome}")
        y -= 25

    # Finaliza e envia
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=relatorio_pesquisas.pdf'
    return response

if __name__ == "__main__":
    app.run(debug=True)

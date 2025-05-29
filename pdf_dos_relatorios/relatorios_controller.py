from flask import Flask, make_response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from main import app

from models.analise_model import Analise
from models.amostra_model import Amostra
from models.avaliacao_modal import Avaliacao
from models.conexao import *
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker 


# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.route("/relatorio/<int:analise_id>/distribuicao", methods=['GET'])
def gerar_pdf_distribuicao_avaliacao(analise_id):   

   #dados do banco 
    db = SessionLocal()
    avaliacoes = db.execute(
        select(Avaliacao)
        .join(Avaliacao.amostra)
        .join(Amostra.analise)
        .where(Analise.id == analise_id)
    ).scalars().all()     
    analise = db.query(Analise).filter_by(id=analise_id).first()
    db.close()   

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
    pdf.drawString(130, altura - 80, "Distribuição da analise:"+analise.produto)
 
    y = altura - 120
    pdf.setFont("Helvetica", 12)

    x_inicial = 150
    y = altura - 120  # topo da página
    espacamento_x = 170     # espaço entre colunas
    espacamento_y = 20      # espaço entre linhas

    for i, avaliacao in enumerate(avaliacoes):
        coluna = i % 3  # 0, 1 ou 2
        linha = i // 3
        x = x_inicial + coluna * espacamento_x

        if coluna == 0 and i != 0:
            y -= espacamento_y

        # Desenhar o número da linha apenas uma vez, no início da linha
        if coluna == 0:
            pdf.drawString(50, y, f"{linha + 1}")  # Número da linha, mais à esquerda

        texto = f"{avaliacao.numero}"
        pdf.drawString(x, y, texto)



    # Finaliza e envia
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=relatorio_pesquisas.pdf'
    return response

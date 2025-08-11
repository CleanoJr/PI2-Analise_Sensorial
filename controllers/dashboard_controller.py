from flask import render_template, make_response
from models.conexao import *
from sqlalchemy.orm import sessionmaker
from models.analise_model import Analise
from models.amostra_model import Amostra
from models.avaliacao_modal import Avaliacao
from utils.calculos import testes, calc_anova # Importando a função de cálculos
from sqlalchemy import select
from utils.calculos import calc_anova, calc_F_tabelado_5, calc_mds
from main import app

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.route('/dashboard/<int:analise_id>')
def dashboard_analise(analise_id):
    db = SessionLocal()
    
    analise = db.query(Analise).filter_by(id=analise_id).first()
    amostras = db.query(Amostra).filter_by(analise_id=analise_id).all()
    avaliadores = db.query(Avaliacao.testador_id).filter(Avaliacao.amostra_id == analise_id).distinct().count()
    
    # avaliacoes = db.query(Avaliacao).filter(Avaliacao.amostra_id.in_([a.id for a in amostras])).all()
    
    if not analise:
        return "Análise não encontrada", 404
    
    # Exemplo: buscar médias das avaliações por atributo e amostra
    resultados = []
    
    for amostra in amostras:
        
        avaliacoes = db.query(Avaliacao).filter_by(amostra_id=amostra.id).all()
        
        # Calcule médias conforme seus campos
        medias = {
            'Impressao Global': (
                sum(a.impressao_global for a in avaliacoes if a.impressao_global is not None) /
                len([a for a in avaliacoes if a.impressao_global is not None])
            ) if any(a.impressao_global is not None for a in avaliacoes) else 0,
            'Cor': (
                sum(a.cor for a in avaliacoes if a.cor is not None) /
                len([a for a in avaliacoes if a.cor is not None])
            ) if any(a.cor is not None for a in avaliacoes) else 0,
            'Aroma': (
                sum(a.aroma for a in avaliacoes if a.aroma is not None) /
                len([a for a in avaliacoes if a.aroma is not None])
            ) if any(a.aroma is not None for a in avaliacoes) else 0,
            'Textura': (
                sum(a.textura for a in avaliacoes if a.textura is not None) /
                len([a for a in avaliacoes if a.textura is not None])
            ) if any(a.textura is not None for a in avaliacoes) else 0,
            'Sabor': (
                sum(a.sabor for a in avaliacoes if a.sabor is not None) /
                len([a for a in avaliacoes if a.sabor is not None])
            ) if any(a.sabor is not None for a in avaliacoes) else 0,
            'Intenção de Compra': (
                sum(a.intencao_compra for a in avaliacoes if a.intencao_compra is not None) /
                len([a for a in avaliacoes if a.intencao_compra is not None])
            ) if any(a.intencao_compra is not None for a in avaliacoes) else 0,
        }

        # Calcula soma total de notas dadas por atributo
        # Isso é necessário para o cálculo de ANOVA
        total_notas = {
            'Impressao Global': sum(a.impressao_global for a in avaliacoes if a.impressao_global is not None),
            'Cor': sum(a.cor for a in avaliacoes if a.cor is not None),
            'Aroma': sum(a.aroma for a in avaliacoes if a.aroma is not None),
            'Textura': sum(a.textura for a in avaliacoes if a.textura is not None),
            'Sabor': sum(a.sabor for a in avaliacoes if a.sabor is not None),
            'Intenção de Compra': sum(a.intencao_compra for a in avaliacoes if a.intencao_compra is not None),
        }


        # Cria lista com a soma de notas por avaliador
        total_por_avaliador = {
            'Impressao Global': sum([a.impressao_global for a in avaliacoes if a.impressao_global is not None]),
            'Cor': sum([a.cor for a in avaliacoes if a.cor is not None]),
            'Aroma': sum([a.aroma for a in avaliacoes if a.aroma is not None]),
            'Textura': sum([a.textura for a in avaliacoes if a.textura is not None]),
            'Sabor': sum([a.sabor for a in avaliacoes if a.sabor is not None]),
            'Intenção de Compra': sum([a.intencao_compra for a in avaliacoes if a.intencao_compra is not None]),
        }

        # Cria lista com cada nota individual por atributo
        notas_individuais = {
            'Impressao Global': [a.impressao_global for a in avaliacoes if a.impressao_global is not None],
            'Cor': [a.cor for a in avaliacoes if a.cor is not None],
            'Aroma': [a.aroma for a in avaliacoes if a.aroma is not None],
            'Textura': [a.textura for a in avaliacoes if a.textura is not None],
            'Sabor': [a.sabor for a in avaliacoes if a.sabor is not None],
            'Intenção de Compra': [a.intencao_compra for a in avaliacoes if a.intencao_compra is not None],
        }

        resultados.append({'amostra': amostra, 'medias': medias})



    # Somando a quantidade de amostras
    qtd_amostras = len(amostras)
    analise.qtd_amostras = qtd_amostras

    #Calculando quantidades de avaliações
    qtd_avaliacoes = db.query(Avaliacao).filter(Avaliacao.testador_id.in_([a.id for a in amostras])).distinct().count()
    analise.qtd_avaliacoes = int(qtd_avaliacoes / qtd_amostras if qtd_amostras > 0 else 0)


    # Dicionário para armazenar resultados de ANOVA por atributo
    resultados_anova = {}

    # Mapeamento dos nomes exibidos para os nomes dos campos do modelo
    atributos_map = {
        'Impressao Global': 'impressao_global',
        'Cor': 'cor',
        'Aroma': 'aroma',
        'Textura': 'textura',
        'Sabor': 'sabor',
        'Intenção de Compra': 'intencao_compra',  # sem acento!
    }

    for atributo in atributos_map.keys():
        campo = atributos_map[atributo]
        resultados_anova[atributo] = calc_anova(
            qtd_amostras=qtd_amostras,
            qtd_avaliadores=avaliadores,
            total_notas=total_notas[atributo],
            total_por_avaliador=[getattr(a, campo) for a in avaliacoes if getattr(a, campo) is not None],
            notas_individuais=notas_individuais[atributo]
        )
    


    db.close()
    # return print(f"Resultados: {resultados}")  # Debugging line to check results

    return render_template('dashboard.html', analise=analise, resultados=resultados, avaliadores=avaliadores, qtd_amostras=qtd_amostras, resultados_anova=resultados_anova)
    # return render_template('dashboard.html', analise=analise, resultados=resultados)  
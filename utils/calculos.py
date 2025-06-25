qtd_avaliadores = 60
qtd_amostras = 3
total_amostras = qtd_amostras * qtd_avaliadores
somas_amostras = [492, 454,	437]
total_por_avaliador = [21, 25, 23, 27, 27, 26, 24, 24, 23, 24, 27, 14, 27, 25, 15, 21, 21, 22, 27, 27, 27, 27, 25, 18, 25, 25, 25, 21, 22, 18, 24, 25, 18, 27, 20, 26, 27, 26, 27, 25, 18, 27, 24, 24, 21, 24, 21, 19, 19, 24, 27, 27, 27, 17, 16, 25, 25, 17, 13, 20]
total_notas = sum(total_por_avaliador)
notas_individuais = [9,7,5,9,8,8,8,8,7,9,9,9,9,9,9,8,9,9,9,9,6,8,8,8,8,7,8,9,7,8,9,9,9,6,5,3,9,9,9,9,7,9,6,6,3,7,9,5,7,9,5,7,7,8,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,9,3,6,9,8,8,8,8,9,9,9,7,8,6,7,8,7,7,7,7,4,8,9,7,8,8,9,9,7,2,9,9,9,7,7,6,8,9,9,9,9,9,9,8,9,9,9,9,9,8,8,6,6,6,9,9,9,8,8,8,8,8,8,7,6,8,9,7,8,7,6,8,7,7,5,9,5,5,8,8,8,9,9,9,9,9,9,9,9,9,6,5,6,9,5,2,9,8,8,8,8,9,6,7,4,7,2,4,8,5,7]

def calc_anova(total_notas, total_amostras, qtd_amostras, qtd_avaliadores, total_por_avaliador, notas_individuais):
    # Fator de correção
    def fator_correcao():
        return (total_notas**2) / (total_amostras)

    #  Soma dos quadrados das Amostras
    def soma_quadrados_amostras(fator_correcao=fator_correcao()):
        sQa = 0
        for soma_amostra in somas_amostras:
            sQa += (soma_amostra**2)
        return (sQa  / qtd_avaliadores) - fator_correcao

    # Soma dos quadrados dos avaliadores
    def soma_quadrados_avaliadores(fator_correcao=fator_correcao()):
        sQav = 0
        for total_avaliador in total_por_avaliador:
            sQav += (total_avaliador**2)
        return (sQav / qtd_amostras) - fator_correcao
    
    # Soma dos quadrados Totais
    def soma_quadrados_totais(fator_correcao=fator_correcao()):
        sQt = 0
        for nota in notas_individuais:
            sQt += (nota**2)
        return sQt - fator_correcao
    
    # Soma dos quadrados do Resíduo
    def soma_quadrados_residuo():
        return (soma_quadrados_totais() - (soma_quadrados_amostras() + soma_quadrados_avaliadores()))

    return (f"FC: {round(fator_correcao(), 2)} \nsQa: {round(soma_quadrados_amostras(), 2)} \nsQav: {round(soma_quadrados_avaliadores(), 2)} \nsQt: {round(soma_quadrados_totais(), 2)} \nsQr: {round(soma_quadrados_residuo(), 2)}")

print(calc_anova(total_notas, total_amostras, qtd_amostras, qtd_avaliadores, total_por_avaliador, notas_individuais))
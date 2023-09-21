def muskingum(serie_vazao_montante, tempo_viagem_pico, coef_amortecimento = 0.3):
    
    limite_min =  1 / (2 * (1 - coef_amortecimento))
    limite_max = 1 / (2 * coef_amortecimento)
    trechos = int(tempo_viagem_pico // limite_max) + 1
    tempo_viagem_pico = tempo_viagem_pico / trechos
    
    c1 = 1 - 2 * tempo_viagem_pico * coef_amortecimento
    c2 = 1 + 2 * tempo_viagem_pico * coef_amortecimento
    c3 = 2 * tempo_viagem_pico * (1 - coef_amortecimento) - 1
    c4 = 2 * tempo_viagem_pico * (1 - coef_amortecimento) + 1

    def f(vazao_montante):
        tamanho_serie = len(vazao_montante)
        vazao_jusante = [vazao_montante[0]]
        for i in range(1, tamanho_serie):
            jusante = (c1 * vazao_montante[i] + c2 * vazao_montante[i - 1] + c3 * vazao_jusante[i - 1]) / c4
            vazao_jusante.append(jusante)
        return vazao_jusante
    
    vazao_montante = serie_vazao_montante 
    for i in range(trechos):        
        serie_vazao_jusante = f(vazao_montante)
        vazao_montante = serie_vazao_jusante

    return serie_vazao_jusante
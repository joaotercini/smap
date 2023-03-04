"""SMAP (Soil Moisture Accounting Model)

Referência:
    Lopes, J.C., Braga, J.B.F., and Conejo, J.L., 1982. SMAP – a simplified hydrological 
    model. In: V.P. Singh, ed. Applied Modelling in Catchment Hydrology. Colorado: Water 
    Resources Publications, 1218–1222.
"""
def smap(area_drenagem: float, capacidade_saturacao_solo: float, capacidade_campo: float, abstracao_inicial: float, parametro_recarga_subterranea: float, recessao_escoamento_superficial: float, recessao_escoamento_basico: float, teor_umidade_inicial: float, vazao_basica_inicial: float, serie_precipitacao: list, serie_evaporacao_potencial: list) -> list:
    """Transforma chuva em vazão

    Args:
        area_drenagem (float): Área de drenagem (km²)
        capacidade_saturacao_solo (float): Capacidade de saturação do solo (mm)
        capacidade_campo (float): Capacidade de campo (%)
        abstracao_inicial (float): Abstração inicial (mm)
        parametro_recarga_subterranea (float): Parâmetro de recarga subterrânea (%)
        recessao_escoamento_superficial (float): Constante de recessão do escoamento superficial (dias)
        recessao_escoamento_basico (float): Constante de recessão do escoamento básico (dias)
        teor_umidade_inicial (float): Teor de umidade inicial (%)
        vazao_basica_inicial (float): Vazão básica inicial (m³/s)
        serie_precipitacao (list): Série temporal de chuva diária (mm)
        serie_evaporacao_potencial (list): Série temporal de evaporação potencial diária (mm)        

    Raises:
        AttributeError: caso série tiverem tamanhos diferentes

    Returns:
        list: vazões calculadas (m³/s)
    """

    # Falta validações de faixa de valores dos parametros
    tamanho_serie = len(serie_precipitacao)
    if len(serie_evaporacao_potencial) != tamanho_serie:
        raise AttributeError(
            "As séries de precipitação e evaporação potencial tem que ser do mesmo tamanho!")

    # inicialização
    reservatorio_solo = teor_umidade_inicial / 100 * capacidade_saturacao_solo
    reservatorio_superficial = 0
    reservatorio_subterraneo = vazao_basica_inicial / (1 - 0.5 ** (1 / recessao_escoamento_basico)) / area_drenagem * 86.4

    serie_vazao = []
    for contador in range(tamanho_serie):

        precipitacao = serie_precipitacao[contador]
        evaporacao_potencial = serie_evaporacao_potencial[contador]
        teor_umidade = reservatorio_solo / capacidade_saturacao_solo

        escoamento_superficial = 0
        if precipitacao > abstracao_inicial:
            escoamento_superficial = (precipitacao - abstracao_inicial) ** 2 / (precipitacao - abstracao_inicial + capacidade_saturacao_solo - reservatorio_solo)

        evaporacao_real = evaporacao_potencial
        if (precipitacao - escoamento_superficial) < evaporacao_potencial:
            evaporacao_real = precipitacao - escoamento_superficial + \
                (evaporacao_potencial - precipitacao +
                 escoamento_superficial) * teor_umidade

        recarga_subterranea = 0
        if reservatorio_solo > (capacidade_campo / 100 * capacidade_saturacao_solo):
            recarga_subterranea = parametro_recarga_subterranea / 100 * teor_umidade * \
                (reservatorio_solo - capacidade_campo / 100 * capacidade_saturacao_solo)

        escoamento_direto = reservatorio_superficial * (1 - 0.5 ** (1 / recessao_escoamento_superficial))

        escoamento_basico = reservatorio_subterraneo * (1 - 0.5 ** (1 / recessao_escoamento_basico))

        reservatorio_solo = reservatorio_solo + precipitacao - escoamento_superficial - evaporacao_real - recarga_subterranea
        reservatorio_superficial = reservatorio_superficial + escoamento_superficial - escoamento_direto
        reservatorio_subterraneo = reservatorio_subterraneo + recarga_subterranea - escoamento_basico

        vazao = (escoamento_direto + escoamento_basico) * area_drenagem / 86.4
        serie_vazao.append(vazao)

    return serie_vazao

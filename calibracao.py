import pandas as pd
from spotpy import objectivefunctions
from smap import smap
from scipy.optimize import minimize


def calibracao(area_drenagem, index, serie_precipitacao, serie_evaporacao_potencial, serie_vazao_observada, limites):

    def roda(p):
        p1, p2, p3, p4, p5, p6, p7, p8 = p

        return smap(
            area_drenagem=area_drenagem,
            capacidade_saturacao_solo=p1,
            capacidade_campo=p2,
            abstracao_inicial=p3,
            parametro_recarga_subterranea=p4,
            recessao_escoamento_superficial=p5,
            recessao_escoamento_basico=p6,
            teor_umidade_inicial=p7,
            vazao_basica_inicial=p8,
            serie_precipitacao=serie_precipitacao,
            serie_evaporacao_potencial=serie_evaporacao_potencial
        )

    def avalia(serie_vazao_calculada):
        return {
            'KGE': objectivefunctions.kge(serie_vazao_observada, serie_vazao_calculada),
            'NSE': objectivefunctions.nashsutcliffe(serie_vazao_observada, serie_vazao_calculada),
            'R2': objectivefunctions.rsquared(serie_vazao_observada, serie_vazao_calculada),
            'PBIAS': objectivefunctions.pbias(serie_vazao_observada, serie_vazao_calculada),
            'Log-NSE': objectivefunctions.lognashsutcliffe(serie_vazao_observada, serie_vazao_calculada),
        }

    def obj_nse(p):
        serie_vazao_calculada = roda(p)
        nse = objectivefunctions.nashsutcliffe(
            serie_vazao_observada, serie_vazao_calculada)
        return -nse

    def obj_log_nse(p):
        serie_vazao_calculada = roda(p)
        log_nse = objectivefunctions.lognashsutcliffe(
            serie_vazao_observada, serie_vazao_calculada)
        return -log_nse

    def obj_kge(p):
        serie_vazao_calculada = roda(p)
        kge = objectivefunctions.kge(
            serie_vazao_observada, serie_vazao_calculada)
        return -kge

    x0 = []
    for i in limites:
        x0.append((i[0]+i[1])/2)

    res_nse = minimize(fun=obj_nse, x0=x0, bounds=limites)
    res_log_nse = minimize(fun=obj_log_nse, x0=x0, bounds=limites)
    res_kge = minimize(fun=obj_kge, x0=x0, bounds=limites)

    series = pd.DataFrame(index=index)
    series['Observada'] = serie_vazao_observada
    series['NSE'] = roda(res_nse.x)
    series['Log-NSE'] = roda(res_log_nse.x)
    series['KGE'] = roda(res_kge.x)

    avaliacao = pd.DataFrame()
    for i in series.columns:
        avaliacao[i] = avalia(series[i])
    
    params = pd.DataFrame(
        index=['Capacidade de saturação do solo (mm)',
             'Capacidade de campo (%)',
             'Abstração inicial (mm)',
             'Parâmetro de recarga subterrânea (%)',
             'Constante de recessão do escoamento superficial (dias)',
             'Constante de recessão do escoamento básico (dias)',
             'Teor de umidade inicial (%)',
             'Vazão básica inicial (m³/s)'])    
    params['NSE']= res_nse.x
    params['Log-NSE']= res_log_nse.x
    params['KGE']= res_kge.x    


    return {
        'series': series,
        'avaliacao': avaliacao,
        'params': params
    }

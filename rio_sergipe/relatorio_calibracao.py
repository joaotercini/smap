import os
import sys
dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.dirname(dir)
sys.path.append(base_dir)
import pandas as pd
import numpy as np
from calibracao import calibracao

area_drenagem = 2070

df = pd.read_csv('rio_sergipe/1992-2018.csv', index_col=0, parse_dates=True)
serie_precipitacao = df['precipitacao'].to_list()
serie_evaporacao_potencial = (df['evaporacao_potencial']).to_list()
serie_vazao_observada = df['vazao_observada'].to_list()

Qini = np.mean(serie_vazao_observada[0:7])

limites = [[100.0, 2000.0],     # Capacidade de saturação do solo (mm)
            [30.0, 50.0],           # Capacidade de campo (%)
            [2.5, 5.0],           # Abstração inicial (mm)
            [0.0, 20.0],          # Parâmetro de recarga subterrânea (%)
            [0.2, 5.0],           # Constante de recessão do escoamento superficial (dias)
            [30.0, 180.0],        # Constante de recessão do escoamento básico (dias)
            [0.0, 100.0],       # Teor de umidade inicial (%)
            [Qini-1, Qini+1]]   # Vazão básica inicial (m³/s)

c = calibracao(area_drenagem, df.index, serie_precipitacao, serie_evaporacao_potencial, serie_vazao_observada, limites)

with pd.ExcelWriter('rio_sergipe/1992-2018.xlsx') as writer:
    c['series'].to_excel(writer, sheet_name="series")
    c['params'].to_excel(writer, sheet_name="params")
    c['avaliacao'].to_excel(writer, sheet_name="avaliacao")

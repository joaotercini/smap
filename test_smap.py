'''Testando Pinheirinho'''
import pandas
import matplotlib.pyplot as plt
from smap import smap

test_data = pandas.read_csv('test_data_smap.csv')
serie_precipitacao = test_data['precipitacao']
serie_evaporacao_potencial = test_data['evaporacao_potencial']
serie_vazao_observada = test_data['vazao_observada']


# Capacidade de saturação do solo (mm)
curve_number = 45
teor_umidade_inicial = 38
capacidade_saturacao_solo = 25.4 * (1000 / curve_number - 10) / (1 - teor_umidade_inicial / 100)

serie_vazao_calculada = smap(113, capacidade_saturacao_solo, 35, 5, 1.3, 1.94, 98.67, teor_umidade_inicial, 1, serie_precipitacao, serie_evaporacao_potencial)

plt.plot(serie_vazao_calculada)
plt.plot(serie_vazao_observada)
plt.legend(['Calculada', 'Observada'])
plt.ylabel('vazão (m³/s)')
plt.xlabel('dias')
plt.show()

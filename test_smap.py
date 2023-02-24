'''Testando Pinheirinho'''
import pandas
import matplotlib.pyplot as plt
from smap import smap

test_data = pandas.read_csv('test_data_smap.csv')
serie_precipitacao = test_data['precipitacao']
serie_evaporacao_potencial = test_data['evaporacao_potencial']
serie_vazao_observada = test_data['vazao_observada']

serie_vazao_calculada = smap(113, 45, 35, 5, 1.3, 1.94, 98.67,
                             38, 1, serie_precipitacao, serie_evaporacao_potencial)

plt.plot(serie_vazao_calculada)
plt.plot(serie_vazao_observada)
plt.legend(['Calculada', 'Observada'])
plt.ylabel('vazão (m³/s)')
plt.xlabel('dias')
plt.show()

# for vazao in serie:
#    print(f'{vazao:.2f}')

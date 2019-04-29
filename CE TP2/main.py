from frase import frase
from frase import populacao
import random

'''criando uma populacao de frases'''

print('criando uma nova populacao de frase')

p = populacao(100)
p.imprimePop()
print ''
p.imprimePopSorted()
while 1:
    if p.frases[0].fit == 0 or p.geracao > 500:
        break
    p.novaGeracao()
print(p.geracao)
p.imprimePop()

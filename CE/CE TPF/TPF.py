import matplotlib.pyplot as plt
import random
from random import randint as rin
import math
from math import pow as pow
import csv

class pos(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class cliente(object):
    def __init__(self):
        self.pos = []


class populacao(object):
    def __init__(self, c = cliente(), tam = 5):
        self.upa = []
        self.selecao = [] #quais upas estao selecionadas para cada cliente
        solucao = []
        for j in range(tam):
            for i in range(5):
                solucao.append(c.pos[rin(0,len(c.pos))])
            self.upa.append(solucao)
            solucao = []

    def fit(self, c = cliente()):
        pass

    def minUPA(self, c = cliente()):
        temp = []
        temp2 = []
        for j in self.upa:
            pos = c.pos
            min = 10000
            temp2 = []
            for k in j:
                for i in len(pos):
                    a = pow(pow(k.x - c.x, 2) + pow(k.y - c.y, 2), 1/2)
                    if min > a:
                        min = a
                        temp = k
                        b = i
                pos.remove(pos[b])
                temp2.append(temp)
            self.selecao.append(temp2)
c = cliente()


with open('pmedian324.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ' ')
    for linha in plots:
        c.pos.append(pos(int(linha[0]), int(linha[1])))




plt.scatter(c.x,c.y, label = 'Bairros',marker = '+')
plt.xlabel('x')
plt.ylabel('y')

#plt.xticks(x)
#plt.yticks(y)


plt.Artist()
plt.title('Distribuição de Bairros')
plt.legend()
plt.show()

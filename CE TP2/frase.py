import random

referencia = 'METHINKS*IT*IS*LIKE*A*WEASEL'
alfabetoPadrao = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ*1234567890'

class frase(object):
    "Esta eh a classe frase. Ela engloba uma frase composta"
    "de palavras espacadas por * (asteriscos). "
    "As palavras podem ser compostas por uma combinacao de "
    "qualquer uma das letras 26 letras do alfabeto, ou seja"
    "sao 27 possiveis caracteres no total."


    '''CONSTRUTOR DE FRASE ALEATORIA'''
    def __init__(self):
        self.sentenca = self.initFrase()
        self.fit = 0
        self.fitness()
        self.tam = len(referencia)
    '''INICIALIZAZAO DE FRASE OBJETIVO - aqui o espaco de busca eh reduzido a partir '''
    def initFrase(self):
        #alfabeto = self.selecaoAlfabeto() #heuristica
        alfabeto = alfabetoPadrao
        tamA = len(alfabeto)
        fra = ''
        for i in range(len(referencia)):
            fra += alfabeto[random.randint(0, tamA - 1)]
        return fra
    pass

    def fitness(self):
        fit = len(referencia)
        tam = len(referencia)
        if len(referencia) != len(self.sentenca):
            fit += 1000
        else:
            for i in range(tam):
                if (referencia[i] == self.sentenca[i]):
                    fit -= 1
        self.fit = fit
    pass

    def selecaoAlfabeto(self):
        temp = '' #espaco de busca
        test = 0 #o caracter esta no espaco de busca temp
        for i in range(len(referencia)):
            for j in range(len(temp)):
                if (temp[j] == referencia[i]):
                    test = 1
            if (test == 0):
                temp += referencia[i]
            test = 0
        return temp

    def __eq__(self, other):
        return self.sentenca == other.sentenca


class populacao(object):
    "Esta eh a classe populacao de frases. Ela engloba uma "
    "geracao inteira de frases e tem como parametro:       "
    "O seu tamanho (tamPop),"
    "A idade da geracao (geracao)"
    "Frases que compoem a populacao(frases)"

    def __init__(self, tam = 0):
        self.tamPop = tam
        self.geracao = 0
        self.frases = []
        self.initPop()
        self.tamPopAtual = len(self.frases)

    def initPop(self):
        for i in range(self.tamPop):
            self.frases.append(frase())

    def imprimePop(self):
        for i in range(0, self.tamPopAtual):
            print(self.frases[i].sentenca, self.frases[i].fit, len(self.frases[i].sentenca))

    def transa(self, pai = frase(), mae = frase()):
        npoint = []
        npoint.append(0)
        naster = 0
        filho1 = frase()
        filho2 = frase()
        temp1 = ''
        temp2 = ''
        mut = 0.75
        aP = []

        for i in range(len(referencia)):
            if (random.uniform(0,1) > 0.9):    #fator mutacao genetica
                #aP = list(self.frases[0].selecaoAlfabeto())
                aP = list(alfabetoPadrao)
                temp1 = temp1 + aP[random.randint(0, len(aP) - 1)]
            elif (random.uniform(0,1) <= mut): #escolha de qual dos pais
                temp1 = temp1 + pai.sentenca[i]
                temp2 = temp2 + mae.sentenca[i]
            else:
                temp1 = temp1 + mae.sentenca[i]
                temp2 = temp2 + pai.sentenca[i]
        filho1.sentenca = temp1
        filho2.sentenca = temp2
        filho1.fitness()
        filho2.fitness()
        self.frases.append(filho1)
        self.frases.append(filho2)
        self.tamPopAtual += 2

    def imprimePopSorted(self):
        temp = self.frases
        temp = sorted(self.frases,key = lambda x: x.fit)
        for i in range(0, self.tamPopAtual):
            print(temp[i].sentenca, temp[i].fit, len(temp[i].sentenca))

    def novaGeracao(self):
        pais = sorted(self.frases, key = lambda x: x.fit)
        for i in range(len(self.frases) - 1):
            self.transa(pais[i], pais[i+1])
        self.frases = sorted(self.frases, key = lambda x: x.fit)
        while len(self.frases) > self.tamPop:
            self.frases.pop()
            self.tamPopAtual -= 1
        self.geracao += 1
    pass

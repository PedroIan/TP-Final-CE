# -*- coding: utf-8 -*-
import socket
import random

allNums = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
allNipes = ['♦', '♥', '♠', '♣']
#allNipes = ['O', 'C', 'E', 'P']
allSeq = [['A','2','3','4','5'],\
            ['2','3','4','5','6'],\
            ['3','4','5','6','7'],\
            ['4','5','6','7','8'],\
            ['5','6','7','8','9'],\
            ['6','7','8','9','10'],\
            ['7','8','9','10','J'],\
            ['8','9','10','J','Q'],\
            ['9','10','J','Q','K'],\
            ['10','J','Q','K','A']] #todas as sequencias possiveis no jogo

version = 1.1

class carta(object): #classe carta, possuindo nipe e numero
    def __init__(self, numero = 0, nipe = 0, valor = 0):
        self.numero = numero
        self.nipe = nipe
        self.valor = valor
    def __eq__(self, other):
        if isinstance(other, carta):
            return self.valor == other.valor
        return false

class deck(object): #deck eh um vetor de cartas, embaralhado por default
    def __init__(self, cartas = []):
        count = 0
        self.cartas = cartas
        for i in allNums:
            for k in allNipes:
                self.cartas.append(carta(i, k, count))
                count += 1
        random.shuffle(self.cartas)

    def pop(self):
        temp = self.cartas.pop(0)
        return temp

class player(object): #classe jogador possui um vetor de cartas (mao) e um de jogadas possiveis
                      #possui tambem funcoes necessarias para o cliente
    def __init__(self, cartas = [], count = 0):
        self.cartas = cartas
        self.jogadas = []
        self.jogadaAtual = []
        self.count = len(cartas)

    def printHand(self):
        if len(self.cartas) == 0:
            print("Mao vazia")
            return
        for i in self.cartas:
            print(i.numero, i.nipe)

    def printJogadas(self):
        if len(self.jogadas) == 0:
            print("Nao ha jogadas")
            return
        for i in self.jogadas:
            print(i.numero, i.nipe)

    def orgNipe(self, cards = []):
        temp = []
        for i in allNipes:
            for k in cards:
                if k.nipe == i:
                    temp.append(k)
        return temp

    def orgNum(self, cards = []):
        temp = []
        for i in allNums:
            for k in cards:
                if k.numero == i:
                    temp.append(k)
        return temp

    def dupla(self, cartasRecebidas = []):
        temp = []
        aux = 1
        for i in range(len(cartasRecebidas)):
            for k in cartasRecebidas:
                if 0 < len(temp):
                    for j in temp:
                        if k.numero == j.numero and k.nipe == j.nipe:
                            aux = 0
                            break
                        aux = 1
                if cartasRecebidas[i].numero == k.numero and cartasRecebidas[i].nipe != k.nipe and aux:
                    temp.append(k)
        try:
            tri = self.trinca(temp)
            for j in tri:
                temp.remove(j)
        finally:

            temp = self.orgNum(temp)
            return temp

    def trinca(self, cartasRecebidas = []):
        cartasRecebidas = self.orgNum(cartasRecebidas)
        temp = []
        for i in range(len(cartasRecebidas) - 2):
            for k in range(i + 1, len(cartasRecebidas) - 1):
                if (cartasRecebidas[i].numero == cartasRecebidas[k].numero and cartasRecebidas[i].numero == cartasRecebidas[k + 1].numero):
                    temp.append(cartasRecebidas[i])
                    temp.append(cartasRecebidas[k])
                    temp.append(cartasRecebidas[k + 1])
                    i += 2
        temp = self.orgNum(temp)
        return temp

    def quadra(self, cartasRecebidas = []):
        cartasRecebidas = self.orgNum(cartasRecebidas)
        temp = []
        for i in range(len(cartasRecebidas) - 3):
            for k in range(i + 1, len(cartasRecebidas) - 2):
                card1 = cartasRecebidas[i].numero
                card2 = cartasRecebidas[k].numero
                card3 = cartasRecebidas[k + 1].numero
                card4 = cartasRecebidas[k + 2].numero
                if (card1 == card2 and card1 == card3 and card1 == card4):
                    temp.append(cartasRecebidas[i])
                    temp.append(cartasRecebidas[k])
                    temp.append(cartasRecebidas[k + 1])
                    temp.append(cartasRecebidas[k + 2])
        return temp

    def sequencia(self, cartasRecebidas = []):
        cartasRecebidas = self.orgNum(cartasRecebidas)
        temp1 = []
        temp2 = []
        card = []
        for i in allNums:
            for k in cartasRecebidas:
                if k.numero == i:
                    temp1.append(k)
                    break

        for j in range(len(temp1) - 4):
            for l in range(0,5):
                card.append(temp1[j + l].numero)
            if card in allSeq:
                temp2.append(temp1[j])
                temp2.append(temp1[j + 1])
                temp2.append(temp1[j + 2])
                temp2.append(temp1[j + 3])
                temp2.append(temp1[j + 4])
            if len(temp2) > 0:
                break
        return temp2

    def flush(self, cartasRecebidas = []):
        temp1 = self.orgNipe(cartasRecebidas)
        temp2 = []
        for i in allNipes:
            for k in range(len(temp1) - 4):
                if temp1[k].nipe == i and temp1[k + 1].nipe == i and temp1[k + 2].nipe == i and temp1[k + 3].nipe == i and temp1[k + 4].nipe == i:
                    temp2.append(temp1[k])
                    temp2.append(temp1[k + 1])
                    temp2.append(temp1[k + 2])
                    temp2.append(temp1[k + 3])
                    temp2.append(temp1[k + 4])
                    break
            if len(temp2) > 0:
                break
        temp2 = self.orgNum(temp2)
        return temp2

    def fullhouse(self, cartasRecebidas = []):
        tri = self.trinca(cartasRecebidas)
        dup = self.dupla(cartasRecebidas)
        temp = []
        if len(dup) > 0 and len(tri) > 0:
            try:
                temp.append(dup[0])
                temp.append(dup[1])
                temp.append(tri[0])
                temp.append(tri[1])
                temp.append(tri[2])
            finally:
                dup = []
                tri = []
        return temp


    def jogada(self, play = 0):
        temp = []
        if play == 1:   #organiza jogos de um na ordem crescente
            self.jogadas = self.orgNum(self.cartas)
        elif play == 2: #organiza os jogos de pares na ordem crescente
            self.jogadas = self.dupla(self.cartas)
        elif play == 3: #organiza os jogos de trincas na ordem crescente
            self.jogadas = self.trinca(self.cartas)
        elif play == 5:
            singles = self.orgNum(self.cartas)
            pairs = self.dupla(self.cartas)
            threeOf = self.trinca(self.cartas)
            #self.jogadas = self.sequencia(self.cartas)
            seq = self.sequencia(self.cartas)
            flushes = self.flush(self.cartas)
            self.jogadas = self.quadra(self.cartas)
            fourOf = self.quadra(self.cartas)
            print('')



class dealer(object): #dealer eh uma classe utilizada pelo servidor, possuindo um vetor baralho e um de cartas descartadas.
    def __init__(self, baralho = deck(), mesa = [], count = 0):
        self.baralho = baralho
        self.mesa = mesa
        self.count = count

    def distribuicao(self):
        cards = []
        for i in range(0,13):
            cards.append(self.baralho.pop())
            self.count += 1
        return cards
        #usu.jogadas = usu.orgNum(usu.jogadas)
        #return usu
        #usu.orgNipe()
        #usu.printHand()
        #usu.orgNum()
        #usu.printHand()

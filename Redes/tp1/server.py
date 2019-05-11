# -*- coding: utf-8 -*-
import random
import socket
import threading
import pickle
import base

#Conexao CLIENTE-SERVIDOR

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, dealer = base.dealer(), jogadas = [], posi = 0):

        self.player = dealer.distribuicao()
        self.endCli = clientAddress
        self.jogadas = jogadas

        threading.Thread.__init__(self)
        self.sockCli = clientsocket

        print("Nova conexão, endereço do cliente: ",self.endCli)

    def run(self):
        print("Conexao com: ", self.endCli)
        msg = ""

        #Real comunicação entre cliente e servidor
        while True:
            data = self.sockCli.recv(2048)
            if not data:
                break
            try:
                if data == b'get':
                    self.sockCli.send(pickle.dumps(self.player))
                elif data == b'bye':
                    break
            finally:
                #print("from:", self.endCli, msg)
                print('')
        self.sockCli.close()
        print("Cliente com endereço ", self.endCli, " desconectado...")
        self._stop()



LOCALHOST = "127.0.0.1"
PORT = 50000

#Conexão TCP/IP preparação para conexão cliente servidor (lado servidor)

print("Inicializando servidor....")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Esperando por requisições.............")

#Variável auxiliar para receber clientes
aux_count_Clientes = 0
dealer = base.dealer()
jogador = base.player()
newThreads = []
mesa = []
while (aux_count_Clientes < 4):
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newThreads.append(ClientThread(clientAddress, clientsock, dealer, aux_count_Clientes))
    newThreads[aux_count_Clientes].start()
    aux_count_Clientes += 1

#Descobrir quem é o primeiro a jogar
aux = 0
playAtual = -1
rodada = 0
for i in newThreads:
    for k in i.player:
        if k.valor == 0:
            playAtual = aux
            break
    if playAtual != aux:
        aux += 1
    else:
        break

while True:
    typeAtual = 0 #1 singles, 2 dupla, 3 trinca, 4 sequencia, 5 flush, 6 fullhouse, 7 quadra
    typeJogada = 0 #1 singles, 2 dupla, 3 trinca, 4 sequencia, 5 flush, 6 fullhouse, 7 quadra
    highest = 0 #maior carta da jogada
    mesaTemp = []
    if not dealer.mesa:
        newThreads[playAtual].sockCli.send(bytes("Sua vez de jogar, mesa vazia", "UTF-8"))
    else:
        newThreads[playAtual].sockCli.send(bytes("Sua vez de jogar", "UTF-8"))
        newThreads[playAtual].sockCli.send(pickle.dumps(dealer.mesa))
    try:
        mesaTemp = pickle.loads(newThreads[playAtual].sockCli.recv(2048))
    except:
        pass
    '''if mesa == b'skip':
        rodada += 1
    else:'''
    while len(mesaTemp) != len(dealer.mesa) and rodada != 0:
        newThreads[playAtual].sockCli.send(bytes("Jogada invalida", "UTF-8"))
        try:
            mesaTemp = pickle.loads(newThreads[playAtual].sockCli.recv(2048))
        except:
            pass
        if mesaTemp == b'skip':
            break
    if len(mesaTemp) == 1:
        typeAtual = 1
        highest = mesaTemp[-1].valor
    elif len(mesaTemp) == 2:
        typeAtual = 2
        highest = mesaTemp[-1].valor
    elif len(mesaTemp) == 3:
        typeAtual = 3
        highest = mesaTemp[-1].valor
    elif mesaTemp == jogador.quadra(mesaTemp):
        typeAtual = 7
        highest = mesaTemp[-1].valor
    elif mesaTemp == jogador.flush(mesaTemp):
        typeAtual = 5
        highest = mesaTemp[-1].valor
    elif mesaTemp == jogador.fullhouse(mesaTemp):
        typeAtual = 6
        highest = mesaTemp[-1].valor
    print(highest)
    rodada += 1
    for i in mesaTemp:
        for k in newThreads[playAtual].player:
            if i.numero == k.numero and i.nipe == k.nipe:
                newThreads[playAtual].player.remove(k)
    dealer.mesa = mesaTemp
    playAtual = (playAtual + 1)%4

# -*- coding: utf-8 -*-
import socket
import pickle
import threading
import base
import sys
import time

#Cliente

class ServerThread(threading.Thread):
    def __init__(self, servAddress, servSocket, player = base.player()):

        self.endServ = servAddress
        self.sockServ = servSocket
        threading.Thread.__init__(self)

        print("Nova conexão, endereço do sevidor: ",self.endServ)

    def run(self, player = base.player()):
        msg = ''
        while True:
            data = self.sockServ.recv(2048)
            if not data:
                break
            try:
                msg = data.decode()
                print("from server:", self.endServ, data)
            except:
                msg = data
            try:
                player.jogadas = pickle.loads(data)
                print("A última jogada foi:")
                player.printJogadas()
            except:
                msg = data
        self.sockServ.close()
        print("Servidor com endereço ", self.endServ, " desconectado...")
        self._stop()

SERVER = "127.0.0.1"
PORT = 50000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
serverSock = client.dup()
client.sendall(bytes('get', 'UTF-8'))
jogador = base.player(pickle.loads(client.recv(1024)))
thread = ServerThread(SERVER, serverSock, jogador)
thread.start()

while True:
    out_data = input()

    if out_data == 'get':
        client.sendall(bytes(out_data, 'UTF-8'))
        jogador.cartas = pickle.loads(client.recv(1024))
        jogador.printHand()
    elif out_data=='bye':
        client.close()
        break
    elif out_data == 'single':
        jogador.jogadas = []
        temp = jogador.orgNum(jogador.cartas)
        temp = temp[0]
        jogador.jogadas.append(temp)
        jogador.printJogadas()
    elif out_data == 'dupla':
        jogador.jogadas = []
        dup = jogador.dupla(jogador.cartas)
        try:
            jogador.jogadas.append(dup[0])
            jogador.jogadas.append(dup[1])
        finally:
            jogador.printJogadas()
    elif out_data == 'trinca':
        jogador.jogadas = []
        jogador.jogadas = jogador.trinca(jogador.cartas)
        jogador.printJogadas()
    elif out_data == 'seq':
        jogador.jogadas = []
        jogador.jogadas = jogador.sequencia(jogador.cartas)
        jogador.printJogadas()
    elif out_data == 'flu':
        jogador.jogadas = []
        jogador.jogadas = jogador.flush(jogador.cartas)
        jogador.printJogadas()
    elif out_data == 'quadra':
        jogador.jogadas = []
        jogador.jogadas = jogador.quadra(jogador.cartas)
        jogador.printHand()
    elif out_data == 'full':
        jogador.jogadas = []
        jogador.jogadas = jogador.fullhouse(jogador.cartas)
        jogador.printJogadas()
    elif out_data == 'cmd':
        print("Comandos possíveis:")
        print("get      - pede a mão atual para o servidor")
        print("num      - imprime a mão em ordem numérica")
        print("send     - envia a última jogada selecionada para o servidor")
        print("bye      - encerra a conexão com o servidor")
        print("")
        print("singles  - imprime o menor jogo de uma carta possível")
        print("dupla    - imprime as duplas")
        print("trinca   - imprime as trincas")
        print("seq      - imprime as sequencias")
        print("flu      - imprime os flushes")
        print("quadra   - imprime as quadras")
        print("full     - imprime os fullhouses")
    elif out_data == 'send':
        client.sendall(pickle.dumps(jogador.jogadas))
        time.sleep(1)
        client.sendall(bytes('get', 'UTF-8'))
        jogador.cartas = pickle.loads(client.recv(2048))
        print("Sua mão atual é:")
        jogador.printHand()
    elif out_data == 'num':
        jogador.jogadas = []
        jogador.jogadas = jogador.orgNum(jogador.cartas)
        jogador.printJogadas()
    '''elif out_data == 'skip':
        client.sendall(bytes(out_data, 'UTF-8'))'''

from socket import *
import json

HOST = 'localhost'
PORTA = 9093

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((HOST, PORTA))
sockobj.listen(1)

while True:
    conexao, endereco = sockobj.accept()
    print('Conectado', endereco)

    while True:
        data = conexao.recv(1024)
        print("User and password: ", json.loads(data))

        resposta = "Executado"
        conexao.send(resposta.encode())

    print('Desconectado', endereco)
    conexao.close()

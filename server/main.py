from socket import *
from repositories.user_repository import UserRepository
import json

HOST = 'localhost'
PORTA = 9093

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((HOST, PORTA))
sockobj.listen(1)

tentativas = 0
user_repository = UserRepository()
while True:
    conexao, endereco = sockobj.accept()
    print('Conectado', endereco)

    while True:
        data = conexao.recv(1024)
        print("User and password: ", json.loads(data))
        credentials = json.loads(data)

        if tentativas == 2:
            print('Você atingiu o limite de tentativas!')
            conexao.close()
            break

        user = user_repository.find(credentials['user'], credentials['password'])
        if user is not None:
            resposta = "Autenticado com sucesso"
            conexao.send(resposta.encode())
            conexao.send(json.dumps({'logged_in': True}).encode())
        else:
            tentativas += 1
            conexao.send('Autenticação falhou!'.encode())


    print('Desconectado', endereco)
    conexao.close()

print()
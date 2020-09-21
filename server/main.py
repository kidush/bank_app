from socket import *
from repositories.user_repository import UserRepository
import json

HOST = 'localhost'
PORTA = 9093

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((HOST, PORTA))
sockobj.listen(1)

tries = 0
user_repository = UserRepository()
while True:
    connection, address = sockobj.accept()
    print('Conectado', address)

    while True:
        data = connection.recv(1024)
        print("User and password: ", json.loads(data))
        credentials = json.loads(data)

        if tries == 2:
            print('Você atingiu o limite de tentativas!')
            connection.close()
            break

        user = user_repository.find(credentials['user'], credentials['password'])
        if user is not None:
            connection.send("Autenticado com sucesso".encode())
            connection.send(json.dumps({'logged_in': True}).encode())
        else:
            tries += 1
            connection.send('Autenticação falhou!'.encode())

    print('Desconectado', address)
    connection.close()
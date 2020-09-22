from socket import socket, AF_INET, SOCK_STREAM
import json

class Server:
    def __init__(self, fake_user, host='localhost', port=9093):
        self.fake_user = fake_user
        self.tries = 0
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.bind((host, port))
        self.sockobj.listen(1)

    def run(self):
        while True:
            connection, address = self.sockobj.accept()
            print('Conectado', address)

            while True:
                data = connection.recv(1024)
                credentials = json.loads(data)

                if self.tries == 2:
                    print('Você atingiu o limite de tentativas!')
                    connection.close()
                    break

                if credentials['user'] == fake_user['username'] and credentials['password'] == fake_user['password']:
                    connection.send(json.dumps({ 'logged_in': True }).encode())
                else:
                    self.tries += 1
                    connection.send(json.dumps({ 'logged_in': False }).encode())

            print('Desconectado', address)
            connection.close()

fake_user = {
    'username': 'admin',
    'password': '123123123'
}

Server(fake_user).run()
from socket import socket, AF_INET, SOCK_STREAM
import json

class Server:
    LOGIN_ATTEMPTS_LIMIT = 2

    def __init__(self, fake_user, host='localhost', port=9093):
        self.fake_user = fake_user
        self.login_attempts = 0
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.bind((host, port))
        self.sockobj.listen(1)

    def run(self):
        while True:
            connection, address = self.sockobj.accept()
            print('Conectado', address)

            while True:
                data = connection.recv(1024)
                
                if self.authenticate(connection, data):
                    connection.send(json.dumps({ 'logged_in': True }).encode())
                else:
                    connection.send(json.dumps({ 'logged_in': False }).encode())
                
                if self.is_login_attempts_reached():
                    connection.close()
                    return False

            print('Desconectado', address)
            connection.close()

    def is_user_authenticated(self, user, password):
        return user == self.fake_user['username'] and password == self.fake_user['password']

    def authenticate(self, connection, data):
        credentials = json.loads(data)

        if self.is_user_authenticated(credentials['user'], credentials['password']):
            return True
        else:
            self.login_attempts += 1

    def is_login_attempts_reached(self):
        return self.login_attempts == self.LOGIN_ATTEMPTS_LIMIT
        

fake_user = {
    'username': 'admin',
    'password': '123123123'
}

Server(fake_user).run()
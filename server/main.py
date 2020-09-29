from socket import socket, AF_INET, SOCK_STREAM
import json

class Server:
    LOGIN_ATTEMPTS_LIMIT = 2

    def __init__(self, host='localhost', port=9093, balance=0):
        self.fake_user = {
            'username': 'admin',
            'password': '123123123'
        }
        self.login_attempts = 0
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.bind((host, port))
        self.sockobj.listen(1)
        self.connection, self.address = self.sockobj.accept()
        self.balance = 0

    def run(self):
        while True:
            print('Conectado', self.address)

            while True:
                data = self.connection.recv(1024)
                
                if self.authenticate(data):
                    self.connection.send(json.dumps({ 'logged_in': True }).encode())
                else:
                    self.connection.send(json.dumps({ 'logged_in': False }).encode())
                
                if self.is_login_attempts_reached():
                    self.connection.close()
                    return False

            print('Desconectado', self.address)
            self.connection.close()

    def is_user_authenticated(self, user, password):
        return user == self.fake_user['username'] and password == self.fake_user['password']

    def authenticate(self, data):
        credentials = json.loads(data)

        if self.is_user_authenticated(credentials['user'], credentials['password']):
            return True
        else:
            self.login_attempts += 1

    def is_login_attempts_reached(self):
        return self.login_attempts == self.LOGIN_ATTEMPTS_LIMIT

    def choose_option(self, option):
        options = {
            '1': self.deposit,
            '2': self.withdraw
        }
        return options[option]()

    def withdraw(self, value):
        if self.balance <= 0:
            return self.connection.send(json.dumps({'error': True, 'message': f'Você não tem saldo suficiente para retirar R$ {value}'}).encode())

    def deposit():
        pass

Server().run()

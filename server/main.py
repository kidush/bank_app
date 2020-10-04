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
        self.authenticated = False

    def run(self):
        while True:
            print('Conectado', self.address)

            while True:
                data = self.connection.recv(1024)
                
                if not self.authenticated:
                    if self.authenticate(data):
                        self.authenticated = True
                        self.connection.send(json.dumps({ 'logged_in': True }).encode())
                    else:
                        self.connection.send(json.dumps({ 'logged_in': False }).encode())
                
                    if self.is_login_attempts_reached():
                        break 
                else:
                    if data.decode() == None or data.decode() == '':
                        break

                    response_data = json.loads(data.decode())
                    self.choose_option(response_data['option'], response_data['value'])
                    
            print('Desconectado', self.address)
            self.connection.close()
            break

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

    def choose_option(self, option, value=None):
        options = {
            '1': (lambda : self.deposit(value)),
            '2': (lambda : self.withdraw(value)),
            '3': (lambda : self.current_balance()),
            '4': (lambda : self.exit())
        }

        return options[option]()

    def withdraw(self, value):
        value = int(value)
        if self.balance <= 0:
            return self.server_message(f'Você não tem saldo suficiente para retirar R$ {value}', error=True)
        elif value > self.balance:
            return self.server_message(f'O valor que você solicitou é maior do que seu saldo: R$ {self.balance}', error=True)
        else:
            self.balance -= value
            return self.server_message(f'Valor sacado: R$ {value}')

    def deposit(self, value):
        value = int(value)
        self.balance += value
        return self.server_message(f'Olá, Seu novo saldo é: R$ {self.balance}')
    
    def current_balance(self):
        self.server_message(f'Seu saldo atual é: R$ {self.balance}')
    
    def exit(self):
        return self.server_message(f'Obrigado por usar nosso banco! =)', exit=True)

    def server_message(self, message, error=False, exit=False):
        return self.connection.send(
            json.dumps({'error': error, 'message': message, 'exit': exit}).encode()
        )


Server().run()

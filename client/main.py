from src.auth import Auth
from socket import socket, AF_INET, SOCK_STREAM

class Main:
    def __init__(self, auth, server, port):
        self.auth = auth
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect((server, port))

    def run(self):
        auth_response = self.auth.authenticate(self.connection)
        if auth_response['logged_in'] == True:
            print('Autenticado com sucesso!')
        else:
            print('Autenticação falhou!')

    def close_connection(self):
        return self.connection.close()

main = Main(Auth(), 'localhost', 9093)

while True:
    main.run()

main.close_connection()

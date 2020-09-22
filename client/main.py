from src.auth import Auth
from socket import socket, AF_INET, SOCK_STREAM
import time

class Main:
    def __init__(self, auth, server, port):
        self.auth = auth
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect((server, port))

    def run(self):
        auth_response = self.auth.authenticate(self.connection)

        if auth_response['logged_in'] == True:
            print('Autenticado com sucesso!')
            time.sleep(2)
            self.show_menu()
        else:
            print('Login ou senha incorreta!')

    def close_connection(self):
        return self.connection.close()
    
    def show_menu(self):
        menu = "Menu:\n 1 - Depositar\n 2 - Sacar\n 3 - Saldo\n 4 - Sair\n"

        option = input(menu)
        self.connection.send(option.encode())

main = Main(Auth(), 'localhost', 9093)

while True:
    main.run()

main.close_connection()

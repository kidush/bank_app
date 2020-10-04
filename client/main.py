from src.auth import Auth
from socket import socket, AF_INET, SOCK_STREAM
from os import name as os_name
from subprocess import call 
import time
import json

class Main:
    def __init__(self, auth, server, port):
        self.auth = auth
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect((server, port))
        self.authenticated = False

    def run(self):
        if not self.authenticated:
            auth_response = self.auth.authenticate(self.connection)

            if auth_response['logged_in'] == True:
                print('Autenticado com sucesso!')
                self.authenticated = True
                time.sleep(2)
                self.clear_screen()

                if self.main_menu():
                    return True

                return False
            else:
                print('Login ou senha incorreta!')
        else:
            if self.main_menu():
                return True
            return False


    def close_connection(self):
        return self.connection.close()
    
    def draw_menu(self):
        return "**--------Banco---------**\n\n1 - Depositar\n2 - Sacar\n3 - Saldo\n4 - Sair\nEscolha uma opção: "

    def main_menu(self):
        menu = self.draw_menu()
        option = input(menu)

        if option == '1':
            value_deposit = input('Informe o valor que você quer depositar: ')
            self.connection.send(json.dumps({'option': option, 'value': value_deposit}).encode())

        if option == '2':
            value_withdraw = input('Informe o valor que você quer sacar: ')
            self.connection.send(json.dumps({'option': option, 'value': value_withdraw}).encode())
        
        if option == '3':
            self.connection.send(json.dumps({'option': option, 'value': ''}).encode())

        if option == '4':
            self.connection.send(json.dumps({'option': option, 'value': ''}).encode())
            time.sleep(2)

        option_response = self.connection.recv(1024)
        option_data = json.loads(option_response.decode())


        print()
        print(option_data['message'])
        print()

        if option_data['exit']:
            return False

        print('Voltando ao menu inicial...')

        time.sleep(3)

        self.clear_screen()
        return True

    def clear_screen(self):    
        return call('clear' if os_name == 'posix' else 'cls')

main = Main(Auth(), 'localhost', 9093)

while True:
    if not main.run():
        break


main.close_connection()

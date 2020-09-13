from lib.auth import Auth
# from lib.connection import Connection
from socket import *

HOST = 'localhost'
PORT = 9093

class Main:
    def __init__(self, auth, server, port):
        self._auth = auth
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect((server, port))

    def run(self):
        self._auth.authenticate(self.connection)
    
    def close_connection(self):
        return self.connection.close()
       

main = Main(Auth(), HOST, PORT)

while True:
    main.run()

main.close_connection()
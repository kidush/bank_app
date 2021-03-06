import json

class Auth:
    def __init__(self):
        self._connection = None

    def authenticate(self, connection):
        self.__connection = connection

        user = input('Informe seu usuário: ')
        password = input('Inform sua senha: ')

        self.__connection.send(json.dumps({'user': user, 'password': password}).encode())

        response = self.__connection.recv(1024)

        if response == None:
            return False

        response_data = json.loads(response.decode())

        return response_data





import sqlite3
from entities.user import User

class UserRepository:
    def __init__(self):
        self.database = sqlite3.connect('database/bank.db')
        self.connection = self.database.cursor()
        self.users = []

    def find(self, username, password):
        user = self.connection.execute('''
                    select id, username, password
                    from users
                    where username = ? and password = ?
                ''', (username, password)).fetchone()
        if user is None:
            return None

        return User(id = user[0], username = user[1], password = user[2])

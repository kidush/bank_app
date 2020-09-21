import sqlite3
from entities.user import User

class UserRepository:
    def __init__(self, *args, **kwargs):
        self.database = sqlite3.connect('database/bank.db')
        self.connection = self.database.cursor()

    def all(self):
        self.users = self.connection.execute("select * from users").fetchall()
        return list(map(lambda user: User(id=user[0], username=user[1], password=user[2]), self.users))
    
    def find(self, username, password):
        user = self.connection.execute('''
                    select username, password 
                    from users 
                    where username = ? and password = ?
                ''', (username, password)).fetchone()
        return User(id = user[0], username = user[1], password = user[2])

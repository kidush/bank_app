import sqlite3
import uuid

db = sqlite3.connect('bank.db')
connection = db.cursor()

connection.execute('drop table if exists users')

connection.execute('''
create table users (
    id uuid text primary key not null,
    username char(50),
    password char(20)
)
''')

uuid = uuid.uuid4().hex
connection.execute("insert into users values (?, 'admin', '123123123')", (uuid,))

db.commit()
db.close()
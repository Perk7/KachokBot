import sqlite3
import json
import datetime

class BotDB:
    def __init__(self, dbname="bot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, data TEXT)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_user(self, obj):
        data = {
            'abonement': obj['abonement'],
            'exerc': obj['exerc'],
            }
        
        stmt = "INSERT INTO users (id, data) VALUES (?, ?)"
        args = (obj['id'], json.dumps(data))
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    def is_user(self, id_user):
        stmt = "SELECT id FROM users WHERE id = (?)"
        args = (id_user, )
        return bool(self.conn.execute(stmt, args).fetchall()[0])

    def update_user(self, id_user, obj):
        stmt = "UPDATE users SET data = (?) WHERE id = (?)"
        args = (json.dumps(obj), id_user)
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    def get_user(self, id_user):
        stmt = "SELECT data FROM users WHERE id = (?)"
        args = (id_user, )
        data = self.conn.execute(stmt, args).fetchall()[0][0]
        return json.loads(data)

    def delete_user(self, id_user):
        stmt = "DELETE FROM users WHERE id = (?)"
        args = (id_user, )
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    def delete_all(self):
        stmt = 'DELETE FROM users'
        self.conn.execute(stmt)
        self.conn.commit()

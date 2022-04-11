import json
import datetime
from os import environ as env 

import psycopg2 as ps

class BotDB:
    def __init__(self, dbname=env.get('DB_NAME')):
        self.dbname = dbname
        self.conn = ps.connect(dbname=dbname,
                               user=env.get('DB_USER'), password=env.get("DB_PASSWORD"), host=env.get('DB_HOST'), port='5432')

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, data TEXT)"
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        self.conn.commit()

    def add_user(self, obj):
        data = {
            'abonement': obj['abonement'],
            'exerc': obj['exerc'],
            }
        
        stmt = "INSERT INTO users (id, data) VALUES (%s, %s)"
        args = (obj['id'], json.dumps(data))
        cursor = self.conn.cursor()
        cursor.execute(stmt, args)
        self.conn.commit()
    
    def is_user(self, id_user):
        stmt = "SELECT id FROM users WHERE id = (%s)"
        args = (id_user,)
        cursor = self.conn.cursor()
        cursor.execute(stmt, args)
        
        return bool(cursor.fetchall())

    def update_user(self, id_user, obj):
        stmt = "UPDATE users SET data = (%s) WHERE id = (%s)"
        args = (json.dumps(obj), id_user)
        cursor = self.conn.cursor()
        cursor.execute(stmt, args)
        
        self.conn.commit()
    
    def get_user(self, id_user):
        stmt = "SELECT data FROM users WHERE id = (%s)"
        args = (id_user, )
        cursor = self.conn.cursor()
        cursor.execute(stmt, args)
        
        data = cursor.fetchall()[0][0]
        return json.loads(data)

    def delete_user(self, id_user):
        stmt = "DELETE FROM users WHERE id = (%s)"
        args = (id_user, )
        cursor = self.conn.cursor()
        cursor.execute(stmt, args)
        
        self.conn.commit()
    
    def delete_all(self):
        stmt = 'DELETE FROM users'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        
        self.conn.commit()

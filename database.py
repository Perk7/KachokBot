import json
import datetime
from os import environ as env 

import psycopg2 as ps
from dotenv import load_dotenv

load_dotenv()

class BotDB:
    def __init__(self, dbname=env.get('DB_NAME')):
        self.dbname = dbname
        self.conn = ps.connect('postgres://ddqvznkzwlflhr:6e9103ebf2f22bab0f338abae9f35cfe5e8044a0510599778f1e6dee65c2002b@ec2-52-214-23-110.eu-west-1.compute.amazonaws.com:5432/d7df01fehc2j27')

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

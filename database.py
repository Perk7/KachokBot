import json
import datetime
import psycopg2 as ps

class BotDB:
    def __init__(self, dbname="d3u1kuoi5v2vjf"):
        self.dbname = dbname
        self.conn = ps.connect(dbname=dbname,
                               user='jxjqwavtrskxma', password='7da6c906fd65f5c337e5f88f1168b30a6c9cd1fd04052570486d711febbca39c', host='ec2-52-18-116-67.eu-west-1.compute.amazonaws.com', port='5432')

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
        ]
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

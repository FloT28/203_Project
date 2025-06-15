import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="users",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

#opens cursor to perform database operaitons 
cur = conn.cursor()

#executes command: create new table 
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                'username text NOT NULL,'
                                'email text NOT NULL,'
                                'password text NOT NULL);'
                                )

cur.execute('INSERT INTO users (username, email, password)'
            'VALUES (%s, %s, %s)',
            ('admin',
             'admin@gmail.com',
             'admin')
             )

conn.commit() 

cur.close() 
conn.close() 


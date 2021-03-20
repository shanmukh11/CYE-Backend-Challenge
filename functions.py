import sqlite3

con = sqlite3.connect('email.db')
cur = con.cursor()


cur.execute('''CREATE TABLE stocks
               (date text, trans text, symbol text, qty real, price real)''')
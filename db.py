import sqlite3

con = sqlite3.connect('class-scheduler.db')

cur = con.cursor()

for row in cur.execute('SELECT * FROM instructors'):
    print(row)

con.commit()

con.close()
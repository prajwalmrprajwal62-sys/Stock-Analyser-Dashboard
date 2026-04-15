import sqlite3

conn = sqlite3.connect('database/stocks.db')
cur = conn.cursor()
cur.execute("select date from reliance limit 5")
print('dates:', cur.fetchall())
cur.execute("select strftime('%y-%m', date) from reliance limit 5")
print('strftime:', cur.fetchall())
conn.close()

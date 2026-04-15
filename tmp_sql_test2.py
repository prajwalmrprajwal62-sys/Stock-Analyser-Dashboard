import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
for fmt in ["%Y-%m", "%y-%m", "%m-%d-%Y"]:
    cur.execute(f"select strftime('{fmt}','2022-01-03')")
    print(fmt, cur.fetchone())
conn.close()

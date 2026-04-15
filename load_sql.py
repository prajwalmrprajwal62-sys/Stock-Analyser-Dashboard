import pandas as pd
import sqlite3
import os

os.makedirs("database", exist_ok=True)
conn=sqlite3.connect("database/stocks.db")
print("db connected")

for file in os.listdir('data/'):
    if file.startswith('cleaned_') and file.endswith('.csv'):
        table_name=file.replace('cleaned_', '').replace('.csv', '').lower()

        df=pd.read_csv(f'data/{file}')
        df.to_sql(table_name,conn,if_exists='replace', index=False)

        print(f"Loeded {len(df)} row into table: {table_name}")

tables=pd.read_sql("select name from sqlite_master where type ='table'",conn)        
print(f"\n tables in database:\n{tables}")

sample= pd.read_sql("""
SELECT date, close,daily_return_pct
from reliance
ORDER BY date DESC
LIMIT 5
""",conn)
print(f"latest 5 REL data:\n{sample}")
conn.close()
print("\n Database ready.")


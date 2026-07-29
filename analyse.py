import pandas as pd
import sqlite3
import os

os.makedirs("database", exist_ok=True)
conn=sqlite3.connect("database/stocks.db")
print("db connected")

best_days = pd.read_sql("""
    select
        stock_name,
        date,
        close,
        daily_return_pct
    from reliance
    where daily_return_pct is not null
    order by daily_return_pct desc
    limit 10
""", conn)

print("top 10 days return:\n", best_days)

monthly_avg = pd.read_sql("""
    select
        strftime('%Y-%m', date) as month,
        round(avg(daily_return_pct), 2) as avg_day_price,
        round(avg(close), 3) as avg_close_price,
        count(*) as trading_days
    from reliance
    group by month
    order by month
""", conn)

print("\n monthly avg - RLS:", monthly_avg)

volatility = pd.read_sql("""
    select
        stock_name,
        round(avg(price_range), 2) as avg_day_change,
        round(avg(abs(daily_return_pct)), 3) as avg_abs_return
    from (
        select stock_name, price_range, daily_return_pct from reliance
        union all
        select stock_name, price_range, daily_return_pct from tcs
        union all
        select stock_name, price_range, daily_return_pct from hdfc
        union all
        select stock_name, price_range, daily_return_pct from infosys
    ) all_stocks
    group by stock_name
    order by avg_abs_return desc
""", conn)

print("\n volatility comp :")
print(volatility)

def calculate_cumulative_return(table_name, investment=10000):
    df = pd.read_sql(f"""
        SELECT date, close FROM {table_name} 
        ORDER BY date
    """, conn)
    
    df['date'] = pd.to_datetime(df['date'])
    
    # --- DROP any rows with missing or zero close price ---
    df = df.dropna(subset=['close'])
    df = df[df['close'] > 0]
    
    # --- SIMPLE PRICE RATIO METHOD (more reliable than cumprod) ---
    # If stock was ₹1115 on Day 1 and ₹1255 on last day,
    # ₹10,000 becomes: 10000 * (1255 / 1115) = ₹11,255
    # This is mathematically identical to compounding daily returns
    # but avoids NaN chain corruption
    
    first_price = df['close'].iloc[0]   # price on first trading day
    last_price = df['close'].iloc[-1]   # price on last trading day
    
    final_value = round(investment * (last_price / first_price), 2)
    total_return_pct = round(((final_value - investment) / investment) * 100, 1)
    
    print(f"{table_name.upper()}: ₹{investment:,} → ₹{final_value:,.0f} "
          f"({total_return_pct:+.1f}%)")
    
    # Also return full daily series for charting later
    df['portfolio_value'] = investment * (df['close'] / first_price)
    
    return df

print("\nIF YOU INVESTED ₹10,000 IN JAN 2022:")
reliance_growth = calculate_cumulative_return('reliance')
tcs_growth = calculate_cumulative_return('tcs')
hdfc_growth = calculate_cumulative_return('hdfc')
infosys_growth = calculate_cumulative_return('infosys')
nifty_growth = calculate_cumulative_return('nifty_50')

conn.close()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

conn = sqlite3.connect('database/stocks.db')

# --- CHART STYLE ---
# seaborn sets a global style — makes all matplotlib charts look better
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 7)  # default chart size

# ============================================================
# CHART 1: Price Trends (Line Chart)
# ============================================================
stocks = ['reliance', 'tcs', 'hdfc', 'infosys']
colors = ['#e63946', '#457b9d', '#2a9d8f', '#e9c46a']

fig, ax = plt.subplots()

for stock, color in zip(stocks, colors):
    df = pd.read_sql(f"SELECT date, close FROM {stock} ORDER BY date", conn)
    df['date'] = pd.to_datetime(df['date'])
    ax.plot(df['date'], df['close'], label=stock.upper(), color=color, linewidth=1.5)

ax.set_title('Stock Price Trends 2022–2024', fontsize=16, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Price (INR)')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/01_price_trends.png', dpi=150)
plt.show()
print("Chart 1 saved.")

# ============================================================
# CHART 2: ₹10,000 Growth Comparison (Cumulative Returns)
# ============================================================
fig, ax = plt.subplots()

for stock, color in zip(stocks + ['nifty_50'], colors + ['#6c757d']):
    df = pd.read_sql(f"SELECT date, close FROM {stock} ORDER BY date", conn)
    df['date'] = pd.to_datetime(df['date'])
    df['growth'] = 10000 * (1 + df['close'].pct_change()).cumprod()
    
    linestyle = '--' if stock == 'nifty_50' else '-'
    ax.plot(df['date'], df['growth'], label=stock.upper(),
            color=color, linewidth=1.8, linestyle=linestyle)

ax.axhline(y=10000, color='white', linestyle=':', alpha=0.5)  # breakeven line
ax.set_title('₹10,000 Invested: Who Won? (2022–2024)', fontsize=16, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Portfolio Value (INR)')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/02_growth_comparison.png', dpi=150)
plt.show()

# ============================================================
# CHART 3: Monthly Return Heatmap (seaborn)
# ============================================================
df_r = pd.read_sql("SELECT date, daily_return_pct FROM reliance", conn)
df_r['date'] = pd.to_datetime(df_r['date'])
df_r['month'] = df_r['date'].dt.month_name().str[:3]  # Jan, Feb, Mar...
df_r['year'] = df_r['date'].dt.year

# Pivot: rows=year, columns=month, values=avg return
pivot = df_r.groupby(['year', 'month'])['daily_return_pct'].mean().unstack()

# Reorder months correctly (Jan → Dec)
month_order = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
pivot = pivot.reindex(columns=month_order)

fig, ax = plt.subplots(figsize=(14, 4))
sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, ax=ax, linewidths=0.5)
ax.set_title('Reliance: Average Daily Return % by Month-Year', fontsize=14)
plt.tight_layout()
plt.savefig('outputs/03_monthly_heatmap.png', dpi=150)
plt.show()

conn.close()
print("\nAll charts saved to outputs/ folder.")
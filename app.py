# app.py — Indian Stock Intelligence Dashboard
# Streamlit web app — entry point for deployment

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime

# ============================================================
# PAGE CONFIG — must be the very first Streamlit command
# ============================================================
st.set_page_config(
    page_title="Indian Stock Intelligence Dashboard",
    page_icon="📈",
    layout="wide"
)

# ============================================================
# DATA FETCHING — cached so it only runs ONCE per session
# @st.cache_data tells Streamlit: "if you've already run this
# function with the same inputs, return the saved result
# instead of running it again"
# ============================================================
@st.cache_data
def load_all_stock_data():
    """
    Fetches 3 years of data for 4 Indian stocks + Nifty50.
    Returns a dictionary: {stock_name: DataFrame}
    """
    stocks = {
        'Reliance':  'RELIANCE.NS',
        'TCS':       'TCS.NS',
        'HDFC':      'HDFCBANK.NS',
        'Infosys':   'INFY.NS',
        'Nifty 50':  '^NSEI'
    }

    all_data = {}

    for name, ticker in stocks.items():
        df = yf.download(ticker, start='2022-01-01', end='2024-12-31', progress=False)

        # Flatten multi-level columns yfinance sometimes creates
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Convert the datetime index to a regular date column
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.rename_axis('date').reset_index()
        else:
            df = df.reset_index()

        # Standardize column names
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        # Remove rows where close price is missing or zero
        df = df.dropna(subset=['close'])
        df = df[df['close'] > 0]

        # Add useful calculated columns
        df['daily_return_pct'] = df['close'].pct_change() * 100
        df['price_range'] = df['high'] - df['low']
        df['stock_name'] = name

        all_data[name] = df

    return all_data


def calculate_growth(df, investment=10000):
    """
    Given a stock DataFrame, calculate how much
    an initial investment grows over the full period.
    Uses simple price ratio: end_price / start_price
    """
    first_price = df['close'].iloc[0]
    df['portfolio_value'] = investment * (df['close'] / first_price)
    return df


# ============================================================
# LOAD DATA — shows a spinner while fetching
# ============================================================
with st.spinner('Fetching live market data from Yahoo Finance...'):
    data = load_all_stock_data()

# Apply growth calculation to all stocks
for name in data:
    data[name] = calculate_growth(data[name])

# ============================================================
# SIDEBAR — user controls
# ============================================================
st.sidebar.title("📊 Dashboard Controls")
st.sidebar.markdown("---")

# Stock selector
selected_stocks = st.sidebar.multiselect(
    "Select stocks to display:",
    options=list(data.keys()),
    default=['Reliance', 'TCS', 'HDFC', 'Infosys']
)

# Investment amount input
investment_amount = st.sidebar.number_input(
    "Investment amount (₹):",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=1000
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data source:** Yahoo Finance")
st.sidebar.markdown("**Period:** Jan 2022 – Dec 2024")
st.sidebar.markdown("*For educational purposes only. Not financial advice.*")

# ============================================================
# MAIN HEADER
# ============================================================
st.title("📈 Indian Stock Intelligence Dashboard")
st.markdown("**Analyzing Reliance, TCS, HDFC Bank, Infosys vs Nifty 50 benchmark (2022–2024)**")
st.markdown("---")

# ============================================================
# SECTION 1 — KEY METRICS (top summary cards)
# ============================================================
st.subheader("💰 If You Invested ₹{:,} in January 2022...".format(investment_amount))

# Recalculate with user's investment amount
cols = st.columns(len(selected_stocks) + 1)  # +1 for Nifty

all_display = selected_stocks + (['Nifty 50'] if 'Nifty 50' not in selected_stocks else [])

for i, name in enumerate(all_display):
    if name not in data:
        continue
    df = data[name]
    first_price = df['close'].iloc[0]
    last_price = df['close'].iloc[-1]
    final_val = round(investment_amount * (last_price / first_price), 0)
    return_pct = round(((final_val - investment_amount) / investment_amount) * 100, 1)

    with cols[i]:
        # Color the metric based on positive/negative return
        if return_pct >= 0:
            st.metric(
                label=name,
                value=f"₹{final_val:,.0f}",
                delta=f"+{return_pct}%"
            )
        else:
            st.metric(
                label=name,
                value=f"₹{final_val:,.0f}",
                delta=f"{return_pct}%"
            )

st.markdown("---")

# ============================================================
# SECTION 2 — PRICE TREND CHART
# ============================================================
st.subheader("📉 Stock Price Trends (2022–2024)")

fig1, ax1 = plt.subplots(figsize=(14, 5))
fig1.patch.set_facecolor('#0e1117')   # dark background
ax1.set_facecolor('#0e1117')

colors = ['#e63946', '#457b9d', '#2a9d8f', '#e9c46a', '#a8dadc']

for i, name in enumerate(selected_stocks):
    if name not in data:
        continue
    df = data[name]
    color = colors[i % len(colors)]
    ax1.plot(df['date'], df['close'],
             label=name, color=color, linewidth=1.8)

ax1.set_title('Closing Price Over Time', color='white', fontsize=14, pad=10)
ax1.set_xlabel('Date', color='white')
ax1.set_ylabel('Price (INR)', color='white')
ax1.tick_params(colors='white')
ax1.spines['bottom'].set_color('#333333')
ax1.spines['left'].set_color('#333333')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(facecolor='#1c1c2e', edgecolor='#333333', labelcolor='white')

st.pyplot(fig1)
plt.close(fig1)

st.markdown("---")

# ============================================================
# SECTION 3 — PORTFOLIO GROWTH COMPARISON
# ============================================================
st.subheader(f"📊 ₹{investment_amount:,} Growth Comparison")

fig2, ax2 = plt.subplots(figsize=(14, 5))
fig2.patch.set_facecolor('#0e1117')
ax2.set_facecolor('#0e1117')

display_for_growth = selected_stocks + ['Nifty 50'] if 'Nifty 50' not in selected_stocks else selected_stocks
colors2 = ['#e63946', '#457b9d', '#2a9d8f', '#e9c46a', '#6c757d']

for i, name in enumerate(display_for_growth):
    if name not in data:
        continue
    df = data[name].copy()
    first_price = df['close'].iloc[0]
    df['portfolio_value'] = investment_amount * (df['close'] / first_price)

    linestyle = '--' if name == 'Nifty 50' else '-'
    color = colors2[i % len(colors2)]
    ax2.plot(df['date'], df['portfolio_value'],
             label=name, color=color,
             linewidth=2, linestyle=linestyle)

# Breakeven line
ax2.axhline(y=investment_amount, color='white', linestyle=':', alpha=0.4, linewidth=1)
ax2.text(df['date'].iloc[10], investment_amount * 1.01,
         'Breakeven', color='white', alpha=0.5, fontsize=9)

ax2.set_title(f'Portfolio Value of ₹{investment_amount:,} Over Time',
              color='white', fontsize=14, pad=10)
ax2.set_xlabel('Date', color='white')
ax2.set_ylabel('Portfolio Value (INR)', color='white')
ax2.tick_params(colors='white')
ax2.spines['bottom'].set_color('#333333')
ax2.spines['left'].set_color('#333333')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(facecolor='#1c1c2e', edgecolor='#333333', labelcolor='white')

st.pyplot(fig2)
plt.close(fig2)

st.markdown("---")

# ============================================================
# SECTION 4 — VOLATILITY TABLE
# ============================================================
st.subheader("⚡ Volatility Comparison")
st.markdown("*Higher avg absolute return = stock moves more each day = higher risk/reward*")

volatility_rows = []
for name in selected_stocks:
    if name not in data:
        continue
    df = data[name].dropna(subset=['daily_return_pct'])
    volatility_rows.append({
        'Stock': name,
        'Avg Daily Range (₹)': round(df['price_range'].mean(), 2),
        'Avg Abs Daily Return (%)': round(df['daily_return_pct'].abs().mean(), 3),
        'Max Single Day Gain (%)': round(df['daily_return_pct'].max(), 2),
        'Max Single Day Drop (%)': round(df['daily_return_pct'].min(), 2)
    })

vol_df = pd.DataFrame(volatility_rows).sort_values('Avg Abs Daily Return (%)', ascending=False)
st.dataframe(vol_df, use_container_width=True)

st.markdown("---")

# ============================================================
# SECTION 5 — MONTHLY HEATMAP (Reliance only)
# ============================================================
st.subheader("🗓️ Monthly Return Heatmap — Reliance")
st.markdown("*Best and worst months for Reliance Industries (average daily return %)*")

if 'Reliance' in data:
    df_r = data['Reliance'].dropna(subset=['daily_return_pct']).copy()
    df_r['month'] = df_r['date'].dt.month_name().str[:3]
    df_r['year'] = df_r['date'].dt.year

    pivot = df_r.groupby(['year', 'month'])['daily_return_pct'].mean().unstack()
    month_order = ['Jan','Feb','Mar','Apr','May','Jun',
                   'Jul','Aug','Sep','Oct','Nov','Dec']
    pivot = pivot.reindex(columns=month_order)

    fig3, ax3 = plt.subplots(figsize=(14, 3))
    fig3.patch.set_facecolor('#0e1117')
    ax3.set_facecolor('#0e1117')

    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn',
                center=0, ax=ax3, linewidths=0.5,
                annot_kws={'size': 9})

    ax3.set_title('Avg Daily Return % by Month & Year (Reliance)',
                  color='white', fontsize=13, pad=10)
    ax3.tick_params(colors='white')

    st.pyplot(fig3)
    plt.close(fig3)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    # REPLACE WITH:
"Built by **Prajwal M R** | CSBS, Dr. Ambedkar Institute of Technology | "
    "[GitHub](https://github.com/prajwalmrprajwal62-sys)"
)
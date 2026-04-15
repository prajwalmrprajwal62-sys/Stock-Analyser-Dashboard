import yfinance as yf
import pandas as pd
import os

stocks = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "Nifty_50": "^NSEI"
}

def fetch_stock(name, ticker, start="2022-01-01", end="2025-01-01"):
    print(f"Fetching data for {name} ({ticker})...")

    df = yf.download(ticker, start=start, end=end)

    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Save date index as a real column BEFORE resetting
    df = df.reset_index()  # this moves the date index into a column called 'Date'
    df.rename(columns={'Date': 'date'}, inplace=True)

    df["stock_name"] = name
    df["ticker"] = ticker

    os.makedirs("data", exist_ok=True)
    df.to_csv(f"data/{name.replace(' ', '_')}.csv", index=False)
    print(f"Saved {len(df)} rows for {name} ({ticker})")
    return df
all_data = []
for name, ticker in stocks.items():
    df = fetch_stock(name, ticker)
    all_data.append(df)

print("\nDone check your data/ folder.")


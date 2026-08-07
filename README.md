# 📈 Indian Stock & Mutual Fund Intelligence Dashboard

A end-to-end data pipeline and analytics dashboard built to analyze Indian equity markets using real live data.

> Built by Prajwal M R | CSBS, Dr. Ambedkar Institute of Technology, Bangalore

---

## 🧠 What This Project Does

This project pulls live stock data for major Indian equities, cleans and processes it, stores it in a SQL database, runs analytical queries, and visualizes insights through an interactive dashboard.

It simulates what a junior Data/Analytics Engineer does on day one at a fintech company — fetch → clean → store → query → visualize.

---

## 🏗️ Architecture

```
Yahoo Finance (live data)
        ↓
   yfinance API
        ↓
  pandas (cleaning, feature engineering)
        ↓
  SQLite (local SQL database)
        ↓
  SQL queries (window functions, aggregations, CTEs)
        ↓
  matplotlib + seaborn (charts)
        ↓
  Streamlit (interactive dashboard)
```

---

## 📊 Stocks Tracked

- Reliance Industries (`RELIANCE.NS`)
- TCS (`TCS.NS`)
- HDFC Bank (`HDFCBANK.NS`)
- Infosys (`INFY.NS`)
- Nifty 50 Index (`^NSEI`) — benchmark

---

## 🔍 Key Insights Generated

1. **Price Trend Analysis** — 2-year price history for all 5 instruments
2. **₹10,000 Growth Comparison** — If you invested ₹10K in Jan 2022, where would it be today?
3. **Monthly Return Heatmap** — Best and worst months by average daily return
4. **Volatility Ranking** — Which stock moves the most day-to-day?
5. **Best/Worst Days** — Top 10 biggest single-day gains and drops

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Data Fetching | `yfinance` | Free, no API key, returns structured DataFrames |
| Data Processing | `pandas` | Vectorized operations on 700+ row datasets, C-level speed |
| Storage | `sqlite3` | Serverless SQL database, single-file, no setup required |
| Querying | SQL (via pandas `read_sql`) | Standard analytical queries on structured financial data |
| Visualization | `matplotlib` + `seaborn` | Precise chart control + statistical plot aesthetics |
| Dashboard | `Streamlit` | Fast Python-native web app, no frontend code needed |

---

## 📁 Project Structure

```
finance_dashboard/
│
├── data/                    ← raw and cleaned CSVs
├── database/
│   └── stocks.db            ← SQLite database
├── notebooks/
│   ├── 01_fetch_data.py     ← pulls live data via yfinance
│   ├── 02_clean_data.py     ← pandas cleaning pipeline
│   ├── 03_load_to_sql.py    ← loads DataFrames into SQLite
│   ├── 04_analyze.py        ← SQL queries + pandas analysis
│   └── 05_visualize.py      ← matplotlib + seaborn charts
├── outputs/                 ← saved chart images
├── app.py                   ← Streamlit dashboard (main entry point)
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/prajwalmrprajwal62-sys/Stock-Analyser-Dashboard.git
cd finance-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Fetch fresh data
python notebooks/01_fetch_data.py

# 4. Clean and load into database
python notebooks/02_clean_data.py
python notebooks/03_load_to_sql.py

# 5. Launch the dashboard
streamlit run app.py
```

---

## 📦 Requirements

```
yfinance
pandas
matplotlib
seaborn
streamlit
```

---

## 💡 What I Learned Building This

- How `yfinance` retrieves OHLCV data from Yahoo Finance as a pandas DataFrame
- Why pandas DataFrames outperform Python lists for 700+ row operations (vectorized C-level execution vs Python interpreter loops)
- Why SQLite for local projects vs PostgreSQL for production (serverless single-file vs client-server architecture)
- SQL window functions applied to real financial data (running totals, rankings)
- How to calculate daily returns using `pct_change()` and cumulative growth using `cumprod()`

---

## 🎯 Business Questions This Answers

- "Which Indian large-cap stock gave the best risk-adjusted return in 2022–2024?"
- "Which months historically have the highest/lowest average daily returns?"
- "Which stock is the most volatile — and is that volatility rewarded?"
- "How does each stock perform relative to the Nifty 50 benchmark?"

---

## 🔮 What's Next (Planned)

- [ ] BigQuery integration (replace SQLite for cloud-scale queries)
- [ ] Mutual Fund NAV tracking (AMFI API)
- [ ] Portfolio simulation (enter your own stock weights)
- [ ] Automated daily data refresh

---

*Data source: Yahoo Finance via yfinance. For educational and portfolio purposes only. Not financial advice.*

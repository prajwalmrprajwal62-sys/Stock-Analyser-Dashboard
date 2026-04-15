import pandas as pd
import os   #for data preparation
def clean_stock_data(filepath):
    df = pd.read_csv(filepath)

    # Fix columns
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    print("Columns:", df.columns.tolist())  # verify here

    # Convert types
    df['date'] = pd.to_datetime(df['date'])
    num_cols = ['close', 'high', 'low', 'open', 'volume']
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')

    print(f"Before cleaning: {df.shape}")
    print(df.dtypes)
    print(df.isnull().sum())

    df = df.sort_values('date').reset_index(drop=True)
    df = df.dropna(subset=['close'])

    # Feature engineering
    df['daily_return_pct'] = df['close'].pct_change() * 100
    df['price_range'] = df['high'] - df['low']

    float_cols = ['open', 'high', 'low', 'close', 'daily_return_pct', 'price_range']
    df[float_cols] = df[float_cols].round(2)

    print(f"After cleaning: {df.shape}")
    return df
cleaned={}
for file in os.listdir('data/'):
    if file.endswith('.csv'):
        name=file.replace('.csv', '')
        cleaned[name]=clean_stock_data(f"data/{file}")
        cleaned[name].to_csv(f'data/cleaned_{file}', index=False)

print("\n all files cleaned!")
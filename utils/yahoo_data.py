import yfinance as yf
import pandas as pd
import time

def fetch_stock_data(symbol, period="6y"):
    """
    Fetch historical daily OHLC data for a stock from Yahoo Finance
    period: 6y (6 years)
    """
    try:
        df = yf.download(symbol, period=period, interval="1d", progress=False)
        df.dropna(inplace=True)
        if df.empty:
            return None
        # Drop stock if any day has huge jump (split/bonus)
        df['pct_change'] = df['Close'].pct_change().abs() * 100
        if df['pct_change'].max() > 60:
            return None
        return df
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def fetch_volume_value(df):
    """
    Compute daily volume value = Volume * ((High + Low)/2)
    """
    df['avg_price'] = (df['High'] + df['Low']) / 2
    df['vol_value'] = df['Volume'] * df['avg_price']
    return df

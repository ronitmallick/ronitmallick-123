import pandas as pd

def zigzag(df, threshold=0.05):
    """
    Detect swing highs/lows using threshold (5% default)
    Returns a list of swing points: {'Date', 'Type', 'Price'}
    Type: 'H' = high, 'L' = low
    """
    swings = []
    last_swing = None
    for i in range(1, len(df)):
        price = df['Close'].iloc[i]
        prev_price = df['Close'].iloc[i-1]
        if last_swing is None:
            last_swing = price
            last_type = None
            continue
        change = (price - last_swing) / last_swing
        if change >= threshold:
            swings.append({'Date': df.index[i], 'Type': 'H', 'Price': price})
            last_swing = price
            last_type = 'H'
        elif change <= -threshold:
            swings.append({'Date': df.index[i], 'Type': 'L', 'Price': price})
            last_swing = price
            last_type = 'L'
    return pd.DataFrame(swings)

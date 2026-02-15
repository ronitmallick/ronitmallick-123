import pandas as pd
import numpy as np

def detect_pattern(df, swings):
    """
    Detect your professional pattern:
    1. 32–50% downtrend
    2. >=2 spikes inside downtrend (High >= L*1.3)
    3. 10% uptrend (close)
    4. 40% in 4 days breakout
    Returns list of matches
    """
    matches = []

    swing_prices = swings['Price'].values
    swing_dates = swings['Date'].values
    swing_types = swings['Type'].values

    for i in range(len(swings)-3):
        # Step 1: Downtrend
        if swing_types[i]=='H' and swing_types[i+1]=='L':
            down_high = swing_prices[i]
            down_low = swing_prices[i+1]
            drop_pct = (down_high - down_low)/down_high * 100
            if 32 <= drop_pct <= 60:
                # Step 2: Spikes inside downtrend
                down_region = df.loc[swing_dates[i]:swing_dates[i+1]]
                L = down_region['Close'].min()
                spike_count = (down_region['High'] >= L*1.3).sum()
                if spike_count >= 2:
                    # Step 3: 10% uptrend
                    if i+2 < len(swings) and swing_types[i+2]=='H':
                        up_low = swing_prices[i+1]
                        up_high = swing_prices[i+2]
                        up_pct = (up_high - up_low)/up_low * 100
                        if up_pct >= 10:
                            # Step 4: 40% in 4 days breakout
                            breakout_region = df.loc[swing_dates[i+2]:]
                            closes = breakout_region['Close'].values
                            for j in range(len(closes)-4):
                                if (closes[j+4] - closes[j])/closes[j] >= 0.40:
                                    match = {
                                        'Downtrend %': round(drop_pct,2),
                                        'Spikes': int(spike_count),
                                        'Uptrend 10% Date': swing_dates[i+2],
                                        'Breakout Date': breakout_region.index[j+4]
                                    }
                                    matches.append(match)
                                    break
    return matches

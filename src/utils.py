# brent_analysis/utils.py

import pandas as pd

def load_brent_data(filepath: str) -> pd.DataFrame:
    """
    Load Brent Oil Prices CSV file and parse dates.
    """
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
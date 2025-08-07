# brent_analysis/eda.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.tsa.stattools import adfuller

def plot_price_over_time(df):
    """
    Plot Brent Oil Price over time.
    """
    plt.figure(figsize=(14, 6))
    sns.lineplot(x='Date', y='Price', data=df)
    plt.title("Brent Oil Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.tight_layout()
    plt.show()

def print_summary_stats(df):
    """
    Print summary statistics of the Price column.
    """
    print("Summary Statistics for Brent Oil Price:")
    print(df['Price'].describe())

def calculate_log_returns(df):
    """
    Calculate log returns of the price series.
    """
    df = df.copy()
    df['LogReturn'] = np.log(df['Price']).diff()
    return df.dropna()

def plot_log_returns(df):
    """
    Plot the log returns over time.
    """
    plt.figure(figsize=(14, 6))
    sns.lineplot(x='Date', y='LogReturn', data=df)
    plt.title("Log Returns of Brent Oil Price")
    plt.xlabel("Date")
    plt.ylabel("Log Return")
    plt.tight_layout()
    plt.show()

def test_stationarity(series):
    """
    Perform Augmented Dickey-Fuller test for stationarity.
    """
    result = adfuller(series)
    print(f"ADF Statistic: {result[0]:.4f}")
    print(f"p-value: {result[1]:.4f}")
    for key, value in result[4].items():
        print(f"Critical Value {key}: {value:.4f}")
    if result[1] < 0.05:
        print("=> The series is likely stationary.")
    else:
        print("=> The series is likely non-stationary.")

from flask import Flask, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load data
df_prices = pd.read_csv('../data/processed/log_returns.csv', parse_dates=['Date'])
df_events = pd.read_csv('../data/raw/events.csv', parse_dates=['Date'])
df_changepoints = pd.read_csv('../data/processed/change_points.csv', parse_dates=['change_date'])

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Serve price data with change point flags"""
    prices = df_prices.to_dict('records')
    changepoints = df_changepoints['change_date'].dt.strftime('%Y-%m-%d').tolist()
    
    # Mark change points in the price data
    for price in prices:
        price['is_change_point'] = price['Date'] in changepoints
    
    return jsonify(prices)

@app.route('/api/events', methods=['GET'])
def get_events():
    """Serve event data with proximity to change points"""
    events = []
    for _, row in df_events.iterrows():
        event = row.to_dict()
        # Find nearest change point
        time_deltas = abs(df_changepoints['change_date'] - row['Date'])
        closest_idx = time_deltas.idxmin()
        event.update({
            'nearest_change_point': df_changepoints.iloc[closest_idx]['change_date'].strftime('%Y-%m-%d'),
            'days_difference': time_deltas[closest_idx].days
        })
        events.append(event)
    
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const BrentOilChart = () => {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [pricesRes, eventsRes] = await Promise.all([
          axios.get('http://localhost:5000/api/prices'),
          axios.get('http://localhost:5000/api/events')
        ]);
        setPrices(pricesRes.data);
        setEvents(eventsRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ width: '100%', height: '500px' }}>
      <ResponsiveContainer>
        <LineChart
          data={prices}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="Date" 
            angle={-45} 
            textAnchor="end" 
            height={70}
            tickFormatter={(date) => new Date(date).toLocaleDateString()}
          />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip 
            formatter={(value) => [`$${value.toFixed(2)}`, 'Price']}
            labelFormatter={(date) => `Date: ${new Date(date).toLocaleDateString()}`}
          />
          <Legend />
          {/* Price Line */}
          <Line
            type="monotone"
            dataKey="Price"
            stroke="#8884d8"
            dot={false}
            activeDot={{ r: 6 }}
            name="Brent Oil Price"
          />
          {/* Change Points */}
          {prices
            .filter(item => item.is_change_point)
            .map((item, idx) => (
              <ReferenceLine
                key={`cp-${idx}`}
                x={item.Date}
                stroke="red"
                label={{ 
                  value: 'Change Point', 
                  position: 'top', 
                  fill: 'red' 
                }}
              />
            ))}
          {/* Events */}
          {events.map((event, idx) => (
            <ReferenceLine
              key={`event-${idx}`}
              x={event.Date}
              stroke="green"
              label={{
                value: event.Event,
                position: 'insideBottom',
                angle: -90,
                fill: 'green',
                fontSize: 10
              }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      {/* Event Legend */}
      <div style={{ marginTop: '20px' }}>
        <h4>Key Events:</h4>
        <ul>
          {events.map((event, idx) => (
            <li key={`legend-${idx}`}>
              <strong>{new Date(event.Date).toLocaleDateString()}:</strong> {event.Event} 
              (Nearest CP: {event.nearest_change_point}, Δ={event.days_difference} days)
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default BrentOilChart;
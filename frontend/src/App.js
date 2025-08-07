import React from 'react';
import Chart from './components/Chart';
import EventFilter from './components/EventFilter';
import Loader from './components/Loader';
import './styles/global.css';
import './styles/chartStyles.css';

const App = () => {
  return (
    <div>
      <h1>Brent Change Point Analysis</h1>
      <EventFilter />
      <Chart />
      <Loader />
    </div>
  );
};

export default App;
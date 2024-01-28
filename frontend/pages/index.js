// pages/index.js
import React, { useState } from 'react';
import Topology from '../components/Topology';  // Correct import statement
import GraphTable from '../components/UserTable';
const Home = () => {
  const [selectedOption, setSelectedOption] = useState('');
  const [userCount, setUserCount] = useState('');

  const handleOptionChange = (option) => {
    setSelectedOption(option);
  };

  const handleUserCountChange = (count) => {
    setUserCount(count);
  };

  return (
    <div>
      <h1>Design and Deploy DFL</h1>
      <Topology
        onOptionChange={handleOptionChange}
        onUserCountChange={handleUserCountChange}
      />
      <GraphTable />

    </div>
    
  );
};

export default Home;

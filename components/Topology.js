// components/Dropdown.js
import React, { useState } from 'react';

const Topology = ({ onOptionChange, onUserCountChange }) => {
  const [selectedOption, setSelectedOption] = useState('Option 1');
  const [userCount, setUserCount] = useState('');

  const handleOptionChange = (e) => {
    const option = e.target.value;
    setSelectedOption(option);
    onOptionChange(option);
  };

  const handleUserCountChange = (e) => {
    const count = e.target.value;
    setUserCount(count);
    onUserCountChange(count);
  };

  return (
    <div>
      <label htmlFor="dropdown">Choose an option:</label>
      <select id="dropdown" value={selectedOption} onChange={handleOptionChange} >
        <option value="Line">Line</option>
        <option value="Ring">Ring</option>
        <option value="Star">Star</option>
        <option value="Mesh">Mesh</option>
        <option value="Hybrid">Hybrid</option>
      </select>
      <br />
      <label htmlFor="userCount">Enter the number of users:</label>
      <input
        type="number"
        id="userCount"
        value={userCount}
        onChange={handleUserCountChange}
        style={{ width: '100px' }}
      />
      <p>
        Selected option: {selectedOption}, Number of users: {userCount || 'N/A'}
      </p>
    </div>
  );
};
export default Topology;
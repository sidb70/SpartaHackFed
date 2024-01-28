import React, { useState } from 'react';
import { FaNetworkWired, FaRing, FaStar, FaProjectDiagram, FaLifeRing } from 'react-icons/fa';

const Topology = ({ onOptionChange, onUserCountChange }) => {
  const [selectedOption, setSelectedOption] = useState('Ring');
  const [userCount, setUserCount] = useState('');

  const handleOptionChange = (option) => {
    setSelectedOption(option);
    onOptionChange(option);
  };

  const handleUserCountChange = (e) => {
    const count = e.target.value;
    setUserCount(count);
    onUserCountChange(count);
  };

  const optionStyle = {
    display: 'inline-block',
    width: '100px',
    height: '100px',
    margin: '10px',
    border: '2px solid #ddd',
    borderRadius: '10px',
    textAlign: 'center',
    lineHeight: '100px',
    cursor: 'pointer',
    background: selectedOption === 'Ring' ? '#f0f0f0' : 'transparent',
  };

  const textStyle = {
    color: '#ec5c3d', // Red color for the text
  };

  return (
    <div className='centered'>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
        <div style={{ ...optionStyle, background: selectedOption === 'Ring' ? '#f0f0f0' : 'transparent' }} onClick={() => handleOptionChange('Ring')}>
          <FaRing />
          <span style={textStyle}>  Ring</span> {/* Text description for Ring */}
        </div>
        <div style={{ ...optionStyle, background: selectedOption === 'Star' ? '#f0f0f0' : 'transparent' }} onClick={() => handleOptionChange('Star')}>
          <FaStar />
          <span style={textStyle}>  Star</span> {/* Text description for Star */}
        </div>
        <div style={{ ...optionStyle, background: selectedOption === 'Mesh' ? '#f0f0f0' : 'transparent' }} onClick={() => handleOptionChange('Mesh')}>
          <FaProjectDiagram />
          <span style={textStyle}>  Mesh</span> {/* Text description for Mesh */}
        </div>
        <div style={{ ...optionStyle, background: selectedOption === 'Hybrid' ? '#f0f0f0' : 'transparent' }} onClick={() => handleOptionChange('Hybrid')}>
          <FaLifeRing />
          <span style={textStyle}>  Hybrid</span> {/* Text description for Hybrid */}
        </div>
      </div>
      
      <p>
        Selected topology: {selectedOption}
      </p>
    </div>
  );
};

export default Topology;

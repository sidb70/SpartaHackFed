import React, { useState, useEffect } from 'react';
import axios from 'axios';
import dotenv from 'dotenv'


const UserTable = ({ userCount }) => {
  const [tableData, setTableData] = useState([]);
  const [submissionMessage, setSubmissionMessage] = useState('');


  useEffect(() => {
    // Initialize the tableData when userCount changes
    setTableData(
      Array.from({ length: userCount }, (_, index) => ({
        userNumber: index + 1,
        ip: '',
        port: '',
      }))
    );
  }, [userCount]);

  const handleEdit = (rowIndex, columnName, value) => {
    setTableData((prevData) =>
      prevData.map((row, index) =>
        index === rowIndex ? { ...row, [columnName]: value } : row
      )
    );
  };

  const handleSubmit = async () => {

    const serverUrl = 'http://35.21.184.220:8000/api/network_config';

    console.log('Submitting data:', tableData);
    const userData = tableData.map(({ userNumber, ip, port }) => ({
      userNumber,
      ip,
      port,
    }));

    try {
    
      // Clear the contents of the cells without deleting the rows
      // setTableData((prevData) =>
      //   prevData.map((row) => ({
      //     ...row,
      //     ip: '',
      //     port: '',
      //   }))
      // );
      
      // Make the API request
      const response = await axios.post(serverUrl, userData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('Response from server:', response.data);
    } catch (error) {
      console.error('Error submitting data:', error.message);
    } finally {
      // Set the submission message to indicate the process has been initiated
      setSubmissionMessage('Decentralized learning process has been initiated. P2P network is now established.');

    }
  };

  return (
    <div className='centeredTable'>
      <table>
        <thead>
          <tr>
            <th>User Number</th>
            <th>IP</th>
            <th>Port</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              <td>{row.userNumber}</td>
              <td>
                <input
                  type="text"
                  value={row.ip}
                  onChange={(e) => handleEdit(rowIndex, 'ip', e.target.value)}
                />
              </td>
              <td>
                <input
                  type="text"
                  value={row.port}
                  onChange={(e) => handleEdit(rowIndex, 'port', e.target.value)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {submissionMessage && <p>{submissionMessage}</p>}
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default UserTable;

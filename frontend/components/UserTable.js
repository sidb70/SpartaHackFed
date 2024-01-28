import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserTable = ({ userCount }) => {
  const [tableData, setTableData] = useState([]);
  const [submissionMessage, setSubmissionMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    if (userCount < 0) {
      setErrorMessage('Number of users in network must be positive');
      return;
    }

    if (userCount > 1000) {
      setErrorMessage('Network is too large');
      return;
    }

    setErrorMessage(''); // Clear any existing error messages
    // Initialize the tableData when userCount is valid
    setTableData(
      Array.from({ length: userCount }, (_, index) => ({
        userNumber: index + 1,
        ip: '',
        port: '',
      }))
    );
  }, [userCount]);


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

    my_ip = requests.get('https://ifconfig.me/ip').text.strip()
    const serverUrl = `http://${my_ip}:8000/api/network_config`;

    console.log('Submitting data:', tableData);
    const userData = tableData.map(({ userNumber, ip, port }) => ({
      userNumber,
      ip,
      port,
    }));

    try {
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
    <div className='centered'>
      {errorMessage ? (
        <p style={{ color: 'red' }}>{errorMessage}</p>
      ) : (
        <>
          {/* Render table and other elements only when there is no error */}
      <table className='centeredTable'>
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
      <br />
      <br />
      <br />
      <button onClick={handleSubmit}>Submit</button>
      </>
      )}
    </div>
  );
};

export default UserTable;

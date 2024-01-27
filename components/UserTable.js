// components/UserTable.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const apiUrl = 'http://127.0.0.1:8000/api/network_config';

const UserTable = ({ userCount }) => {
  const [tableData, setTableData] = useState([]);

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
    const userData = tableData.map(({ userNumber, ip, port }) => ({
      userNumber,
      ip,
      port,
    }));
  
    try {
      const response = await axios.post(apiUrl, userData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      console.log('Response from server:', response.data);
    } catch (error) {
      console.error('Error submitting data:', error.message);
    }
  };

  return (
    <div>
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
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default UserTable;

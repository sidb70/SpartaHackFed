// components/UserTable.js
import React, { useState, useEffect } from 'react';

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

  const handleSubmit = () => {
    const userData = tableData.map(({ userNumber, ip, port }) => ({
      userNumber,
      ip,
      port,
    }));

    const jsonData = JSON.stringify(userData);
    console.log(jsonData); // You can store or send this JSON data to an API
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

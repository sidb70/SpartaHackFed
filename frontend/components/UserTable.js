import { useEffect, useState } from 'react';
import axios from 'axios';

function UserTable() {
  const [graphData, setGraphData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);

  const fetchUsers = async () => {
    try {
      const my_ip = '35.23.186.81'; // daniel's ip
      const serverUrl = `http://${my_ip}:8000`;
      const response = await axios.get(`${serverUrl}/api/get_graph`);
      console.log(response.data.Graph); // [{userNumber: 1, ip: "35.21.231.182", port: 8001}]
      setGraphData(response.data.Graph);
      setLoading(false);
    } catch (error) {
      setErrorMessage('An error occurred while fetching user data.');
      setLoading(false);
    }
  };


  useEffect(() => {
    fetchUsers();
  }, []);

  const startTraining = async () => {
    try {

      const my_ip = '35.21.231.182';
      const serverUrl = `http://${my_ip}:8000`;
      const response = await axios.post(`${serverUrl}/api/network_config`);
      console.log(response.data); // [{userNumber: 1, ip: "35.21.231.182", port: 8001}]
      //setGraphData(response.data);
      setLoading(false);
    } catch (error) {
      setErrorMessage('An error occurred while fetching user data.');
      setLoading(false);
    }
  };
  return (
    <div className='centered'>
      {loading ? (
        <p>Loading graph data...</p>
      ) : errorMessage ? (
        <p style={{ color: 'red' }}>{errorMessage}</p>
      ) : graphData.length === 0 ? (
        <p>0 users</p>
      ) : (
        <>
          <table className='centeredTable'>
            <thead>
              <tr>
                <th>User IP</th>
                <th>User Port</th>
              </tr>
            </thead>
            <tbody>
              {graphData.map((user, index) => (
                <tr key={index}>
                  <td>{user.ip}</td>
                  <td>{user.port}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
      <div className="button-container">
        <button onClick={fetchUsers}>Refresh Users</button>
        <button onClick={startTraining}>Start Training</button>
      </div>
    </div>
  );
}

export default UserTable;
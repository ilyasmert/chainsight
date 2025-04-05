import React, { useEffect, useState } from 'react';
import { fetchReady } from '../services/api';

const ReadyTable = () => {
  const [readyData, setReadyData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showTable, setShowTable] = useState(true);

  useEffect(() => {
    const getReadyData = async () => {
      try {
        const data = await fetchReady();
        setReadyData(data);
      } catch (error) {
        console.error('Failed to fetch ready data:', error);
      } finally {
        setLoading(false);
      }
    };

    getReadyData();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2 style={{ cursor: 'pointer' }} onClick={() => setShowTable(!showTable)}>
        Ready Table {showTable ? '▲' : '▼'}
      </h2>

      {showTable && (
        <table border="1" cellPadding="6" style={{ borderCollapse: 'collapse', width: '100%' }}>
          <thead>
            <tr>
              <th>Product ID</th>
              <th>Quantity</th>
              <th>Week</th>
              <th>Year</th>
            </tr>
          </thead>
          <tbody>
            {readyData.map((item, index) => (
              <tr key={index}>
                <td>{item.productid}</td>
                <td>{item.quantity}</td>
                <td>{item.weekid}</td>
                <td>{item.year}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ReadyTable;

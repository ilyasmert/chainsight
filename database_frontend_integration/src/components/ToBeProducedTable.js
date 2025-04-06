import React, { useEffect, useState } from 'react';
import { fetchToBeProduced } from '../services/inventoryApi';

const ToBeProducedTable = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const result = await fetchToBeProduced();
        setData(result);
      } catch (err) {
        console.error('Failed to fetch To Be Produced:', err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <p>Loading To Be Produced...</p>;

  return (
    <div>
      <h2>To Be Produced Table</h2>
      <table border="1" cellPadding="6" style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th>Product ID</th>
            <th>Quantity</th>
            <th>Week ID</th>
            <th>Year</th>

            <th>Estimated Production Date</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, idx) => (
            <tr key={idx}>
              <td>{item.productid}</td>
              <td>{item.quantity}</td>
              <td>{item.weekid}</td>
              <td>{item.year}</td>
              <td>{item.etd}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ToBeProducedTable;

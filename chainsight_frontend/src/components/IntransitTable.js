import React, { useEffect, useState } from 'react';
import { fetchIntransit } from '../services/inventoryApi';

const IntransitTable = () => {
  const [intransitData, setIntransitData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getData = async () => {
      try {
        const data = await fetchIntransit();
        setIntransitData(data);
      } catch (error) {
        console.error('Failed to fetch intransit data:', error);
      } finally {
        setLoading(false);
      }
    };

    getData();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Intransit Table</h2>
      <table border="1" cellPadding="6" style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th>Product ID</th>
            <th>Quantity</th>
            <th>Week</th>
            <th>Year</th>
            <th>ETA</th>
          </tr>
        </thead>
        <tbody>
          {intransitData.map((item, index) => (
            <tr key={index}>
              <td>{item.productid}</td>
              <td>{item.quantity}</td>
              <td>{item.weekid}</td>
              <td>{item.year}</td>
                <td>{item.eta}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default IntransitTable;

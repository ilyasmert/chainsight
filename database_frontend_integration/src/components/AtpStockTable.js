import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AtpStockTable = () => {
  const [atpData, setAtpData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAtpStock = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/inventory/atp-stock/');
        setAtpData(response.data);
      } catch (error) {
        console.error('Failed to fetch ATP stock data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAtpStock();
  }, []);

  if (loading) return <p>Loading ATP Stock...</p>;

  return (
    <div>
      <h2>ATP Stock Table</h2>
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
          {atpData.map((item) => (
            <tr key={`${item.productid}-${item.weekid}-${item.year}`}>
              <td>{item.productid}</td>
              <td>{item.quantity}</td>
              <td>{item.weekid}</td>
              <td>{item.year}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AtpStockTable;

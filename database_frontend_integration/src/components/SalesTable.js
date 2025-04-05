import React, { useEffect, useState } from 'react';
import { fetchSales } from '../services/api';

const SalesTable = () => {
  const [salesData, setSalesData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getSales = async () => {
      try {
        const data = await fetchSales();
        setSalesData(data);
      } catch (err) {
        console.error('Failed to fetch sales:', err);
      } finally {
        setLoading(false);
      }
    };
    getSales();
  }, []);

  if (loading) return <p>Loading sales...</p>;

  return (
    <div>
      <h2>Sales Table</h2>
      <table border="1" cellPadding="6" style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th>Product ID</th>
            <th>Quantity</th>
            <th>Week ID</th>
            <th>Year</th>
          </tr>
        </thead>
        <tbody>
          {salesData.map((item, index) => (
            <tr key={index}>
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

export default SalesTable;

import React, { useEffect, useState } from 'react';
import { fetchAtpStock } from '../services/inventoryApi';
import AtpStockPieChart from './AtpStockPieChart';

const DashboardPage = () => {
  const [atpStockData, setAtpStockData] = useState([]);
  const [loadingAtp, setLoadingAtp] = useState(true);
  const [errorAtp, setErrorAtp] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('userToken');
    const username = localStorage.getItem('username');

    if (token && username) {
      setIsLoggedIn(true);
      setLoadingAtp(false);
      setAtpStockData([]);
      setErrorAtp(null);
    } else {
      setIsLoggedIn(false);

      const loadAtpStock = async () => {
        try {
          setLoadingAtp(true);
          const result = await fetchAtpStock();
          console.log("Fetched ATP Stock Data:", result); // Debug fetched data
          setAtpStockData(result);
          setErrorAtp(null);
        } catch (err) {
          console.error("Error fetching ATP stock data:", err);
          setErrorAtp("Failed to load ATP stock data.");
          setAtpStockData([]);
        } finally {
          setLoadingAtp(false);
        }
      };
      loadAtpStock();
    }
  }, []);

  if (isLoggedIn) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h1>Welcome to chAInSight!</h1>
        <p>Please log in to view the dashboard.</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>chAInSight</h1>
      <p>Welcome to chAInSight! You can display summarized information here.</p>

      <div style={{ marginTop: '30px', marginBottom: '30px', background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
        <h2>ATP Stock Overview</h2>
        {loadingAtp ? (
          <p>Loading ATP stock data...</p>
        ) : errorAtp ? (
          <p style={{ color: 'red' }}>{errorAtp}</p>
        ) : atpStockData.length > 0 ? (
          <AtpStockPieChart data={atpStockData} loading={loadingAtp} error={errorAtp} />
        ) : (
          <p>No ATP stock data to display.</p>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
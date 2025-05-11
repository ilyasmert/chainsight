import React, { useEffect, useState } from 'react';
import { fetchAtpStock } from '../services/inventoryApi'; // Adjust path as needed
import AtpStockPieChart from './AtpStockPieChart'; // Import the new component

const DashboardPage = () => {
  const [atpStockData, setAtpStockData] = useState([]);
  const [loadingAtp, setLoadingAtp] = useState(true);
  const [errorAtp, setErrorAtp] = useState(null);

  useEffect(() => {
    const loadAtpStock = async () => {
      try {
        setLoadingAtp(true);
        const result = await fetchAtpStock();
        setAtpStockData(result);
        setErrorAtp(null);
      } catch (err) {
        console.error("Failed to fetch ATP stock for dashboard:", err);
        setErrorAtp("Failed to load ATP stock data.");
        setAtpStockData([]);
      } finally {
        setLoadingAtp(false);
      }
    };
    loadAtpStock();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>chAInSight</h1>
      <p>Welcome to chAInSight! Charts and summaries will be displayed here.</p>

      <div style={{ marginTop: '30px', marginBottom: '30px', background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
        <h2>ATP Stock Overview</h2>
        <AtpStockPieChart data={atpStockData} loading={loadingAtp} error={errorAtp} />
      </div>

      {/* <div style={{ marginTop: '30px', marginBottom: '30px' }}>
        <h2>Intransit Overview</h2> */}
      {/* <IntransitChartComponent /> */}
      {/* </div> */}

      {/* Add more sections for other charts as needed */}
    </div>
  );
};

export default DashboardPage;
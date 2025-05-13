import React, { useEffect, useState } from 'react';
import { fetchAtpStock, fetchIntransit } from '../services/inventoryApi'; // Import fetchIntransitData
import AtpStockPieChart from './AtpStockPieChart';
import IntransitVolumeChart from './IntransitVolumeChart'; // Import IntransitVolumeChart

const DashboardPage = () => {
  const [atpStockData, setAtpStockData] = useState([]);
  const [loadingAtp, setLoadingAtp] = useState(true);
  const [errorAtp, setErrorAtp] = useState(null);

  const [intransitData, setIntransitData] = useState([]);
  const [loadingIntransit, setLoadingIntransit] = useState(true);
  const [errorIntransit, setErrorIntransit] = useState(null);

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('userToken');
    const username = localStorage.getItem('username');

    if (token && username) {
      setIsLoggedIn(true);
      // If logged in, perhaps clear data or set loading to false if no data is fetched
      setLoadingAtp(false);
      setAtpStockData([]);
      setErrorAtp(null);
      setLoadingIntransit(false);
      setIntransitData([]);
      setErrorIntransit(null);
    } else {
      setIsLoggedIn(false);

      const loadDashboardData = async () => {
        // Load ATP Stock
        try {
          setLoadingAtp(true);
          const atpResult = await fetchAtpStock();
          console.log("Fetched ATP Stock Data:", atpResult);
          setAtpStockData(atpResult);
          setErrorAtp(null);
        } catch (err) {
          console.error("Error fetching ATP stock data:", err);
          setErrorAtp("Failed to load ATP stock data.");
          setAtpStockData([]);
        } finally {
          setLoadingAtp(false);
        }

        // Load Intransit Data
        try {
          setLoadingIntransit(true);
          // Assuming your intransit data items have 'date' and 'volume' fields
          // e.g., { date: '2023-01-15', volume: 100 }
          const intransitResult = await fetchIntransit();
          console.log("Fetched Intransit Data:", intransitResult);
          setIntransitData(intransitResult);
          setErrorIntransit(null);
        } catch (err) {
          console.error("Error fetching intransit data:", err);
          setErrorIntransit("Failed to load intransit data.");
          setIntransitData([]);
        } finally {
          setLoadingIntransit(false);
        }
      };
      loadDashboardData();
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

      <div style={{ display: 'flex', flexDirection: 'row', gap: '20px', marginTop: '30px' }}>
        <div style={{ flex: 1, background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
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

        <div style={{ flex: 1, background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
          {/* Intransit Volume Chart will go here */}
          {/* Title for Intransit chart is inside IntransitVolumeChart component */}
          {loadingIntransit ? (
            <p>Loading intransit data...</p>
          ) : errorIntransit ? (
            <p style={{ color: 'red' }}>{errorIntransit}</p>
          ) : intransitData.length > 0 ? (
            <IntransitVolumeChart data={intransitData} loading={loadingIntransit} error={errorIntransit} />
          ) : (
            <p>No intransit data to display.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
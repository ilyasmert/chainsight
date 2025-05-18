import React, { useEffect, useState, useContext } from 'react';
import { fetchAtpStock, fetchIntransit, fetchToBeProduced } from '../services/inventoryApi';
import AtpStockPieChart from './AtpStockPieChart';
import IntransitVolumeChart from './IntransitVolumeChart';
import ToBeProducedVolumeChart from './ToBeProducedVolumeChart';
import { AuthContext } from './AuthContext';

const DashboardPage = () => {
  const { loggedIn } = useContext(AuthContext);

  const [atpStockData, setAtpStockData] = useState([]);
  const [loadingAtp, setLoadingAtp] = useState(true);
  const [errorAtp, setErrorAtp] = useState(null);

  const [intransitData, setIntransitData] = useState([]);
  const [loadingIntransit, setLoadingIntransit] = useState(true);
  const [errorIntransit, setErrorIntransit] = useState(null);

  const [toBeProducedData, setToBeProducedData] = useState([]);
  const [loadingTbp, setLoadingTbp] = useState(true);
  const [errorTbp, setErrorTbp] = useState(null);

  useEffect(() => {
    if (!loggedIn) return;

    const loadDashboardData = async () => {
      try {
        setLoadingAtp(true);
        const atpResult = await fetchAtpStock();
        setAtpStockData(atpResult);
        setErrorAtp(null);
      } catch (err) {
        setErrorAtp("Failed to load ATP stock data.");
        setAtpStockData([]);
      } finally {
        setLoadingAtp(false);
      }

      try {
        setLoadingIntransit(true);
        const intransitResult = await fetchIntransit();
        setIntransitData(intransitResult);
        setErrorIntransit(null);
      } catch (err) {
        setErrorIntransit("Failed to load intransit data.");
        setIntransitData([]);
      } finally {
        setLoadingIntransit(false);
      }

      try {
        setLoadingTbp(true);
        const tbpResult = await fetchToBeProduced();
        setToBeProducedData(tbpResult);
        setErrorTbp(null);
      } catch (err) {
        setErrorTbp("Failed to load To-Be-Produced data.");
        setToBeProducedData([]);
      } finally {
        setLoadingTbp(false);
      }
    };

    loadDashboardData();
  }, [loggedIn]);

  if (!loggedIn) {
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

      {/* ATP Stock PieChart — Full Width Top */}
      <div style={{ marginBottom: '30px' }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
          <h2 style={{ textAlign: 'center' }}>ATP Stock Overview</h2>
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

      {/* Intransit + To-Be-Produced Charts side-by-side */}
      <div style={{ display: 'flex', flexDirection: 'row', gap: '20px' }}>
        <div style={{ flex: 1 }}>
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

        <div style={{ flex: 1 }}>
          {loadingTbp ? (
            <p>Loading To-Be-Produced data...</p>
          ) : errorTbp ? (
            <p style={{ color: 'red' }}>{errorTbp}</p>
          ) : toBeProducedData.length > 0 ? (
            <ToBeProducedVolumeChart data={toBeProducedData} loading={loadingTbp} error={errorTbp} />
          ) : (
            <p>No To-Be-Produced data to display.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

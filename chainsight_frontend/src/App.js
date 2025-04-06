import React, { useState } from 'react';
import ReadyTable from './components/ReadyTable';
import AtpStockTable from './components/AtpStockTable';
import IntransitTable from './components/IntransitTable';
import SalesTable from './components/SalesTable';
import ToBeProducedTable from './components/ToBeProducedTable';
import UploadPage from './pages/UploadPage';
import UpdatePalletInfo from './components/UpdatePalletInfo'; // (dummy component – we’ll create next)
import UpdateTransportationInfo from './components/UpdateTransportationInfo'; // (dummy component)
import RunOptimization from './components/RunOptimization';

function App() {
  const [activeDropdown, setActiveDropdown] = useState(null);
  const [selectedContent, setSelectedContent] = useState(null);

  const toggleDropdown = (section) => {
    setActiveDropdown((prev) => (prev === section ? null : section));
    setSelectedContent(null); // Reset selected sub-page on dropdown change
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>chAInSight - Inventory Dashboard</h1>

      {/* Inventory Section */}
      <h3 onClick={() => toggleDropdown('inventory')} style={{ cursor: 'pointer' }}>
        Inventory {activeDropdown === 'inventory' ? '▾' : '▸'}
      </h3>
      {activeDropdown === 'inventory' && (
        <div style={{ paddingLeft: '20px' }}>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('ready')}>Ready Table</p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('atp')}>ATP Stock Table</p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('intransit')}>Intransit Table</p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('sales')}>Sales Table</p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('tobe')}>To Be Produced Table</p>
        </div>
      )}

      {/* Upload Section */}
      <h3 onClick={() => toggleDropdown('upload')} style={{ cursor: 'pointer', marginTop: '20px' }}>
        Upload Weekly Files {activeDropdown === 'upload' ? '▾' : '▸'}
      </h3>
      {activeDropdown === 'upload' && (
        <div style={{ paddingLeft: '20px' }}>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('upload_excel')}>
            Upload Excel Files
          </p>
        </div>
      )}

      {/* Update Variables Section */}
      <h3 onClick={() => toggleDropdown('update')} style={{ cursor: 'pointer', marginTop: '20px' }}>
        Update Variables {activeDropdown === 'update' ? '▾' : '▸'}
      </h3>
      {activeDropdown === 'update' && (
        <div style={{ paddingLeft: '20px' }}>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('update_pallet')}>
            Update Pallet Info
          </p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('update_transport')}>
            Update Transportation Info
          </p>
        </div>
      )}
      {/* Run Optimization Section */}
      <h3 onClick={() => toggleDropdown('optimize')} style={{ cursor: 'pointer', marginTop: '20px' }}>
            Run Optimization {activeDropdown === 'optimize' ? '▾' : '▸'}
      </h3>
      {activeDropdown === 'optimize' && (
        <div style={{ paddingLeft: '20px' }}>
            <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedContent('run_optimization')}>
            Start Optimization
            </p>
        </div>
      )}

      {/* Render selected content */}
      <div style={{ marginTop: '30px' }}>
        {selectedContent === 'ready' && <ReadyTable />}
        {selectedContent === 'atp' && <AtpStockTable />}
        {selectedContent === 'intransit' && <IntransitTable />}
        {selectedContent === 'sales' && <SalesTable />}
        {selectedContent === 'tobe' && <ToBeProducedTable />}

        {selectedContent === 'upload_excel' && <UploadPage />}
        {selectedContent === 'update_pallet' && <UpdatePalletInfo />}
        {selectedContent === 'update_transport' && <UpdateTransportationInfo />}

        {selectedContent === 'run_optimization' && <RunOptimization />}
      </div>
    </div>
  );
}

export default App;

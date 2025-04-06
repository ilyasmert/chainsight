import React, { useState } from 'react';
import ReadyTable from './components/ReadyTable';
import AtpStockTable from './components/AtpStockTable';
import IntransitTable from './components/IntransitTable';
import SalesTable from "./components/SalesTable";
import ToBeProducedTable from "./components/ToBeProducedTable";
import UploadPage from './pages/UploadPage'; // ✅ Import your new Upload page

function App() {
  const [selectedTable, setSelectedTable] = useState(null);

  return (
    <div style={{ padding: '20px' }}>
      <h1>chAInSight - Inventory Dashboard</h1>

      {/* Inventory Dropdown */}
      <h3 onClick={() => setSelectedTable(selectedTable === 'inventory' ? null : 'inventory')} style={{ cursor: 'pointer' }}>
        Inventory ▾
      </h3>

      {selectedTable === 'inventory' && (
        <div style={{ paddingLeft: '20px' }}>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedTable('ready')}>Ready Table</p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedTable('atp')}>ATP Stock Table</p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedTable('intransit')}>Intransit Table</p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedTable('sales')}>Sales Table</p>
          <p style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setSelectedTable('tobe')}>To Be Produced Table</p>
        </div>
      )}

      {/* Upload Tab */}
      <h3
        onClick={() => setSelectedTable('upload')}
        style={{ cursor: 'pointer', color: selectedTable === 'upload' ? 'blue' : 'black', marginTop: '20px' }}
      >
        Upload Weekly Files
      </h3>

      {/* Content Rendering */}
      {selectedTable === 'ready' && <ReadyTable />}
      {selectedTable === 'atp' && <AtpStockTable />}
      {selectedTable === 'intransit' && <IntransitTable />}
      {selectedTable === 'sales' && <SalesTable />}
      {selectedTable === 'tobe' && <ToBeProducedTable />}
      {selectedTable === 'upload' && <UploadPage />} {/* ✅ Mount UploadPage */}
    </div>
  );
}

export default App;

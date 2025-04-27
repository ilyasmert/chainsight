import React, { useState } from 'react';
import ReadyTable from '../components/ReadyTable';
import AtpStockTable from '../components/AtpStockTable';
import IntransitTable from '../components/IntransitTable';
import SalesTable from '../components/SalesTable';
import ToBeProducedTable from '../components/ToBeProducedTable';

const TABS = [
  { key: 'ready', label: 'Ready', component: ReadyTable },
  { key: 'atp', label: 'Atp Stock', component: AtpStockTable },
  { key: 'intransit', label: 'Intransit', component: IntransitTable },
  { key: 'sales', label: 'Sales', component: SalesTable },
  { key: 'tobep', label: 'To Be Produced', component: ToBeProducedTable }
];

const InventoryPage = () => {
  const [selectedTab, setSelectedTab] = useState('ready');
  const activeTab = TABS.find(tab => tab.key === selectedTab);
  const ActiveComponent = activeTab.component;

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      {/* Sticky Header: Title + Tabs */}
      <div className="inventory-header-sticky" style={{ top: 0 }}>
        <h2 style={{ fontWeight: 700, marginBottom: 16 }}>Inventory Page</h2>
        <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
          {TABS.map(tab => (
            <button
              key={tab.key}
              onClick={() => setSelectedTab(tab.key)}
              style={{
                padding: '10px 28px',
                background: selectedTab === tab.key ? '#FF715B' : '#3e4451',
                color: '#fff',
                border: 'none',
                borderRadius: 6,
                fontWeight: selectedTab === tab.key ? 600 : 400,
                fontSize: 16,
                cursor: 'pointer',
                transition: 'background 0.2s'
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
        <hr />
      </div>
      {/* Table Area, scrollable if large */}
      <div
        style={{
          margin: '32px 24px',
          background: '#fff',
          border: '1px solid #333',
          borderRadius: 4,
          padding: '24px 28px',
          maxHeight: 500,           // Table container is scrollable!
          overflowY: 'auto'
        }}
      >
        {/* Render table with sticky headers */}
        <div style={{ minWidth: 800 }}>
          {/* Assume all table components use className="sticky-table" on their <table> */}
          <ActiveComponent />
        </div>
      </div>
    </div>
  );
};

export default InventoryPage;


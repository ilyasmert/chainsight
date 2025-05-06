import React, { useState } from 'react';

const ARCHIVE_TABS = [
  { key: 'readyArchive', label: 'Ready Archive' },
  { key: 'atpArchive', label: 'ATP Stock Archive' },
  { key: 'intransitArchive', label: 'Intransit Archive' },
  { key: 'salesArchive', label: 'Sales Archive' },
  { key: 'toBeProducedArchive', label: 'To Be Produced Archive' }
];

const InventoryArchivePage = () => {
  const [selectedTab, setSelectedTab] = useState('readyArchive');

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      {/* Sticky Header: Title + Tabs */}
      <div className="inventory-header-sticky" style={{ top: 0 }}>
        <h2 style={{ fontWeight: 700, marginBottom: 16 }}>Inventory Archive</h2>
        <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
          {ARCHIVE_TABS.map(tab => (
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

      {/* Content Area */}
      <div
        style={{
          margin: '32px 24px',
          background: '#fff',
          border: '1px solid #333',
          borderRadius: 4,
          padding: '24px 28px',
          minHeight: 300,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <div style={{ fontSize: 18, color: '#666', textAlign: 'center' }}>
          Will be implemented on request.
        </div>
      </div>
    </div>
  );
};

export default InventoryArchivePage;

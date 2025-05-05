import React, { useState, useEffect } from 'react';
import {
  fetchReadyArchive,
  fetchAtpStockArchive,
  fetchIntransitArchive,
  fetchSalesArchive,
  fetchToBeProducedArchive
} from "../services/inventoryApi";

const ARCHIVE_TABS = [
  { key: 'readyArchive', label: 'Ready Archive', fetcher: fetchReadyArchive },
  { key: 'atpArchive', label: 'ATP Stock Archive', fetcher: fetchAtpStockArchive },
  { key: 'intransitArchive', label: 'Intransit Archive', fetcher: fetchIntransitArchive },
  { key: 'salesArchive', label: 'Sales Archive', fetcher: fetchSalesArchive },
  { key: 'toBeProducedArchive', label: 'To Be Produced Archive', fetcher: fetchToBeProducedArchive }
];

const InventoryArchivePage = () => {
  const [selectedTab, setSelectedTab] = useState(ARCHIVE_TABS[0].key);
  const [data, setData] = useState([]);
  const [filters, setFilters] = useState({});
  const [quantityFilter, setQuantityFilter] = useState({ operator: '=', value: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async (tabKey) => {
    const tab = ARCHIVE_TABS.find(t => t.key === tabKey);
    if (!tab) return;

    setLoading(true);
    setError(null);
    setFilters({});
    setQuantityFilter({ operator: '=', value: '' });

    try {
      const response = await tab.fetcher();
      setData(response);
    } catch (err) {
      setError('Failed to fetch archive data.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(selectedTab);
  }, [selectedTab]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const filteredData = data.filter(row => {
    return Object.entries(filters).every(([key, value]) => {
      if (!value) return true;
      const cellValue = String(row[key] || '').toLowerCase();
      return cellValue.includes(value.toLowerCase());
    }) && (function() {
      const quantity = parseFloat(row.quantity);
      const filterVal = parseFloat(quantityFilter.value);
      if (!quantityFilter.value || isNaN(filterVal)) return true;
      switch (quantityFilter.operator) {
        case '>': return quantity > filterVal;
        case '<': return quantity < filterVal;
        case '>=': return quantity >= filterVal;
        case '<=': return quantity <= filterVal;
        case '=': return quantity === filterVal;
        default: return true;
      }
    })();
  });

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      <div className="inventory-header-sticky" style={{ top: 0, background: '#fff', zIndex: 10 }}>
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

      <div style={{
        margin: '32px 24px',
        background: '#fff',
        border: '1px solid #333',
        borderRadius: 4,
        padding: '0',
        overflow: 'auto',
        maxHeight: '500px',
        position: 'relative'
      }}>
        {loading ? (
          <div style={{ textAlign: 'center', padding: 24 }}>Loading...</div>
        ) : error ? (
          <div style={{ color: 'red', textAlign: 'center', padding: 24 }}>{error}</div>
        ) : data.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#666', padding: 24 }}>
            No data available for this archive.
          </div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead style={{ position: 'sticky', top: 0, background: '#f9f9f9', zIndex: 5 }}>
              <tr>
                {Object.keys(data[0]).map(key => (
                  <th key={key} style={{ border: '1px solid #ccc', padding: '6px' }}>
                    <div style={{ fontWeight: 'bold' }}>{key}</div>
                    {key.toLowerCase() === 'quantity' ? (
                      <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
                        <select
                          value={quantityFilter.operator}
                          onChange={e => setQuantityFilter(prev => ({ ...prev, operator: e.target.value }))}
                          style={{ padding: '2px', fontSize: 12 }}
                        >
                          <option value="=">=</option>
                          <option value=">">&gt;</option>
                          <option value="<">&lt;</option>
                          <option value=">=">&gt;=</option>
                          <option value="<=">&lt;=</option>
                        </select>
                        <input
                          type="number"
                          value={quantityFilter.value}
                          onChange={e => setQuantityFilter(prev => ({ ...prev, value: e.target.value }))}
                          placeholder="Value"
                          style={{ width: '60px', fontSize: 12, padding: '2px' }}
                        />
                      </div>
                    ) : (
                      <input
                        type="text"
                        value={filters[key] || ''}
                        onChange={e => handleFilterChange(key, e.target.value)}
                        placeholder="Filter..."
                        style={{
                          width: '100%',
                          padding: '4px',
                          border: '1px solid #bbb',
                          borderRadius: 4,
                          fontSize: 12,
                          marginTop: 4
                        }}
                      />
                    )}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filteredData.map((row, idx) => (
                <tr key={idx}>
                  {Object.values(row).map((val, i) => (
                    <td key={i} style={{ border: '1px solid #ccc', padding: '6px' }}>
                      {String(val)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default InventoryArchivePage;

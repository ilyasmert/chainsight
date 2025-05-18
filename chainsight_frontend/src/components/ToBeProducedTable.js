import React, { useEffect, useState } from 'react';
import { fetchToBeProduced } from '../services/inventoryApi';
import ToBeProducedVolumeChart from './ToBeProducedVolumeChart';

const quantityOperators = ["=", ">", "<"];

const ToBeProducedTable = () => {
  const [data, setData] = useState([]);
  const [filters, setFilters] = useState({
    productid: "",
    quantityOperator: "=",
    quantityValue: "",
    weekid: "",
    year: "",
    etd: "",
  });
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('table'); // 'table' | 'chart'
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchToBeProduced()
      .then(result => {
        setData(result);
        setLoading(false);
      })
      .catch(err => {
        setError("Failed to load To-Be-Produced data.");
        setData([]);
        setLoading(false);
      });
  }, []);

  const handleFilterChange = (e, key) => {
    setFilters({ ...filters, [key]: e.target.value });
  };

  const filteredData = data.filter(row =>
    (row.productid || "").toLowerCase().includes((filters.productid || "").toLowerCase()) &&
    (row.weekid?.toString().toLowerCase() || "").includes((filters.weekid || "").toLowerCase()) &&
    (row.year?.toString().toLowerCase() || "").includes((filters.year || "").toLowerCase()) &&
    (row.etd || "").toLowerCase().includes((filters.etd || "").toLowerCase()) &&
    (
      filters.quantityValue === "" ||
      (filters.quantityOperator === "=" && Number(row.quantity) === Number(filters.quantityValue)) ||
      (filters.quantityOperator === ">" && Number(row.quantity) > Number(filters.quantityValue)) ||
      (filters.quantityOperator === "<" && Number(row.quantity) < Number(filters.quantityValue))
    )
  );

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ position: 'relative' }}>
      {/* View Toggle */}
      <div style={{ marginBottom: 16, display: 'flex', gap: '10px' }}>
        <button
          onClick={() => setViewMode('table')}
          style={viewMode === 'table' ? activeButtonStyle : buttonStyle}
        >
          View Table
        </button>
        <button
          onClick={() => setViewMode('chart')}
          style={viewMode === 'chart' ? activeButtonStyle : buttonStyle}
        >
          View Chart
        </button>
      </div>

      {/* TABLE VIEW */}
      {viewMode === 'table' && (
        <>
          {!filteredData.length && <div>No data found for current filters.</div>}
          {filteredData.length > 0 && (
            <div style={{
              maxHeight: 400,
              overflowY: 'auto',
              background: '#fff',
              borderRadius: 8,
              boxShadow: '0 1px 4px #eee'
            }}>
              <table className="sticky-table" style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr>
                    <th>
                      Product ID<br />
                      <input
                        type="text"
                        value={filters.productid}
                        onChange={e => handleFilterChange(e, "productid")}
                        placeholder="Filter Product ID"
                        style={inputStyle}
                      />
                    </th>
                    <th>
                      Quantity<br />
                      <select
                        value={filters.quantityOperator}
                        onChange={e => handleFilterChange(e, "quantityOperator")}
                        style={{ width: 42, marginRight: 4, fontSize: 13, padding: "2px 4px", borderRadius: 4 }}
                      >
                        {quantityOperators.map(op => (
                          <option key={op} value={op}>{op}</option>
                        ))}
                      </select>
                      <input
                        type="number"
                        value={filters.quantityValue}
                        onChange={e => handleFilterChange(e, "quantityValue")}
                        placeholder="Value"
                        style={{ ...inputStyle, width: 60 }}
                      />
                    </th>
                    <th>
                      Week ID<br />
                      <input
                        type="text"
                        value={filters.weekid}
                        onChange={e => handleFilterChange(e, "weekid")}
                        placeholder="Filter Week ID"
                        style={inputStyle}
                      />
                    </th>
                    <th>
                      Year<br />
                      <input
                        type="text"
                        value={filters.year}
                        onChange={e => handleFilterChange(e, "year")}
                        placeholder="Filter Year"
                        style={inputStyle}
                      />
                    </th>
                    <th>
                      ETD<br />
                      <input
                        type="text"
                        value={filters.etd}
                        onChange={e => handleFilterChange(e, "etd")}
                        placeholder="Filter ETD"
                        style={inputStyle}
                      />
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredData.map((row, i) => (
                    <tr key={i} style={{ borderBottom: "1px solid #eee" }}>
                      <td style={cellStyle}>{row.productid}</td>
                      <td style={cellStyle}>{row.quantity}</td>
                      <td style={cellStyle}>{row.weekid}</td>
                      <td style={cellStyle}>{row.year}</td>
                      <td style={cellStyle}>{row.etd}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      {/* CHART VIEW */}
      {viewMode === 'chart' && (
        <div style={{
          width: '100%',
          background: '#fff',
          padding: 20,
          borderRadius: 8,
          boxShadow: '0 1px 4px #eee',
          position: 'relative'
        }}>
          <h3 style={{ textAlign: 'center', marginBottom: 20 }}>Weekly To-Be-Produced Volumes</h3>
          <ToBeProducedVolumeChart data={filteredData} loading={loading} error={error} />
        </div>
      )}
    </div>
  );
};

const inputStyle = {
  marginTop: 4,
  width: "90%",
  fontSize: 13,
  padding: "2px 6px",
  border: "1px solid #ddd",
  borderRadius: 4,
};

const cellStyle = {
  padding: 8,
  background: '#fff'
};

const buttonStyle = {
  padding: '8px 16px',
  fontSize: '14px',
  cursor: 'pointer',
  border: '1px solid #ddd',
  borderRadius: '4px',
  background: '#f9f9f9',
};

const activeButtonStyle = {
  ...buttonStyle,
  background: '#e0e0e0',
  fontWeight: 'bold',
};

export default ToBeProducedTable;

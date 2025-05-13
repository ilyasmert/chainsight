import React, { useEffect, useState } from 'react';
import { fetchAtpStock } from '../services/inventoryApi'; // Adjust as needed
import AtpStockPieChart from './AtpStockPieChart'; // Import the reusable component

const quantityOperators = ["=", ">", "<"];
// COLORS constant is removed as it's in AtpStockPieChart

const AtpStockTable = () => {
  const [data, setData] = useState([]);
  const [filters, setFilters] = useState({
    productid: "",
    quantityOperator: "=",
    quantityValue: "",
    weekid: "",
    year: "",
  });
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('table'); // 'table' or 'chart'

  useEffect(() => {
    setLoading(true);
    fetchAtpStock().then(result => {
      setData(result);
      setLoading(false);
    }).catch(error => {
      console.error("Failed to fetch ATP stock:", error);
      setData([]);
      setLoading(false);
      // Optionally, set an error state here if you want to display it
    });
  }, []);

  const handleFilterChange = (e, key) => {
    setFilters({ ...filters, [key]: e.target.value });
  };

  const filteredData = data.filter(row =>
    (row.productid || "").toLowerCase().includes((filters.productid || "").toLowerCase()) &&
    (row.weekid !== undefined && row.weekid !== null ? row.weekid.toString().toLowerCase() : "").includes((filters.weekid || "").toLowerCase()) &&
    (row.year !== undefined && row.year !== null ? row.year.toString().toLowerCase() : "").includes((filters.year || "").toLowerCase()) &&
    (
      filters.quantityValue === "" ||
      (filters.quantityOperator === "=" && Number(row.quantity) === Number(filters.quantityValue)) ||
      (filters.quantityOperator === ">" && Number(row.quantity) > Number(filters.quantityValue)) ||
      (filters.quantityOperator === "<" && Number(row.quantity) < Number(filters.quantityValue))
    )
  );

  // getPieChartData function is removed as its logic is in AtpStockPieChart

  if (loading && data.length === 0) return <div>Loading...</div>; // Show loading only if data is not yet available

  return (
    <div>
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

      {viewMode === 'table' && (
        <>
          {loading && <p>Loading table data...</p>}
          {!loading && !filteredData.length && <div>No data found for current filters.</div>}
          {!loading && filteredData.length > 0 && (
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
                  </tr>
                </thead>
                <tbody>
                  {filteredData.map((row, i) => (
                    <tr key={i} style={{ borderBottom: "1px solid #eee" }}>
                      <td style={cellStyle}>{row.productid}</td>
                      <td style={cellStyle}>{row.quantity}</td>
                      <td style={cellStyle}>{row.weekid}</td>
                      <td style={cellStyle}>{row.year}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      {viewMode === 'chart' && (
        <div style={{ width: '100%', background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
          <h3 style={{ textAlign: 'center', marginBottom: 20 }}>ATP Stock Overview</h3>
          {/* Use the AtpStockPieChart component */}
          <AtpStockPieChart data={filteredData} loading={loading} error={null} />
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

export default AtpStockTable;
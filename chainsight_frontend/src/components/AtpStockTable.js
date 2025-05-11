import React, { useEffect, useState } from 'react';
import { fetchAtpStock } from '../services/inventoryApi'; // Adjust as needed
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const quantityOperators = ["=", ">", "<"];
const COLORS = ['#FF8042', '#00C49F']; // Colors for pie chart segments (negative, non-negative)

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
    fetchAtpStock().then(result => {
      setData(result);
      setLoading(false);
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

  const getPieChartData = () => {
    if (!filteredData.length) return [];
    const negativeQuantityCount = filteredData.filter(item => Number(item.quantity) < 0).length;
    const nonNegativeQuantityCount = filteredData.length - negativeQuantityCount;

    return [
      { name: 'Quantity < 0', value: negativeQuantityCount },
      { name: 'Quantity >= 0', value: nonNegativeQuantityCount },
    ];
  };

  const pieChartData = getPieChartData();

  if (loading) return <div>Loading...</div>;

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
          {!filteredData.length && !loading && <div>No data found for current filters.</div>}
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
        <>
          {!pieChartData.find(d => d.value > 0) && !loading && <div>No data to display in chart for current filters.</div>}
          {pieChartData.find(d => d.value > 0) && (
            <div style={{ width: '100%', height: 400, background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
              <h3 style={{ textAlign: 'center', marginBottom: 20 }}>Product Quantity Distribution</h3>
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={pieChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={120}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value, name) => [`${value} products`, name]} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
                <div style={{ marginTop: 20, textAlign: 'center', fontSize: 14 }}>
                  <p><strong># of Products {'<'} 0:</strong> {pieChartData[0]?.value || 0}</p>
                  <p><strong># of Products {'>='} 0:</strong> {pieChartData[1]?.value || 0}</p>
                  <p><strong>Total Products:</strong> {filteredData.length}</p>
                </div>
            </div>
          )}
        </>
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
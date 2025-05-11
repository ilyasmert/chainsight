import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#FF8042', '#00C49F']; // Colors for pie chart segments (negative, non-negative)

const AtpStockPieChart = ({ data, loading, error }) => {
  const getPieChartData = () => {
    if (!data || data.length === 0) return [];
    const negativeQuantityCount = data.filter(item => Number(item.quantity) < 0).length;
    const nonNegativeQuantityCount = data.length - negativeQuantityCount;

    return [
      { name: 'Quantity < 0', value: negativeQuantityCount },
      { name: 'Quantity >= 0', value: nonNegativeQuantityCount },
    ];
  };

  const pieData = getPieChartData();
  const totalProducts = data ? data.length : 0;

  if (loading) return <p>Loading chart data...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!data || data.length === 0) return <p>No data available for chart.</p>;
  // Check if there's any data to display in the pie chart itself
  if (!pieData.find(d => d.value > 0)) return <p>No data to display in chart for current selection.</p>;


  return (
    <>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={pieData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent, value }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {pieData.map((entry, index) => (
              <Cell key={`cell-atp-pie-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value, name) => [`${value} products`, name]} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ marginTop: 10, textAlign: 'center', fontSize: 14 }}>
        <p><strong># of Products {'<'} 0:</strong> {pieData[0]?.value || 0}</p>
        <p><strong># of Products {'>='} 0:</strong> {pieData[1]?.value || 0}</p>
        <p><strong>Total Products:</strong> {totalProducts}</p>
      </div>
    </>
  );
};

export default AtpStockPieChart;
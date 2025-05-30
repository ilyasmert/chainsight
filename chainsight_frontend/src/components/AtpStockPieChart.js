import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const COLORS = ['#228B22', '#4F4F4F', '#FF0000']; // green, gray, red

const AtpStockPieChart = ({ data, loading, error }) => {
  const getPieChartData = () => {
    if (!data || data.length === 0) return [];

    const negativeQuantityCount = data.filter(item => Number(item.quantity) < 0).length;
    const zeroQuantityCount = data.filter(item => Number(item.quantity) === 0).length;
    const positiveQuantityCount = data.filter(item => Number(item.quantity) > 0).length;

    return [
      { name: 'Positive Stock', value: positiveQuantityCount },
      { name: 'Zero Stock', value: zeroQuantityCount },
      { name: 'Negative Stock', value: negativeQuantityCount }
    ];
  };

  const pieData = getPieChartData();
  const totalProducts = data ? data.length : 0;
  const week = data && data.length > 0 ? data[0].weekid : 'N/A';
  const year = data && data.length > 0 ? data[0].year : 'N/A';

  if (loading) return <p>Loading chart data...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!data || data.length === 0) return <p>No data available for chart.</p>;
  if (!pieData.find(d => d.value > 0)) return <p>No data to display in chart for current selection.</p>;

  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={pieData}
            cx="50%"
            cy="50%"
            outerRadius={120} // Reduced outerRadius
            labelLine={true}
            label={({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
              const RADIAN = Math.PI / 180;
              const radius = outerRadius + 30;
              const x = cx + radius * Math.cos(-midAngle * RADIAN);
              const y = cy + radius * Math.sin(-midAngle * RADIAN);
              const color = COLORS[index % COLORS.length];
              const { name, value } = pieData[index];
              const displayPercent = `${(percent * 100).toFixed(0)}%`;

              return (
                <text
                  x={x}
                  y={y}
                  fill={color}
                  textAnchor={x > cx ? 'start' : 'end'}
                  dominantBaseline="central"
                  fontSize={14}
                >
                  {`${name}: ${value} (${displayPercent})`}
                </text>
              );
            }}
            dataKey="value"
          >
            {pieData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value, name) => [`${value} products`, name]} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>

      <div style={{ marginTop: 10, textAlign: 'left', fontSize: 14 }}>
        <p><strong>Total Products:</strong> {totalProducts}</p>
        <p><strong>Week:</strong> {week}, <strong>Year:</strong> {year}</p>
      </div>
    </div>
  );
};

export default AtpStockPieChart;
import React, { useMemo, useEffect } from 'react';
import {
  parseISO,
  format,
  startOfWeek,
  endOfWeek,
} from 'date-fns';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const processDataForChart = (toBeProducedData) => {
  if (!toBeProducedData || toBeProducedData.length === 0) return [];

  const weeklyVolumes = {};

  toBeProducedData.forEach(item => {
    try {
      const date = parseISO(item.etd);
      const monday = startOfWeek(date, { weekStartsOn: 1 });
      const sunday = endOfWeek(date, { weekStartsOn: 1 });

      const weekLabel = `${format(monday, 'dd-MM')} to ${format(sunday, 'dd-MM')}`;
      const startDate = monday.toISOString();
      const volume = Number(item.quantity);

      if (!isNaN(volume)) {
        if (weeklyVolumes[weekLabel]) {
          weeklyVolumes[weekLabel].totalVolume += volume;
        } else {
          weeklyVolumes[weekLabel] = {
            week: weekLabel,
            totalVolume: volume,
            startDate,
          };
        }
      }
    } catch (e) {
      console.error("Error processing item:", item, e);
    }
  });

  return Object.values(weeklyVolumes).sort(
    (a, b) => new Date(a.startDate) - new Date(b.startDate)
  );
};

const ToBeProducedVolumeChart = ({ data, loading, error }) => {
  const chartData = useMemo(() => processDataForChart(data), [data]);

  const totalVolume = useMemo(() => {
    if (!data || data.length === 0) return 0;
    return Math.round(data.reduce((sum, item) => sum + Number(item.quantity || 0), 0));
  }, [data]);

  const latestWeek = data?.[0]?.weekid || '-';
  const latestYear = data?.[0]?.year || '-';

  useEffect(() => {
    console.log('Raw To-Be-Produced data:', data);
  }, [data]);

  if (loading) return <p>Loading chart data...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!data || data.length === 0) return <p>No To-Be-Produced data available.</p>;
  if (chartData.length === 0 || chartData.every(item => item.totalVolume === 0))
    return <p>No meaningful data to display.</p>;

  return (
    <div style={{ width: '100%', background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
      <h2 style={{ textAlign: 'center', marginBottom: 20 }}>Weekly To-Be-Produced Volumes</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 80, bottom: 90 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="week"
            angle={-45}
            textAnchor="end"
            interval={0}
            tick={{ fontSize: 10 }}
          />
          <YAxis
            width={40}
            tick={{ dx: -10, fontSize: 12 }}
            tickFormatter={(value) => Math.round(value)}
            label={{
              value: '',
              angle: -90,
              position: 'outsideLeft',
              offset: 10,
              dy: -10,
            }}
          />
          <Tooltip formatter={(value) => [`${Math.round(value)} m²`, "Total Volume"]} />
          <Legend verticalAlign="top" height={36} />
          <Bar dataKey="totalVolume" fill="#82ca9d" name="Total Volume (m²)" />
        </BarChart>
      </ResponsiveContainer>

      <div style={{ textAlign: 'left', marginTop: 10 }}>
        <p style={{ margin: 0, fontSize: 14 }}>
          <strong>Total Volume:</strong> {totalVolume} m²
        </p>
        <p style={{ margin: 0, fontSize: 14 }}>
          <strong>Week:</strong> {latestWeek}, <strong>Year:</strong> {latestYear}
        </p>
      </div>
    </div>
  );
};

export default ToBeProducedVolumeChart;

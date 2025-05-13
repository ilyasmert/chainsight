import React, { useMemo, useEffect } from 'react'; // ✅ Add useEffect here
import { parseISO, format, startOfWeek, endOfWeek , getISOWeek} from 'date-fns';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// ✅ Refactored to properly define and log 'result'
const processDataForChart = (intransitData) => {
  if (!intransitData || intransitData.length === 0) return [];

  const weeklyVolumes = {};

  intransitData.forEach(item => {
    try {
      const date = parseISO(item.eta);
      const monday = startOfWeek(date, { weekStartsOn: 1 });
      const sunday = endOfWeek(date, { weekStartsOn: 1 });

      const weekLabel = `${format(monday, 'MM-dd')} to ${format(sunday, 'MM-dd')}`;
      const startDate = monday.toISOString(); // For real sorting
      const volume = Number(item.quantity);

      if (!isNaN(volume)) {
        if (weeklyVolumes[weekLabel]) {
          weeklyVolumes[weekLabel].totalVolume += volume;
        } else {
          weeklyVolumes[weekLabel] = {
            week: weekLabel,
            totalVolume: volume,
            startDate: startDate
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

const IntransitVolumeChart = ({ data, loading, error }) => {
  const chartData = useMemo(() => processDataForChart(data), [data]);

  const totalVolume = useMemo(() => {
    if (!data || data.length === 0) return 0;
    return data.reduce((sum, item) => sum + Number(item.quantity || 0), 0);
  }, [data]);

  const latestWeek = data?.[0]?.weekid || '-';
  const latestYear = data?.[0]?.year || '-';

  useEffect(() => {
    console.log('Raw intransit data received by chart:', data);
  }, [data]);

  if (loading) return <p>Loading chart data...</p>;
  if (error) return <p style={{ color: 'red' }}>{error || 'Error loading chart data.'}</p>;
  if (!data || data.length === 0) return <p>No intransit data available.</p>;
  if (chartData.length === 0 || chartData.every(item => item.totalVolume === 0))
    return <p>No meaningful data to display for current selection.</p>;

  return (
    <div style={{ width: '100%', background: '#fff', padding: 20, borderRadius: 8, boxShadow: '0 1px 4px #eee' }}>
      <h2 style={{ textAlign: 'center', marginBottom: 20 }}>Weekly Intransit Volumes</h2>
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
            label={{
              value: '',
              angle: -90,
              position: 'outsideLeft',
              offset: 10,
              dy: -10,
            }}
            tick={{ dx: -10, fontSize: 12 }}
          />
          <Tooltip formatter={(value) => [`${value} m²`, "Total Volume"]} />
          <Legend verticalAlign="top" height={36} />
          <Bar dataKey="totalVolume" fill="#8884d8" name="Total Volume (m²)" />
        </BarChart>
      </ResponsiveContainer>

      {/* 👇 Summary below chart */}
      <div style={{ textAlign: 'left', marginTop: 10 }}>
        <p style={{ margin: 0,fontSize: 14 }}>
          <strong>Total Volume:</strong> {Math.round(totalVolume).toLocaleString()} m²
        </p>
        <p> </p>
        <p style={{  margin: 0,fontSize: 14 }}>
           <strong>Week:</strong> {latestWeek},<strong>Year:</strong> {latestYear}
        </p>
      </div>

    </div>
  );
};

export default IntransitVolumeChart;

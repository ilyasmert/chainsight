import React, { useMemo, useEffect, useState, useRef } from 'react';
import {
  parseISO,
  format,
  startOfWeek,
  endOfWeek
} from 'date-fns';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const processDataForChart = (intransitData) => {
  if (!intransitData || intransitData.length === 0) return [];

  const weeklyVolumes = {};

  intransitData.forEach(item => {
    try {
      const date = parseISO(item.eta);
      const monday = startOfWeek(date, { weekStartsOn: 1 });
      const sunday = endOfWeek(date, { weekStartsOn: 1 });

      const weekLabel = `${format(monday, 'dd-MM')} to ${format(sunday, 'dd-MM')}`;
      const startDate = monday.toISOString();
      const volume = Number(item.quantity);

      if (!isNaN(volume)) {
        if (weeklyVolumes[weekLabel]) {
          weeklyVolumes[weekLabel].totalVolume += volume;
          weeklyVolumes[weekLabel].rawItems.push(item);
        } else {
          weeklyVolumes[weekLabel] = {
            week: weekLabel,
            totalVolume: volume,
            startDate,
            rawItems: [item]
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
    return Math.round(data.reduce((sum, item) => sum + Number(item.quantity || 0), 0));
  }, [data]);

  const latestWeek = data?.[0]?.weekid || '-';
  const latestYear = data?.[0]?.year || '-';

  const [selectedWeekData, setSelectedWeekData] = useState(null);
  const [selectedWeekLabel, setSelectedWeekLabel] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const modalRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        setModalVisible(false);
      }
    };

    if (modalVisible) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [modalVisible]);

  if (loading) return <p>Loading chart data...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!data || data.length === 0) return <p>No intransit data available.</p>;
  if (chartData.length === 0 || chartData.every(item => item.totalVolume === 0))
    return <p>No meaningful data to display for current selection.</p>;

  return (
    <div style={{ position: 'relative', zIndex: 1 }}>
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
            tick={{ dx: -10, fontSize: 12 }}
            tickFormatter={(value) => Math.round(value)}
            label={{ value: '', angle: -90, position: 'outsideLeft', offset: 10, dy: -10 }}
          />
          <Tooltip formatter={(value) => [`${Math.round(value)} m²`, "Total Volume"]} />
          <Legend verticalAlign="top" height={36} />
          <Bar
            dataKey="totalVolume"
            fill="#8884d8"
            name="Total Volume (m²)"
            onClick={(data, index) => {
              const clicked = chartData[index];
              setSelectedWeekData(clicked.rawItems);
              setSelectedWeekLabel(clicked.week);
              setModalVisible(true);
            }}
          />
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

      {/* Modal + background overlay */}
      {modalVisible && (
        <>
          {/* Dark overlay */}
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.4)',
            zIndex: 9998
          }} />

          {/* Modal */}
          <div
            ref={modalRef}
            style={{
              position: 'absolute',
              top: '20%',
              left: '50%',
              transform: 'translate(-50%, -20%)',
              background: '#fff',
              border: '1px solid #ccc',
              borderRadius: 8,
              padding: 20,
              boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
              zIndex: 9999,
              maxHeight: 400,
              overflowY: 'auto',
              minWidth: 320
            }}
          >
            <h3>Products intransit for: <span style={{ color: '#555' }}>{selectedWeekLabel}</span></h3>
            <ul>
              {selectedWeekData?.map((item, idx) => (
                <li key={idx}>
                  {item.productname || item.productid}: {Math.round(item.quantity)} m²
                </li>
              ))}
            </ul>
            <button onClick={() => setModalVisible(false)}>Close</button>
          </div>
        </>
      )}
    </div>
  );
};

export default IntransitVolumeChart;

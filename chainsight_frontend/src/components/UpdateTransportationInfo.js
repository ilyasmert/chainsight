// src/components/UpdateTransportationInfo.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const capacityOptions = ['m2', 'kg'];
const costOptions = ['days', 'weeks'];
const API_BASE_URL = 'http://localhost:8000';

const UpdateTransportationInfo = () => {
  const [rows, setRows] = useState([]);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setError('');
    axios.get(`${API_BASE_URL}/api/inventory/transportation/`)
      .then(res => {
        setRows(res.data || []);
      })
      .catch(err => {
        console.error('Fetch error:', err);
        setError(`Failed to fetch transportation data: ${err.response?.status} ${err.response?.statusText}`);
      });
  }, []);

  const handleInputChange = (index, field, value) => {
    const updated = [...rows];
    updated[index][field] = value;
    setRows(updated);
    setSaved(false);
    setError('');
  };

  const handleSave = async () => {
    setError('');
    setSaved(false);
    try {
      const payload = rows.map(row => ({
        ...row,
        transportationcapacity: Number(row.transportationcapacity),
        transportationcost: Number(row.transportationcost),
        year: Number(row.year),
      }));

      await axios.post(`${API_BASE_URL}/api/inventory/transportation/archive/`);
      await axios.put(`${API_BASE_URL}/api/inventory/transportation/update/`, payload);
      setSaved(true);
    } catch (error) {
      console.error("Update failed:", error);
      setError(`Update failed: ${error.response?.status} ${error.response?.statusText}`);
    }
  };

  return (
    <div className="p-4 bg-white rounded shadow-md">
      <h2 className="text-xl font-semibold mb-6">🚚 Update Transportation Info</h2>
      {error && <p className="text-red-600 mb-4 font-semibold">❌ {error}</p>}

      <table className="w-full text-base border border-gray-300 table-fixed">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-3 text-left">Name</th> {/* Ensured text-left */}
            <th className="border p-3 text-left">Capacity</th> {/* Ensured text-left */}
            <th className="border p-3 text-left">Capacity Unit</th> {/* Ensured text-left */}
            <th className="border p-3 text-left w-28">Cost</th> {/* Ensured text-left */}
            <th className="border p-3 text-left">Cost Unit</th> {/* Ensured text-left */}
            <th className="border p-3 text-left">Year</th> {/* Ensured text-left */}
          </tr>
        </thead>
        <tbody>
          {rows.length > 0 ? rows.map((row, i) => (
            <tr key={row.transportationid || i} style={{ height: '32px' }}>
              <td className="border p-3">{row.transportationname}</td>
              <td className="border p-3">
                <input
                  type="number"
                  value={row.transportationcapacity || ''}
                  onChange={e => handleInputChange(i, 'transportationcapacity', e.target.value)}
                  className="w-28 px-3 py-2 border rounded"
                />
              </td>
              <td className="border p-3">
                <select
                  value={row.capacityunit || ''}
                  onChange={e => handleInputChange(i, 'capacityunit', e.target.value)}
                  className="w-24 px-2 py-2 border rounded"
                >
                  {capacityOptions.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </td>
              <td className="border p-3">
                <input
                  type="number"
                  value={row.transportationcost || ''}
                  onChange={e => handleInputChange(i, 'transportationcost', e.target.value)}
                  className="w-16 px-2 py-2 border rounded"
                />
              </td>
              <td className="border p-3">
                <select
                  value={row.costunit || ''}
                  onChange={e => handleInputChange(i, 'costunit', e.target.value)}
                  className="w-24 px-2 py-2 border rounded"
                >
                  {costOptions.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </td>
              <td className="border p-3">
                <input
                  type="number"
                  value={row.year || ''}
                  onChange={e => handleInputChange(i, 'year', e.target.value)}
                  className="w-20 px-3 py-2 border rounded"
                />
              </td>
            </tr>
          )) : (
            <tr>
              <td colSpan="6" className="text-center p-6 text-gray-500">
                No transportation data found or still loading.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <button
        onClick={handleSave}
        disabled={rows.length === 0}
        className="mt-10 bg-green-500 hover:bg-green-600 text-white text-xl font-bold py-4 px-12 rounded disabled:bg-gray-400" /* Increased text-xl, py-4, px-12 */
      >
        SAVE
      </button>

      {saved && (
        <p className="text-green-600 mt-4 font-semibold text-base">
          ✅ Transportation info saved successfully.
        </p>
      )}
    </div>
  );
};

export default UpdateTransportationInfo;
import React, { useState } from 'react';
import axios from 'axios';

const truckSVG = (
  <svg height="24" viewBox="0 0 24 24" style={{ marginRight: 8 }}>
    <rect x="2" y="9" width="13" height="6" fill="#aaa" />
    <rect x="15" y="11" width="5" height="4" fill="#d63" />
    <circle cx="6" cy="17" r="2" fill="#333" />
    <circle cx="17" cy="17" r="2" fill="#333" />
  </svg>
);
const containerSVG = (
  <svg height="24" viewBox="0 0 24 24" style={{ marginRight: 8 }}>
    <rect x="4" y="10" width="16" height="6" fill="#1996f3" />
    <rect x="2" y="11" width="2" height="4" fill="#888" />
    <rect x="20" y="11" width="2" height="4" fill="#888" />
  </svg>
);

const defaultRows = [
  { type: "Truck", icon: truckSVG, capacity: "400", transit: "3 days" },
  { type: "Container", icon: containerSVG, capacity: "2000", transit: "8 days" },
];

const UpdateVariablesPage = () => {
  const [activeTab, setActiveTab] = useState("pallet");
  const [rows, setRows] = useState(defaultRows);
  const [saved, setSaved] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleInputChange = (index, field, value) => {
    const updated = [...rows];
    updated[index][field] = value;
    setRows(updated);
    setSaved(false);
  };

  const handleSave = () => {
    setSaved(true);
    console.log("Saved transportation info:", rows);
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/api/update_pallet_info/', formData);
      setUploadStatus("✅ Upload successful!");
    } catch (error) {
      setUploadStatus("❌ Upload failed!");
    }
  };

  return (
    <div style={{ padding: 24 }}>
      {/* Tabs */}
      <div style={{ display: "flex", gap: 16, marginBottom: 16 }}>
        <button
          onClick={() => setActiveTab("pallet")}
          style={{
            background: activeTab === "pallet" ? "#ff715b" : "#444",
            color: "#fff",
            border: "none",
            borderRadius: 5,
            fontSize: 15,
            padding: "10px 34px",
            cursor: "pointer",
            fontWeight: 500
          }}
        >Pallet Info</button>
        <button
          onClick={() => setActiveTab("transportation")}
          style={{
            background: activeTab === "transportation" ? "#ff715b" : "#444",
            color: "#fff",
            border: "none",
            borderRadius: 5,
            fontSize: 15,
            padding: "10px 34px",
            cursor: "pointer",
            fontWeight: 500
          }}
        >Transportation Info</button>
      </div>

      {/* Pallet Info Content */}
      {activeTab === "pallet" && (
        <div style={{ marginTop: 32 }}>
          <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Upload Pallet Info File (.xlsx)</h3>
          <input
            type="file"
            accept=".xlsx"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ marginBottom: 12 }}
          />
          <br />
          <button
            onClick={handleFileUpload}
            style={{
              background: "#1996f3",
              color: "#fff",
              border: "none",
              borderRadius: 5,
              fontSize: 15,
              padding: "8px 24px",
              cursor: "pointer",
              fontWeight: 500,
            }}
          >
            Upload File
          </button>
          <div style={{ marginTop: 12, color: uploadStatus.startsWith("✅") ? "green" : "red" }}>
            {uploadStatus}
          </div>
        </div>
      )}

      {/* Transportation Info Content */}
      {activeTab === "transportation" && (
        <div style={{ maxWidth: 460, marginTop: 16, marginLeft: 4 }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#fafafa" }}>
                <th style={{ border: "1px solid #bbb", padding: 10, fontSize: 15, fontWeight: 600 }}>Type</th>
                <th style={{ border: "1px solid #bbb", padding: 10, fontSize: 15, fontWeight: 600 }}>Capacity per week</th>
                <th style={{ border: "1px solid #bbb", padding: 10, fontSize: 15, fontWeight: 600 }}>Transit time</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, i) => (
                <tr key={i}>
                  <td style={{ border: "1px solid #bbb", padding: 10, display: "flex", alignItems: "center", fontSize: 15 }}>
                    {row.icon}{row.type}
                  </td>
                  <td style={{ border: "1px solid #bbb", padding: 10, fontSize: 15 }}>
                    <input
                      type="text"
                      value={row.capacity}
                      style={{
                        width: 80,
                        padding: "6px",
                        fontSize: 15,
                        border: "1px solid #ccc",
                        borderRadius: 4
                      }}
                      onChange={e => handleInputChange(i, "capacity", e.target.value)}
                    />
                  </td>
                  <td style={{ border: "1px solid #bbb", padding: 10, fontSize: 15 }}>
                    <input
                      type="text"
                      value={row.transit}
                      style={{
                        width: 80,
                        padding: "6px",
                        fontSize: 15,
                        border: "1px solid #ccc",
                        borderRadius: 4
                      }}
                      onChange={e => handleInputChange(i, "transit", e.target.value)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <button
            onClick={handleSave}
            style={{
              background: "#26B35B",
              color: "#fff",
              border: "none",
              borderRadius: 5,
              fontSize: 15,
              padding: "8px 28px",
              marginTop: 16,
              marginBottom: 8,
              cursor: "pointer",
              fontWeight: 500,
            }}
          >
            Save
          </button>
          {saved && (
            <div style={{ color: "#26B35B", marginTop: 6, fontWeight: 500 }}>
              Transportation info saved!
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default UpdateVariablesPage;

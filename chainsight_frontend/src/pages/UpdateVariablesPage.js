import React, { useState } from 'react';
import axios from 'axios';
import UpdateTransportationInfo from '../components/UpdateTransportationInfo'; // ✅ Import new component

const UpdateVariablesPage = () => {
  const [activeTab, setActiveTab] = useState("pallet");
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/api/inventory/update_pallet_info/', formData);
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
        <div style={{ marginTop: 32 }}>
          <UpdateTransportationInfo />
        </div>
      )}
    </div>
  );
};

export default UpdateVariablesPage;

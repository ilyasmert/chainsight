import React, { useRef, useState } from 'react';
import { uploadExcelFile } from '../services/uploadApi';

const tableMapping = {
  ready: 'ready',
  sales: 'sales',
  intransit: 'intransit',
  atp_stock: 'atp_stock',
  to_be_produced: 'to_be_produced',
};

const UploadWeeklyFilesPage = () => {
  const [files, setFiles] = useState([]);
  const [uploadResults, setUploadResults] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  // --- Drag & Drop Handlers ---
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };
  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFiles([...e.dataTransfer.files].slice(0, 5));
      setUploadResults([]);
    }
  };

  // --- Button/File Logic ---
  const handleFileChange = (e) => {
    setFiles([...e.target.files].slice(0, 5));
    setUploadResults([]);
  };
  const triggerFileInput = () => {
    fileInputRef.current.value = "";
    fileInputRef.current.click();
  };

  // --- Upload Logic ---
  const handleSubmit = async () => {
    setUploading(true);
    const results = [];

    for (const file of files) {
      const lowerName = file.name.toLowerCase();
      const matchedKey = Object.keys(tableMapping).find((key) => lowerName.includes(key));
      if (!matchedKey) {
        results.push({ file: file.name, status: '❌ Unknown table name in filename' });
        continue;
      }
      try {
        const response = await uploadExcelFile(file, tableMapping[matchedKey], 'admin');
        results.push({ file: file.name, status: `✅ ${response.message}` });
      } catch (err) {
        results.push({
          file: file.name,
          status: `❌ ${err.response?.data?.error || 'Upload failed.'}`,
        });
      }
    }

    setUploadResults(results);
    setUploading(false);
    setFiles([]);
  };

  return (
    <div style={{
      maxWidth: 500,
      margin: "48px auto 0 auto",
      background: "#fff",
      border: "1px solid #bbb",
      borderRadius: 8,
      padding: "32px 32px 24px 32px",
      boxShadow: "0 2px 12px rgba(0,0,0,0.04)"
    }}>
      <h2 style={{ fontWeight: 600, fontSize: 22, marginBottom: 18 }}>Upload Weekly Excel Files</h2>
      <div style={{ marginBottom: 18, fontSize: 16 }}>
        Upload up to 5 excel files.
      </div>
      <div
        onClick={triggerFileInput}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        style={{
          border: dragActive ? "2px dashed #FF715B" : "2px dashed #bbb",
          background: dragActive ? "#fff5f3" : "#fafbfc",
          borderRadius: 8,
          padding: "32px 0",
          textAlign: "center",
          marginBottom: 18,
          cursor: uploading ? "not-allowed" : "pointer",
          transition: "border 0.2s, background 0.2s",
        }}
      >
        <button
          type="button"
          disabled={uploading}
          style={{
            background: "#FF715B",
            color: "#fff",
            border: "none",
            borderRadius: 5,
            fontSize: 16,
            padding: "10px 38px",
            marginBottom: 8,
            cursor: uploading ? "not-allowed" : "pointer"
          }}
        >
          Upload
        </button>
        <div style={{ color: "#ff715b", fontSize: 15, marginTop: 10 }}>
          Drag & drop or click 'Upload' to select up to 5 Excel files
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx"
          multiple
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
      </div>

      {files.length > 0 && (
        <div style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 14, color: "#333", marginBottom: 5 }}>📝 Selected Files:</div>
          <ul style={{ paddingLeft: 20, marginBottom: 5 }}>
            {files.map((file, i) => <li key={i}>{file.name}</li>)}
          </ul>
          <button
            onClick={handleSubmit}
            disabled={uploading}
            style={{
              background: "#26B35B",
              color: "#fff",
              border: "none",
              borderRadius: 5,
              fontSize: 15,
              padding: "8px 26px",
              marginTop: 4,
              cursor: uploading ? "not-allowed" : "pointer",
            }}
          >
            {uploading ? "Uploading..." : "Submit"}
          </button>
        </div>
      )}

      {uploadResults.length > 0 && (
        <div style={{ marginTop: 8 }}>
          {uploadResults.map((res, idx) => (
            <div key={idx} style={{ fontSize: 15, marginBottom: 2 }}>
              <b>{res.file}</b>: <span>{res.status}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UploadWeeklyFilesPage;

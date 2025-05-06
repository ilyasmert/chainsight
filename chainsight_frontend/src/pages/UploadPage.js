import React, { useRef, useState } from 'react';
import { uploadExcelFile } from '../services/uploadApi';

const tableMapping = {
  ready: 'ready',
  sales: 'sales',
  intransit: 'intransit',
  atp_stock: 'atp_stock',
  to_be_produced: 'to_be_produced',
};

const UploadPage = () => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadResults, setUploadResults] = useState([]);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setFiles([...e.target.files].slice(0, 5));
    setUploadResults([]);
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const handleUpload = async () => {
    setUploading(true);
    const results = [];

    for (const file of files) {
      const lowerName = file.name.toLowerCase();
      const matchedKey = Object.keys(tableMapping).find((key) => lowerName.includes(key));

      if (!matchedKey) {
        results.push({ file: file.name, status: '❌ Unknown table name' });
        continue;
      }

      try {
        const response = await uploadExcelFile(file, matchedKey, 'admin');
        results.push({ file: file.name, status: `✅ ${response.message}` });
      } catch (err) {
        results.push({ file: file.name, status: `❌ ${err.response?.data?.error || 'Upload failed'}` });
      }
    }

    setUploadResults(results);
    setUploading(false);
  };

  return (
    <div className="p-6 space-y-4">
      <button
        onClick={triggerFileInput}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload Excel Files ▸
      </button>

      <input
        type="file"
        accept=".xlsx"
        multiple
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />

      {files.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm text-gray-700">📝 Selected Files:</p>
          {files.map((file, index) => (
            <div key={index}>{file.name}</div>
          ))}

          <button
            onClick={handleUpload}
            disabled={uploading}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            {uploading ? 'Uploading...' : 'Start Upload'}
          </button>
        </div>
      )}

      {uploadResults.length > 0 && (
        <div className="mt-4">
          {uploadResults.map((result, index) => (
            <div key={index}>{result.status}: {result.file}</div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UploadPage;

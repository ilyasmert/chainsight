import React, { useState } from 'react';
import { uploadExcelFile } from '../services/uploadApi'; // ✅ cleaner abstraction

const tableMapping = {
  ready: 'ready',
  sales: 'sales',
  intransit: 'intransit',
  atp_stock: 'atp_stock',
  to_be_produced: 'to_be_produced',
};

const ExcelUploadModal = ({ isOpen, onClose }) => {
  const [files, setFiles] = useState([]);
  const [uploadResults, setUploadResults] = useState([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFiles = [...e.target.files].slice(0, 5);
    setFiles(selectedFiles);
    setUploadResults([]);
  };

  const handleUpload = async () => {
    setIsUploading(true);
    const results = [];

    for (const file of files) {
      const lowerName = file.name.toLowerCase();
      const matchedKey = Object.keys(tableMapping).find((key) =>
        lowerName.includes(key)
      );

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
    setIsUploading(false);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md space-y-4">
        <h2 className="text-xl font-bold">Upload Excel Files (1–5)</h2>

        <input
          type="file"
          accept=".xlsx"
          multiple
          onChange={handleFileChange}
          className="w-full"
        />

        {files.length > 0 && (
          <div className="text-sm text-gray-600">
            {files.map((file, i) => (
              <div key={i}>📄 {file.name}</div>
            ))}
          </div>
        )}

        {uploadResults.length > 0 && (
          <div className="text-sm space-y-1 mt-3">
            {uploadResults.map((res, i) => (
              <div key={i}>
                <strong>{res.file}</strong>: <span>{res.status}</span>
              </div>
            ))}
          </div>
        )}

        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded bg-gray-300 hover:bg-gray-400"
            disabled={isUploading}
          >
            Close
          </button>
          <button
            onClick={handleUpload}
            className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
            disabled={isUploading || files.length === 0}
          >
            {isUploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExcelUploadModal;

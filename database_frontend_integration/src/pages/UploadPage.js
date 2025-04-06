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
  const [expanded, setExpanded] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef();

  const toggleUploadSection = () => {
    setExpanded(prev => !prev);
    setFiles([]); // clear previous selections if collapsed
  };

  const handleFileChange = (e) => {
    setFiles([...e.target.files].slice(0, 5));
  };

  const handleUpload = async () => {
    setUploading(true);

    for (const file of files) {
      const lowerName = file.name.toLowerCase();
      const matchedKey = Object.keys(tableMapping).find((key) =>
        lowerName.includes(key)
      );

      if (!matchedKey) {
        alert(`❌ ${file.name}: Unknown table name`);
        continue;
      }

      try {
        const response = await uploadExcelFile(file, matchedKey, 'admin');
        alert(`✅ ${file.name}: ${response.message}`);
      } catch (err) {
        alert(`❌ ${file.name}: ${err.response?.data?.error || 'Upload failed'}`);
      }
    }

    setFiles([]);
    setUploading(false);
  };

  return (
    <div className="p-6 space-y-4">
      {/* Single visible button */}
      <button
        onClick={toggleUploadSection}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload Excel Files {expanded ? '▾' : '▸'}
      </button>


      {expanded && (
        <>
          <p className="text-sm text-gray-600">
            Upload 1 to 5 Excel files named like <code>ready.xlsx</code>, <code>sales.xlsx</code>, etc. <br />
            The app will archive existing data and insert new rows.
          </p>

          <input
            type="file"
            accept=".xlsx"
            multiple
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
          />


          {files.length > 0 && (
            <div className="space-y-2 mt-4">
              <p className="text-sm text-gray-700">📝 Files Selected:</p>
              {files.map((file, i) => (
                <div key={i}>• {file.name}</div>
              ))}

              <button
                onClick={handleUpload}
                disabled={uploading}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                {uploading ? 'Uploading...' : 'Upload Excel Files'}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default UploadPage;

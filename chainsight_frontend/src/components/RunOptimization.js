// src/components/RunOptimization.js

import React from 'react';

const RunOptimization = () => {
  return (
    <div className="p-4 bg-white rounded shadow-md">
      <h2 className="text-xl font-semibold mb-2">⚙️ Run Optimization</h2>
      <p>This section will allow users to run inventory/transportation optimization.</p>
      <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Run Now
      </button>
    </div>
  );
};

export default RunOptimization;

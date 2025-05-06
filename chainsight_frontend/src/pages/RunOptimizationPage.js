import React from 'react';

const playSVG = (
  <svg height="24" width="24" style={{ marginRight: 8, verticalAlign: 'middle' }} fill="#fff" viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="12" fill="#26B35B" />
    <polygon points="10,8 18,12 10,16" fill="#fff" />
  </svg>
);

const RunOptimization = () => {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '60vh'
    }}>
      <button
        style={{
          background: "#26B35B",
          color: "#fff",
          border: "none",
          borderRadius: 7,
          padding: "14px 38px",
          fontSize: 20,
          fontWeight: 600,
          boxShadow: "0 2px 8px rgba(38,179,91,0.10)",
          display: "flex",
          alignItems: "center",
          cursor: "pointer",
          marginTop: 30
        }}
        onClick={() => { /* Dummy action for now */ }}
      >
        {playSVG} Run
      </button>
      <div style={{ color: "#777", marginTop: 22, fontSize: 16 }}>Optimization will be run here soon.</div>
    </div>
  );
};

export default RunOptimization;

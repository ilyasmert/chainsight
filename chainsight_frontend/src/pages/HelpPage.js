import React, { useState } from 'react';

const helpSections = [
  {
    title: "📦 Inventory",
    description: `
      View and manage all inventory-related data (Ready, ATP Stock, Intransit, Sales, To Be Produced).
      - Filter by Product ID, Quantity, Week, Year, ETA.
      - Quantity filtering supports =, >, <.
      - Sticky headers while scrolling.
    `
  },
  {
    title: "📤 Upload Files",
    description: `
      Upload up to 5 Excel files at once for inventory tables.
      - Drag & drop or click to upload.
      - Automatically detects the table based on filename.
      - Archives previous data.
    `
  },
  {
    title: "🛠️ Update Variables",
    description: `
      Manage Pallet Info and Transportation Info.
      - Upload pallet Excel file (coming soon).
      - Edit Truck and Container weekly capacity and transit time live.
    `
  },
  {
    title: "🚀 Run Optimization",
    description: `
      Trigger optimization using the latest uploaded data.
      - "Run" button starts optimization process.
      - Outputs will be available for download (future feature).
    `
  }
];

const HelpPage = () => {
  const [openIndex, setOpenIndex] = useState(null);

  const toggleSection = (index) => {
    if (openIndex === index) {
      setOpenIndex(null); // Collapse if clicked again
    } else {
      setOpenIndex(index);
    }
  };

  return (
    <div style={{ padding: "32px", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ fontSize: "32px", fontWeight: "bold", marginBottom: "32px" }}>
        Help Center
      </h1>

      {helpSections.map((section, index) => (
        <div key={index} style={{ marginBottom: "32px" }}>
          <button
            onClick={() => toggleSection(index)}
            style={{
              width: "100%",
              textAlign: "left",
              padding: "20px 28px",
              background: "#e2e8f0",
              border: "none",
              borderRadius: "8px",
              fontSize: "20px",
              fontWeight: "600",
              cursor: "pointer",
              transition: "background 0.3s",
              color: "#111"
            }}
            onMouseOver={(e) => e.target.style.background = "#cbd5e1"}
            onMouseOut={(e) => e.target.style.background = "#e2e8f0"}
          >
            {section.title}
          </button>

          {openIndex === index && (
            <div
              style={{
                marginTop: "14px",
                background: "#f8fafc",
                padding: "18px 24px",
                borderRadius: "6px",
                border: "1px solid #cbd5e1",
                fontSize: "14px", /* SMALLER explanation */
                whiteSpace: "pre-line",
                color: "#444"
              }}
            >
              {section.description}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default HelpPage;

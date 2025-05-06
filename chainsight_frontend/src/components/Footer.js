import React from 'react';

const Footer = () => (
  <footer className="footer">
    <hr style={{ marginBottom: 12, opacity: 0.3 }} />
    <div style={{ textAlign: "center", color: "#888", fontSize: 14, padding: 12 }}>
      &copy; {new Date().getFullYear()} chAInsight. All rights reserved.
    </div>
  </footer>
);

export default Footer;

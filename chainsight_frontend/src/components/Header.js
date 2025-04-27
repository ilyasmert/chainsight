import React from 'react';

const Header = () => (
  <header className="header">
    <div className="font-bold">chAInsight</div>
    <div>
      <button style={{marginRight: 12}}>Help</button>
      <button>Logout</button>
      <span style={{marginLeft: 20, color: '#888'}}>Welcome, UserX</span>
    </div>
  </header>
);

export default Header;

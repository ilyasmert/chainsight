import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => (
  <nav className="sidebar">
    <div className="sidebar-links">
      <NavLink to="/inventory" activeClassName="active">Inventory</NavLink>
      <NavLink to="/inventory-archive" activeClassName="active">Inventory Archive</NavLink> {/* 🆕 added */}
      <NavLink to="/upload" activeClassName="active">Upload Files</NavLink>
      <NavLink to="/variables" activeClassName="active">Update Variables</NavLink>
      <NavLink to="/optimization" activeClassName="active">Run Optimization</NavLink>
    </div>

    <div className="sidebar-footer">
      <NavLink to="/help" activeClassName="active" className="help-link">❓ Help</NavLink>
    </div>
  </nav>
);

export default Sidebar;

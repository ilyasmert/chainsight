import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => (
  <nav className="sidebar">
    <NavLink to="/inventory" activeClassName="active">Inventory</NavLink>
    <NavLink to="/upload" activeClassName="active">Upload Files</NavLink>
    <NavLink to="/variables" activeClassName="active">Update Variables</NavLink>
    <NavLink to="/optimization" activeClassName="active">Run Optimization</NavLink>
  </nav>
);

export default Sidebar;

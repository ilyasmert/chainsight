import React, { useContext } from "react";
import { NavLink } from "react-router-dom";
import { AuthContext } from "./AuthContext";

const Sidebar = () => {
  const { loggedIn } = useContext(AuthContext);
  if (!loggedIn) return null;

  return (
    <nav className="sidebar">
      <div className="sidebar-links">
        <NavLink to="/inventory" activeClassName="active">
          Inventory
        </NavLink>
        <NavLink to="/inventory-archive" activeClassName="active">
          Inventory Archive
        </NavLink>
        <NavLink to="/upload" activeClassName="active">
          Upload Files
        </NavLink>
        <NavLink to="/variables" activeClassName="active">
          Update Variables
        </NavLink>
        <NavLink to="/optimization" activeClassName="active">
          Run Optimization
        </NavLink>
      </div>

      <div className="sidebar-footer">
        <NavLink to="/help" activeClassName="active" className="help-link">
          ❓ Help
        </NavLink>
      </div>
    </nav>
  );
};

export default Sidebar;

import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import "./Header.css";

const Header = () => {
  const navigate = useNavigate();
  const { loggedIn, setLoggedIn } = useContext(AuthContext);
  const [showModal, setShowModal] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLoginClick = () => {
    setShowModal(true);
    setError("");
    setUsername("");
    setPassword("");
  };

  const handleLogout = () => {
    setLoggedIn(false);
    navigate("/");
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username === "admin" && password === "admin") {
      setLoggedIn(true);
      setShowModal(false);
      setError("");
    } else {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="header flex justify-between items-center p-4 border-b">
      <span
        className="font-bold text-lg cursor-pointer text-black"
        onClick={() => navigate("/")}
      >
        chAInSight
      </span>
      <div className="flex items-center space-x-2">
        {loggedIn ? (
          <>
            <button onClick={handleLogout} className="btn btn-secondary">
              Logout
            </button>
            <span className="text-xs text-gray-500 ml-2">Welcome, admin</span>
          </>
        ) : (
          <button onClick={handleLoginClick} className="btn btn-primary">
            Login
          </button>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
              <label>Username</label>
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              {error && <p className="error-text">{error}</p>}
              <div className="actions">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Login
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Header;

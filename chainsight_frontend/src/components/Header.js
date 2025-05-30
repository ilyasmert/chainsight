import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import { login, register, logout } from "../services/userApi";
import "./Header.css";

const Header = () => {
  const navigate = useNavigate();
  const { loggedIn, setLoggedIn, user, setUser } = useContext(AuthContext);

  const [showModal, setShowModal] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const today = new Date().toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  const openModal = (registerMode = false) => {
    setIsRegister(registerMode);
    setError("");
    setUsername("");
    setEmail("");
    setPassword("");
    setShowModal(true);
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (_) {
      // ignore
    }
    setLoggedIn(false);
    setUser(null);
    navigate("/");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const fn = isRegister ? register : login;
      const body = isRegister
        ? { username, email, password }
        : { username, password };

      const { data } = await fn(body);

      if (data.success) {
        if (isRegister) {
          // after registering, switch to login mode
          setIsRegister(false);
          setError("Registered! Please log in.");
        } else {
          setLoggedIn(true);
          setUser(data.username);
          setShowModal(false);
        }
      } else {
        setError(data.error || "Unknown error");
      }
    } catch (err) {
      setError(err.response?.data?.error || "Network error");
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

      <div className="flex items-center space-x-4">
        <span className="text-sm text-black-600">{today}</span>
        <div className="h-4 border-l border-gray-400" />

        {loggedIn ? (
          <>
            <span className="text-xs text-gray-500 ml-2">Welcome, {user}</span>
            <button onClick={handleLogout} className="btn ml-2">
              Logout
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() => openModal(false)}
              className="btn btn-primary"
            >
              Login
            </button>
            <button
              onClick={() => openModal(true)}
              className="btn btn-secondary"
            >
              Register
            </button>
          </>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>{isRegister ? "Register" : "Login"}</h2>
            <form onSubmit={handleSubmit}>
              <label>Username</label>
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />

              {isRegister && (
                <>
                  <label>Email</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </>
              )}

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
                  {isRegister ? "Register" : "Login"}
                </button>
              </div>
            </form>

            <p className="mt-2 text-sm">
              {isRegister
                ? "Already have an account? "
                : "Don't have an account? "}
              <button
                onClick={() => {
                  setIsRegister(!isRegister);
                  setError("");
                }}
                className="text-blue-600 underline"
              >
                {isRegister ? "Login" : "Register"}
              </button>
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Header;

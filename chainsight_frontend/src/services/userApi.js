import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/inventory",
  withCredentials: true, // send & receive cookies for session auth
  headers: { "Content-Type": "application/json" },
});

export const register = ({ username, email, password }) =>
  apiClient.post("/register/", { username, email, password });

export const login = ({ username, password }) =>
  apiClient.post("/login/", { username, password });

export const logout = () => apiClient.post("/logout/");

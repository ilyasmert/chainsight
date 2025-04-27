import React from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import InventoryPage from "./pages/InventoryPage";
import UploadWeeklyFilesPage from "./pages/UploadWeeklyFilesPage";
import UpdateVariablesPage from "./pages/UpdateVariablesPage";
import RunOptimizationPage from "./pages/RunOptimizationPage"; // If you have your main styles here
import Footer from "./components/Footer";
import DashboardLayout from "./layouts/DashboardLayout";
import HomePage from "./pages/HomePage";
import "./App.css";

const App = () => {
  return (
    <DashboardLayout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/inventory" element={<InventoryPage />} />
        <Route path="/upload" element={<UploadWeeklyFilesPage />} />
        <Route path="/variables" element={<UpdateVariablesPage />} />
        <Route path="/optimization" element={<RunOptimizationPage />} />
      </Routes>
    </DashboardLayout>
  );
};
export default App;

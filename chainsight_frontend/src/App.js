import React from "react";
import { Routes, Route, Navigate } from "react-router-dom"; // Import Navigate
//import Sidebar from "./components/Sidebar";
//import Header from "./components/Header";
import InventoryPage from "./pages/InventoryPage";
import UploadWeeklyFilesPage from "./pages/UploadWeeklyFilesPage";
import UpdateVariablesPage from "./pages/UpdateVariablesPage";
import RunOptimizationPage from "./pages/RunOptimizationPage"; // If you have your main styles here
//import Footer from "./components/Footer";
import DashboardLayout from "./layouts/DashboardLayout";
import HomePage from "./pages/HomePage"; // You might replace this or keep it if it's different from Dashboard
import HelpPage from "./pages/HelpPage";
import InventoryArchivePage from "./pages/InventoryArchivePage";
import DashboardPage from "./components/DashboardPage"; // Ensure this path is correct

import "./App.css";

const App = () => {
  return (
    <DashboardLayout>
      <Routes>
        {/* Redirect root path to /dashboard */}
        <Route path="/" element={<Navigate replace to="/dashboard" />} />
        {/* Define the route for the DashboardPage */}
        <Route path="/dashboard" element={<DashboardPage />} />

        {/* Keep your other existing routes */}
        <Route path="/inventory" element={<InventoryPage />} />
        <Route path="/inventory-archive" element={<InventoryArchivePage />} />
        <Route path="/upload" element={<UploadWeeklyFilesPage />} />
        <Route path="/variables" element={<UpdateVariablesPage />} />
        <Route path="/optimization" element={<RunOptimizationPage />} />
        <Route path="/help" element={<HelpPage />} />

        {/* If HomePage is different and still needed, you can keep its route,
            otherwise, the dashboard will be the primary landing page.
            If HomePage was intended to be the dashboard, you can remove its specific route
            or rename/refactor HomePage to be DashboardPage.
            For now, I'll assume DashboardPage is the new main entry.
        */}
        {/* <Route path="/home" element={<HomePage />} /> */}

      </Routes>
    </DashboardLayout>
  );
};
export default App;
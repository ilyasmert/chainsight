import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Footer from '../components/Footer';

const DashboardLayout = ({ children }) => (
  <div className="app-container">
    <Header />
    <div className="main-layout">
      <Sidebar />
      <main className="main-content">
        {children}
      </main>
    </div>
    <Footer />
  </div>
);

export default DashboardLayout;

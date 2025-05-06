import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();
  const today = new Date().toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }); // Output: 06 May 2025
  return (
    <div className="header flex justify-between items-center p-4 border-b">
      <span
        className="font-bold text-lg"
        style={{ cursor: 'pointer', color: '#000000' }}
        onClick={() => navigate('/')}
      >
        chAInSight
      </span>
      <div className="flex items-center space-x-4">
        <span className="text-sm text-black-600">{today}</span>
        <div className="h-4 border-l border-gray-400" />
        <span className="text-xs text-gray-500">Welcome, admin</span>
        <button className="btn ml-2">Logout</button>
      </div>
    </div>
  );
};

export default Header;

import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  return (
    <div className="header flex justify-between items-center p-4 border-b">
      <span
        className="font-bold text-lg"
        style={{ cursor: 'pointer', color: '#OOOOOO' }}
        onClick={() => navigate('/')}
      >
        chAInSight
      </span>
      <div className="flex items-center space-x-2">
        <button className="btn">Help</button>
        <button className="btn">Logout</button>
        <span className="text-xs text-gray-500 ml-2">Welcome, UserX</span>
      </div>
    </div>
  );
};

export default Header;

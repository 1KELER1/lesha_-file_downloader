import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

function ProtectedRoute() {
  const isAuthenticated = !!localStorage.getItem('access_token');
  
  // Если пользователь не аутентифицирован, перенаправляем на страницу входа
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
}

export default ProtectedRoute; 
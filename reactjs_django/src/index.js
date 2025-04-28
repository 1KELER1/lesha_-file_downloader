import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import '../src/resources/css/bootstrap.min.css'
import App from './App';
import reportWebVitals from './reportWebVitals';
import {Route, BrowserRouter, Routes, Navigate} from 'react-router-dom';
import UploadFile from './components/UploadFile'
import UserProfile from './components/UserProfile'
import ProtectedRoute from './components/ProtectedRoute'
import Header from './components/Header';

// Инициализируем axios с токеном авторизации, если он есть
import axios from 'axios';
const token = localStorage.getItem('access_token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

function Router(){
  return(
    <BrowserRouter>
      <Routes>
        {/* Публичные маршруты */}
        <Route path="/welcome" element={<Header />} />
        
        {/* Защищенные маршруты */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<UploadFile />} />
          <Route path="/app" element={<App />} />
          <Route path="/profile" element={<UserProfile />} />
        </Route>
        
        {/* Перенаправление */}
        <Route path="*" element={<Navigate to="/welcome" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

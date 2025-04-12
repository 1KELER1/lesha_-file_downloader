import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  
  const api = 'http://127.0.0.1:8000';

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          navigate('/login');
          return;
        }
        
        const config = {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        };
        
        const response = await axios.get(`${api}/api/user/`, config);
        setUser(response.data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete axios.defaults.headers.common['Authorization'];
    navigate('/login');
  };

  if (loading) {
    return <div className="text-center mt-5"><div className="spinner-border"></div></div>;
  }

  return (
    <div className="container mt-3">
      <div className="card">
        <div className="card-header bg-info text-white d-flex justify-content-between align-items-center">
          <h4 className="mb-0">Профиль пользователя</h4>
          <button className="btn btn-danger" onClick={handleLogout}>Выйти</button>
        </div>
        <div className="card-body">
          {user && (
            <div>
              <p><strong>Имя пользователя:</strong> {user.username}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <hr />
              <button className="btn btn-primary" onClick={() => navigate('/')}>
                Перейти к файлам
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default UserProfile; 
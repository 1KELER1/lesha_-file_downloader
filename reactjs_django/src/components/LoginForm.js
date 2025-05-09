import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Header from './Header';

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  // Используем переменную окружения для API URL
  const api = process.env.REACT_APP_API_URL || '';

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${api}/api/token/`, {
        username,
        password
      });
      
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
      
      // Перенаправляем на главную страницу
      navigate('/');
    } catch (err) {
      setError('Неверное имя пользователя или пароль');
      console.error(err);
    }
  };

  return (
    <>
      <Header />
      <div className="container mt-3">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <div className="card-header bg-primary text-white">
                <h4 className="mb-0">Вход в систему</h4>
              </div>
              <div className="card-body">
                {error && <div className="alert alert-danger">{error}</div>}
                <form onSubmit={handleSubmit}>
                  <div className="form-group mb-3">
                    <label htmlFor="username">Имя пользователя</label>
                    <input
                      type="text"
                      className="form-control"
                      id="username"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      required
                    />
                  </div>
                  
                  <div className="form-group mb-3">
                    <label htmlFor="password">Пароль</label>
                    <input
                      type="password"
                      className="form-control"
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </div>
                  
                  <button type="submit" className="btn btn-primary">Войти</button>
                </form>
                
                <div className="mt-3">
                  <p>Нет аккаунта? <a href="/register">Зарегистрироваться</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default LoginForm; 
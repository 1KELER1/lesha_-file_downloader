import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Header from './Header';

function RegisterForm() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  // Используем переменную окружения для API URL
  const api = process.env.REACT_APP_API_URL || '';

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Проверка на совпадение паролей на стороне клиента
    if (password !== password2) {
      setError('Пароли не совпадают');
      return;
    }

    try {
      await axios.post(`${api}/api/register/`, {
        username,
        email,
        password,
        password2,
        first_name: firstName,
        last_name: lastName
      });
      
      // При успешной регистрации перенаправляем на страницу входа
      navigate('/login');
    } catch (err) {
      console.error(err);
      if (err.response && err.response.data) {
        // Отображаем ошибки с сервера
        const errorMessages = Object.values(err.response.data)
          .flat()
          .join(', ');
        setError(errorMessages || 'Ошибка при регистрации');
      } else {
        setError('Ошибка соединения с сервером');
      }
    }
  };

  return (
    <>
      <Header />
      <div className="container mt-3">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <div className="card-header bg-success text-white">
                <h4 className="mb-0">Регистрация</h4>
              </div>
              <div className="card-body">
                {error && <div className="alert alert-danger">{error}</div>}
                <form onSubmit={handleSubmit}>
                  <div className="form-group mb-3">
                    <label htmlFor="username">Имя пользователя *</label>
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
                    <label htmlFor="email">Email *</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>

                  <div className="form-group mb-3">
                    <label htmlFor="firstName">Имя</label>
                    <input
                      type="text"
                      className="form-control"
                      id="firstName"
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                    />
                  </div>

                  <div className="form-group mb-3">
                    <label htmlFor="lastName">Фамилия</label>
                    <input
                      type="text"
                      className="form-control"
                      id="lastName"
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                    />
                  </div>
                  
                  <div className="form-group mb-3">
                    <label htmlFor="password">Пароль *</label>
                    <input
                      type="password"
                      className="form-control"
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </div>
                  
                  <div className="form-group mb-3">
                    <label htmlFor="password2">Подтверждение пароля *</label>
                    <input
                      type="password"
                      className="form-control"
                      id="password2"
                      value={password2}
                      onChange={(e) => setPassword2(e.target.value)}
                      required
                    />
                  </div>
                  
                  <button type="submit" className="btn btn-success">Зарегистрироваться</button>
                </form>
                
                <div className="mt-3">
                  <p>Уже есть аккаунт? <a href="/login">Войти</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default RegisterForm; 
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Header() {
  const [activeTab, setActiveTab] = useState(0);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [email, setEmail] = useState('');
  const [password2, setPassword2] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [registerError, setRegisterError] = useState('');
  const navigate = useNavigate();
  
  // Используем переменную окружения для API URL
  const api = process.env.REACT_APP_API_URL || '';

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${api}/api/token/`, {
        username,
        password
      });
      
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
      
      // Перенаправляем на главную страницу системы
      navigate('/');
    } catch (err) {
      setError('Неверное имя пользователя или пароль');
      console.error(err);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();

    // Проверка на совпадение паролей на стороне клиента
    if (password !== password2) {
      setRegisterError('Пароли не совпадают');
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
      
      // При успешной регистрации переключаемся на вкладку входа
      setActiveTab(4);
      // Очищаем форму регистрации
      setEmail('');
      setPassword2('');
      setFirstName('');
      setLastName('');
      setRegisterError('');
    } catch (err) {
      console.error(err);
      if (err.response && err.response.data) {
        // Отображаем ошибки с сервера
        const errorMessages = Object.values(err.response.data)
          .flat()
          .join(', ');
        setRegisterError(errorMessages || 'Ошибка при регистрации');
      } else {
        setRegisterError('Ошибка соединения с сервером');
      }
    }
  };

  const tabs = [
    {
      id: 0,
      title: 'Основная информация',
      content: (
        <div className="py-3">
          <h4 className="mb-3 text-primary">Название, категория работы, автор, руководитель</h4>
          <div className="card-text">
            <p><strong>Название:</strong> Разработка лендинг-страницы центра экологической экспертизы ФГБОУ ВО «АнГТУ». UI/UX дизайн</p>
            <p><strong>Категория работы:</strong> Веб-приложение</p>
            <p><strong>Автор:</strong> Рыбин А.В.</p>
            <p><strong>Руководитель:</strong> Головкова Е.А.</p>
          </div>
        </div>
      )
    },
    {
      id: 1,
      title: 'Цели и задачи',
      content: (
        <div className="py-3">
          <h4 className="mb-3 text-primary">Цели, задачи работы, план работы</h4>
          <div className="card-text">
            <p><strong>Цель:</strong> Разработка фронтенда</p>
            <p><strong>Задачи:</strong></p>
            <ul className="list-group list-group-flush mb-3">
              <li className="list-group-item">Анализ целевой аудитории</li>
              <li className="list-group-item">Изучение конкурентной среды</li>
              <li className="list-group-item">Формирование структуры лендинг-страницы:</li>
              <li className="list-group-item">Создание прототипа</li>
              <li className="list-group-item">Разработка UI-дизайна:</li>
              <li className="list-group-item">Оптимизация UX</li>
              <li className="list-group-item">Верстка и программирование</li>
              <li className="list-group-item">Тестирование</li>
              <li className="list-group-item">Запуск и анализ результатов</li>
            </ul>
             <p><strong>План работы:</strong></p>
            <ul className="list-group list-group-flush mb-3">
              <li className="list-group-item">1. Подготовительный этап</li>
              <li className="list-group-item">2. Исследование</li>
              <li className="list-group-item">3. Проектирование</li>
              <li className="list-group-item">4. Концепт</li>
              <li className="list-group-item">5. Создание прототипа</li>
              <li className="list-group-item">6. Тестирование</li>
              <li className="list-group-item">7. Публикация</li>
              <li className="list-group-item">8. Анализ и улучшение</li>
            </ul>
          </div>
        </div>
      )
    },
    {
      id: 2,
      title: 'Результаты',
      content: (
        <div className="py-3">
          <h4 className="mb-3 text-primary">Теоретические и практические результаты</h4>
          <div className="card-text">
            <div className="row">
              <div className="col-md-6">
                <div className="card mb-3">
                  <div className="card-header bg-light">
                    <h5 className="mb-0">Теоретические результаты</h5>
                  </div>
                  <ul className="list-group list-group-flush">
                    <li className="list-group-item">Изучение принципов создания лендинг-страниц</li>
                    <li className="list-group-item">Формирование знаний о UI/UX дизайне</li>
                    <li className="list-group-item">Понимание пользовательских сценариев</li>
                    <li className="list-group-item">Овладение современными подходами к адаптивному дизайну</li>
                    <li className="list-group-item">Аналитика эффективности лендингов</li>
                  </ul>
                </div>
              </div>
              <div className="col-md-6">
                <div className="card mb-3">
                  <div className="card-header bg-light">
                    <h5 className="mb-0">Практические результаты</h5>
                  </div>
                  <ul className="list-group list-group-flush">
                    <li className="list-group-item">Разработана лендинг-страница</li>
                    <li className="list-group-item">Создан полноценный UI/UX дизайн</li>
                    <li className="list-group-item">Реализована адаптивная верстка лендинга</li>
                    <li className="list-group-item">Интегрированы интерактивные элементы</li>
                    <li className="list-group-item">Произведено тестирование и оптимизация страницы</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 3,
      title: 'Модуль',
      content: (
        <div className="py-3">
          <h4 className="mb-3 text-primary">Модуль, в соответствии с индивидуальным заданием</h4>
          <div className="card bg-light">
            <div className="card-body">
              <p>Реализация модуля загрузки файлов с валидацией и фильтрацией по типам.</p>
              <p className="mb-0">Возможность просмотра загруженных файлов и управления ими.</p>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 4,
      title: 'Авторизация',
      content: (
        <div className="py-3">
          <h4 className="mb-3 text-primary">Вход в систему</h4>
          <div className="card">
            <div className="card-body">
              {error && <div className="alert alert-danger">{error}</div>}
              <form onSubmit={handleLoginSubmit}>
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
                <p>Нет аккаунта? <button className="btn btn-link p-0" onClick={() => setActiveTab(5)}>Зарегистрироваться</button></p>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 5,
      title: 'Регистрация',
      content: (
        <div className="py-3">
          <h4 className="mb-3 text-primary">Регистрация</h4>
          <div className="card">
            <div className="card-body">
              {registerError && <div className="alert alert-danger">{registerError}</div>}
              <form onSubmit={handleRegisterSubmit}>
                <div className="form-group mb-3">
                  <label htmlFor="reg-username">Имя пользователя *</label>
                  <input
                    type="text"
                    className="form-control"
                    id="reg-username"
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
                  <label htmlFor="reg-password">Пароль *</label>
                  <input
                    type="password"
                    className="form-control"
                    id="reg-password"
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
                <p>Уже есть аккаунт? <button className="btn btn-link p-0" onClick={() => setActiveTab(4)}>Войти</button></p>
              </div>
            </div>
          </div>
        </div>
      )
    }
  ];

  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
  };

  // Проверяем, авторизован ли пользователь
  const isAuthenticated = !!localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete axios.defaults.headers.common['Authorization'];
    navigate('/welcome');
  };

  return (
    <div className="container mt-4 mb-4">
      <div className="card shadow">
        <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
          <h3 className="mb-0">Курсовая работа</h3>
          <div>
            {isAuthenticated ? (
              <div className="d-flex">
                <Link to="/" className="btn btn-light me-2">Главная</Link>
                <Link to="/profile" className="btn btn-light me-2">Профиль</Link>
                <button 
                  type="button" 
                  className="btn btn-danger"
                  onClick={handleLogout}
                >
                  Выйти
                </button>
              </div>
            ) : (
              <div className="d-flex">
                <button 
                  type="button" 
                  className="btn btn-light me-2"
                  onClick={() => setActiveTab(4)}
                >
                  Войти
                </button>
                <button 
                  type="button" 
                  className="btn btn-light"
                  onClick={() => setActiveTab(5)}
                >
                  Регистрация
                </button>
              </div>
            )}
          </div>
        </div>
        <div className="card-body">
          <ul className="nav nav-tabs mb-3">
            {tabs.slice(0, 4).map(tab => (
              <li className="nav-item" key={tab.id}>
                <button 
                  type="button"
                  className={`nav-link ${activeTab === tab.id ? 'active fw-bold' : ''}`} 
                  onClick={() => handleTabClick(tab.id)}
                >
                  {tab.title}
                </button>
              </li>
            ))}
          </ul>
          <div className="tab-content" style={{ minHeight: '250px', transition: 'all 0.3s ease' }}>
            {tabs.find(tab => tab.id === activeTab)?.content}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Header; 
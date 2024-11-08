import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = ({ setIsAuthenticated }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('https://sanches.pythonanywhere.com/login', { username, password });
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      setIsAuthenticated(true);
      setMessage('Вход выполнен успешно!');
      navigate('/products'); // Перенаправляем на страницу с продуктами
    } catch (error) {
      setMessage('Ошибка входа. Попробуйте снова.');
    }
  };

  return (
      <div className="login-container">
        <form onSubmit={handleSubmit}>
          <h2>Вход</h2>
          <input
              type="text"
              placeholder="Имя пользователя"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
          />
          <input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
          />
          <button type="submit">Войти</button>
        </form>
        {message && <p>{message}</p>}
      </div>
  );
};

export default Login;

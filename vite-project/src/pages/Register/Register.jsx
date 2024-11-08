import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Register.css';

const Register = ({ setIsAuthenticated }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      const response = await axios.post('https://sanches.pythonanywhere.com/register', {
        username,
        email,
        password,
        role
      });
      if (response.status === 201) {
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        setIsAuthenticated(true);
        setMessage('Регистрация выполнена успешно!');
        navigate('/products'); // Перенаправляем на страницу с продуктами
      }
    } catch (error) {
      setMessage('Ошибка регистрации. Попробуйте снова.');
    } finally {
      setLoading(false);
    }
  };

  return (
      <div className="register-container">
        <form onSubmit={handleSubmit}>
          <h2>Регистрация</h2>
          {message && <p>{message}</p>}
          <input
              type="text"
              placeholder="Имя пользователя"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
          />
          <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
          />
          <input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
          />
          <input
              type="text"
              placeholder="Роль"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Регистрация...' : 'Зарегистрироваться'}
          </button>
        </form>
      </div>
  );
};

export default Register;

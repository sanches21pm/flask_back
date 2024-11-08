import React, { useState } from 'react';
import axios from 'axios';
import './RegisterAdmin.css';

const RegisterAdmin = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      const response = await axios.post('/register_admin', { username, email, password });
      if (response.status === 201) {
        setMessage('Admin registered successfully');
        setUsername('');
        setEmail('');
        setPassword('');
      }
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setMessage('Username already exists');
      } else {
        setMessage('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-admin-container">
      <form onSubmit={handleSubmit}>
        <h2>Register Admin</h2>
        {message && <p>{message}</p>}
        <input
          type="text"
          placeholder="Username"
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
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
};

export default RegisterAdmin;

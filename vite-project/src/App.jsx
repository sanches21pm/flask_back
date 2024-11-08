import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header/Header';
import Home from './pages/Home/Home';
import Categories from './pages/Categories/Categories';
import CategoryDetail from './pages/CategoryDetail/CategoryDetail';
import Products from './pages/Products/Products';
import ProductDetail from './pages/ProductDetail/ProductDetail';
import Reviews from './pages/Reviews/Reviews';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Profile from './pages/Profile/Profile';
import RegisterAdmin from './pages/RegisterAdmin/RegisterAdmin';
import PrivateRoute from './components/PrivateRoute';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import './App.css';

import AddProduct from './pages/Products/AddProduct';
import AddCategory from './pages/AddCategory/AddCategory';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Проверка токена при загрузке приложения
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  // Функция для выхода из аккаунта
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
  };

  return (
      <ThemeProvider theme={theme}>
        <Router>
          <Header isAuthenticated={isAuthenticated} handleLogout={handleLogout} />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/categories" element={<Categories />} />
            <Route path="/categories/:category_id" element={<CategoryDetail />} />
            <Route path="/products" element={<Products />} />
            <Route path="/products/:product_id" element={<ProductDetail />} />
            <Route path="/products/:product_id/reviews" element={<Reviews />} />
            <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<PrivateRoute element={Profile} />} />
            <Route path="/register_admin" element={<PrivateRoute element={RegisterAdmin} />} />
            <Route path="/add-product" element={<AddProduct />} />
            <Route path="/add-category" element={<AddCategory />} />

          </Routes>
        </Router>
      </ThemeProvider>
  );
};

export default App;

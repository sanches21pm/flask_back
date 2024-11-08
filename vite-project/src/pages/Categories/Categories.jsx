import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import { FaPlusCircle } from 'react-icons/fa';
import './Categories.css';

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSeller, setIsSeller] = useState(false);
  const navigate = useNavigate();

  const fetchProfile = async () => {
    const token = localStorage.getItem('access_token');
    try {
      const response = await axios.get('https://sanches.pythonanywhere.com/profile', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setIsSeller(response.data.role === 'seller' || response.data.role === 'admin');
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get('https://sanches.pythonanywhere.com/categories');
      setCategories(response.data);
    } catch (error) {
      console.error('Ошибка загрузки категорий:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
    fetchCategories();
  }, []);

  const handleAddCategory = () => {
    navigate('/add-category');
  };

  if (loading) {
    return <p>Загрузка...</p>;
  }

  return (
      <div className="categories-container">
        <h2>Categories</h2>
        <div className="categories-grid">
          {isSeller && (
              <div className="category-card add-category-card" onClick={handleAddCategory}>
                <FaPlusCircle className="add-category-icon" />
                <h3 className="add-category-text">Добавить категорию</h3>
              </div>
          )}
          {categories.map((category) => (
              <div className="category-card" key={category.id}>
                <img src={category.image || 'https://via.placeholder.com/150'} alt={category.name} className="category-image" />
                <h3 className="category-name">{category.name}</h3>
                <p className="category-description">{category.description}</p>
                <Link to={`/categories/${category.id}`} className="category-link">Посмотреть продукты</Link>
              </div>
          ))}
        </div>
      </div>
  );
};

export default Categories;

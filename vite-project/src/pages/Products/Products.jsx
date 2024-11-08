import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FaPlusCircle } from 'react-icons/fa';
import './Products.css';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSeller, setIsSeller] = useState(false);
  const navigate = useNavigate();

  // Получение профиля пользователя
  const fetchProfile = async () => {
    const token = localStorage.getItem('access_token');
    try {
      const response = await axios.get('https://sanches.pythonanywhere.com/profile', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setIsSeller(response.data.role === 'seller');
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error);
    }
  };

  // Получение списка продуктов
  const fetchProducts = async () => {
    const token = localStorage.getItem('access_token');
    try {
      const response = await axios.get('https://sanches.pythonanywhere.com/products', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setProducts(response.data);
    } catch (error) {
      console.error('Ошибка загрузки продуктов:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
    fetchProducts();
  }, []);

  // Переход к добавлению продукта
  const handleAddProduct = () => {
    navigate('/add-product');
  };

  // Переход на страницу с деталями продукта
  const handleProductClick = (productId) => {
    navigate(`/products/${productId}`);
  };

  if (loading) {
    return <p>Загрузка...</p>;
  }

  return (
      <div className="products-container">
        <div className="products-grid">
          {isSeller && (
              <div className="product-card add-product-card" onClick={handleAddProduct}>
                <FaPlusCircle className="add-product-icon" />
                <h3 className="add-product-text">Добавить продукт</h3>
              </div>
          )}
          {products.map((product) => (
              <div
                  className="product-card"
                  key={product.id}
                  onClick={() => handleProductClick(product.id)}
              >
                <h3 className="product-name">{product.name}</h3>
                <p className="product-price">${product.price}</p>
                <p className="product-description">{product.description}</p>
              </div>
          ))}
        </div>
      </div>
  );
};

export default Products;

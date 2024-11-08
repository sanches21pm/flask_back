import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './CategoryDetail.css';

const CategoryDetail = () => {
  const { category_id } = useParams();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Функция для получения продуктов категории
  const fetchCategoryProducts = async () => {
    try {
      const response = await axios.get(`https://sanches.pythonanywhere.com/categories/${category_id}/products`);
      setProducts(response.data);
    } catch (error) {
      console.error('Ошибка загрузки продуктов:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategoryProducts();
  }, [category_id]);

  if (loading) {
    return <p>Загрузка...</p>;
  }

  return (
      <div className="category-detail-container">
        <h2>Продукты категории</h2>
        {products.length === 0 ? (
            <p>В этой категории пока нет продуктов.</p>
        ) : (
            <div className="products-grid">
              {products.map((product) => (
                  <div className="product-card" key={product.id}>
                    <h3 className="product-name">{product.name}</h3>
                    <p className="product-price">${product.price}</p>
                    <p className="product-description">{product.description}</p>
                  </div>
              ))}
            </div>
        )}
      </div>
  );
};

export default CategoryDetail;

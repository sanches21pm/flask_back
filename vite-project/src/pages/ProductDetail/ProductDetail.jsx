import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { FaStar } from 'react-icons/fa';
import './ProductDetail.css';

const ProductDetail = () => {
  const { product_id } = useParams();
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [newReview, setNewReview] = useState('');
  const [rating, setRating] = useState(0);
  const [hover, setHover] = useState(null);
  const [role, setRole] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('access_token');
      try {
        const productResponse = await axios.get('https://sanches.pythonanywhere.com/products', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const productData = productResponse.data.find((item) => item.id === parseInt(product_id, 10));
        setProduct(productData || {});

        const profileResponse = await axios.get('https://sanches.pythonanywhere.com/profile', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setRole(profileResponse.data.role);

        const reviewsResponse = await axios.get(`https://sanches.pythonanywhere.com/products/${product_id}/reviews`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setReviews(reviewsResponse.data);
      } catch (error) {
        setMessage('Ошибка загрузки информации о продукте.');
      }
    };

    fetchData();
  }, [product_id]);

  const handleAddReview = async () => {
    const token = localStorage.getItem('access_token');
    try {
      await axios.post(
          `https://sanches.pythonanywhere.com/products/${product_id}/review`,
          { content: newReview, rating },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
      );
      setMessage('Отзыв успешно добавлен!');
      setNewReview('');
      setRating(0);
      const updatedReviews = await axios.get(`https://sanches.pythonanywhere.com/products/${product_id}/reviews`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setReviews(updatedReviews.data);
    } catch (error) {
      setMessage('Не удалось добавить отзыв.');
    }
  };

  const handleDeleteReview = async (review_id) => {
    const token = localStorage.getItem('access_token');
    try {
      await axios.delete(`https://sanches.pythonanywhere.com/products/${product_id}/review/${review_id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessage('Отзыв успешно удалён!');
      const updatedReviews = await axios.get(`https://sanches.pythonanywhere.com/products/${product_id}/reviews`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setReviews(updatedReviews.data);
    } catch (error) {
      setMessage('Ошибка при удалении отзыва.');
    }
  };

  return (
      <div className="product-detail-container">
        {product ? (
            <>
              <h2 className="product-name">{product.name}</h2>
              <p className="product-description">{product.description}</p>
              <p className="product-price">Цена: ${product.price}</p>

              <h3>Отзывы:</h3>
              <div className="reviews-list">
                {reviews.length > 0 ? (
                    reviews.map((review) => (
                        <div key={review.id} className="review-box">
                          <div className="review-rating">
                            {[...Array(5)].map((star, index) => (
                                <FaStar
                                    key={index}
                                    color={index < review.rating ? '#ffc107' : '#e4e5e9'}
                                    size={20}
                                />
                            ))}
                          </div>
                          <p className="review-content">{review.content}</p>
                          {(role === 'admin' || role === 'user') && (
                              <button
                                  onClick={() => handleDeleteReview(review.id)}
                                  className="delete-review-button"
                              >
                                Удалить
                              </button>
                          )}
                        </div>
                    ))
                ) : (
                    <p>Отзывов пока нет.</p>
                )}
              </div>

              {role === 'user' && (
                  <div className="add-review-form">
                    <h3>Добавить отзыв</h3>
                    <div className="rating-stars">
                      {[...Array(5)].map((star, index) => {
                        const ratingValue = index + 1;
                        return (
                            <FaStar
                                key={index}
                                className="star"
                                color={ratingValue <= (hover || rating) ? '#ffc107' : '#e4e5e9'}
                                size={30}
                                onClick={() => setRating(ratingValue)}
                                onMouseEnter={() => setHover(ratingValue)}
                                onMouseLeave={() => setHover(null)}
                            />
                        );
                      })}
                    </div>
                    <textarea
                        placeholder="Введите ваш отзыв"
                        value={newReview}
                        onChange={(e) => setNewReview(e.target.value)}
                    />
                    <button onClick={handleAddReview} className="add-review-button">
                      Оставить отзыв
                    </button>
                  </div>
              )}
            </>
        ) : (
            <p>Загрузка...</p>
        )}
        {message && <p className="message">{message}</p>}
      </div>
  );
};

export default ProductDetail;

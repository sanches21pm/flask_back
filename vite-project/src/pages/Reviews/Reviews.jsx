import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './Reviews.css';

const Reviews = () => {
  const { product_id } = useParams();
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    axios.get(`/products/${product_id}/reviews`).then(response => setReviews(response.data));
  }, [product_id]);

  return (
    <div className="reviews-container">
      <h2>Reviews</h2>
      <ul>
        {reviews.map(review => (
          <li key={review.id}>{review.content} - Rating: {review.rating}</li>
        ))}
      </ul>
    </div>
  );
};

export default Reviews;

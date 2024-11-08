import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './AddProduct.css';

const AddProduct = () => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [price, setPrice] = useState('');
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    // Функция для получения списка категорий
    const fetchCategories = async () => {
        try {
            const response = await axios.get('https://sanches.pythonanywhere.com/categories');
            setCategories(response.data);
        } catch (error) {
            console.error('Ошибка загрузки категорий:', error);
        }
    };

    useEffect(() => {
        fetchCategories();
    }, []);

    // Обработка отправки формы
    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('access_token');

        try {
            await axios.post(
                'https://sanches.pythonanywhere.com/products',
                {
                    name,
                    description,
                    price: parseFloat(price),
                    category_id: selectedCategory,
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );
            setMessage('Продукт успешно добавлен!');
            // Перенаправление на страницу со списком продуктов через 1.5 секунды
            setTimeout(() => navigate('/products'), 1500);
        } catch (error) {
            console.error('Ошибка при добавлении продукта:', error);
            setMessage('Не удалось добавить продукт. Попробуйте снова.');
        }
    };

    return (
        <div className="add-product-container">
            <h2>Добавить продукт</h2>
            {message && <p className="message">{message}</p>}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Название продукта"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Описание продукта"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Цена продукта"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    required
                />
                <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    required
                >
                    <option value="">Выберите категорию</option>
                    {categories.map((category) => (
                        <option key={category.id} value={category.id}>
                            {category.name}
                        </option>
                    ))}
                </select>
                <button type="submit">Добавить продукт</button>
            </form>
        </div>
    );
};

export default AddProduct;

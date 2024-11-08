import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './AddCategory.css';

const AddCategory = () => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('access_token');

        try {
            await axios.post(
                'https://sanches.pythonanywhere.com/categories',
                { name, description },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );
            setMessage('Категория успешно добавлена!');
            setTimeout(() => navigate('/categories'), 1500);
        } catch (error) {
            console.error('Ошибка при добавлении категории:', error);
            setMessage('Не удалось добавить категорию. Попробуйте снова.');
        }
    };

    return (
        <div className="add-category-container">
            <h2>Добавить категорию</h2>
            {message && <p>{message}</p>}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Название категории"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Описание категории"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                />
                <button type="submit">Добавить категорию</button>
            </form>
        </div>
    );
};

export default AddCategory;

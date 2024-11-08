// // // src/api.js
// // import axios from 'axios';

// // const API_URL = 'http://localhost:8000'; // Замените на URL вашего FastAPI сервера

// // // Регистрация пользователя
// // export const register = async (userData) => {
// //   try {
// //     const response = await axios.post(`${API_URL}/register`, userData);
// //     return response.data;
// //   } catch (error) {
// //     console.error('Registration error:', error);
// //     throw error;
// //   }
// // };

// // // Вход пользователя
// // export const login = async (credentials) => {
// //   try {
// //     const response = await axios.post(`${API_URL}/login`, credentials);
// //     return response.data;
// //   } catch (error) {
// //     console.error('Login error:', error);
// //     throw error;
// //   }
// // };



// // src/api.js
// import axios from "axios";

// const API_URL = "http://localhost:8000"; // Замените на URL вашего FastAPI-бэкенда

// // Регистрация пользователя
// export const registerUser = async (userData) => {
//   try {
//     const response = await axios.post(`${API_URL}/register`, userData);
//     return response.data;
//   } catch (error) {
//     throw error.response.data;
//   }
// };

// // Вход пользователя
// export const loginUser = async (credentials) => {
//   try {
//     const response = await axios.post(`${API_URL}/login`, credentials);
//     return response.data;
//   } catch (error) {
//     throw error.response.data;
//   }
// };

// // Получение профиля пользователя
// export const getUserProfile = async (token) => {
//   try {
//     const response = await axios.get(`${API_URL}/profile`, {
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     });
//     return response.data;
//   } catch (error) {
//     throw error.response.data;
//   }
// };

// // Обновление профиля пользователя
// export const updateUserProfile = async (token, updateData) => {
//   try {
//     const response = await axios.put(`${API_URL}/profile`, updateData, {
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     });
//     return response.data;
//   } catch (error) {
//     throw error.response.data;
//   }
// };

// // Удаление профиля пользователя
// export const deleteUserProfile = async (token) => {
//   try {
//     const response = await axios.delete(`${API_URL}/profile`, {
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     });
//     return response.data;
//   } catch (error) {
//     throw error.response.data;
//   }
// };



// src/api.js
import axios from "axios";
import config from "./config"; // Импорт конфигурации

const API_URL = config.apiBaseUrl; // Используем базовый URL из конфигурации

// Регистрация пользователя
export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/register`, userData);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// Вход пользователя
export const loginUser = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/login`, credentials);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// Получение профиля пользователя
export const getUserProfile = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// Обновление профиля пользователя
export const updateUserProfile = async (token, updateData) => {
  try {
    const response = await axios.put(`${API_URL}/profile`, updateData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// Удаление профиля пользователя
export const deleteUserProfile = async (token) => {
  try {
    const response = await axios.delete(`${API_URL}/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

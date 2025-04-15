// Api.js
import axios from "axios";

const Api = axios.create({
  baseURL: "http://localhost:8000",
});

// Interceptor para adicionar o token atualizado sempre
Api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken"); // <- mesma chave usada no login
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default Api;

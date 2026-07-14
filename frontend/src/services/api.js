import axios from "axios";

const api = axios.create({
    baseURL: "https://ai-industrial-safety-system.onrender.com",
});

export default api;
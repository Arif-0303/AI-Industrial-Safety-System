import api from "./api";

export const askAI = async (message) => {
  const response = await api.post("/chat/", {
    message: message,
  });

  return response.data;
};
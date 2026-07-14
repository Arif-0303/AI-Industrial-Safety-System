import api from "./api";

export const getSectors = async () => {
    const response = await api.get("/sectors/");
    return response.data;
};
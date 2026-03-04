import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const analyzeVideo = async (videoId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/analyze/${videoId}`, {
            params: { max_comments: 100 }
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || "Network Error");
    }
};

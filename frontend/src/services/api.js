import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export const authAPI = {
  signup: (email, password) =>
    apiClient.post("/auth/signup", { email, password }),
  login: (email, password) =>
    apiClient.post("/auth/login", { email, password }),
  verify: () => apiClient.post("/auth/verify"),
};

export const photoAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return apiClient.post("/photos/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  list: () => apiClient.get("/photos/list"),
  get: (photoId) => apiClient.get(`/photos/${photoId}`),
  delete: (photoId) => apiClient.delete(`/photos/${photoId}`),
  download: (photoId) =>
    apiClient.get(`/photos/${photoId}/file`, { responseType: "blob" }),
};

export const faceAPI = {
  process: (photoId) => apiClient.post(`/faces/process/${photoId}`),
  label: (faceId, personName) =>
    apiClient.put(`/faces/${faceId}/label`, { person_name: personName }),
  labelFace: (photoId, faceIndex, personName) =>
    apiClient.post(`/faces/label`, {
      photo_id: photoId,
      face_index: faceIndex,
      person_name: personName,
    }),
  getPerson: (personId) => apiClient.get(`/faces/person/${personId}`),
  getAllPeople: () => apiClient.get("/faces/people"),
};

export const chatAPI = {
  send: (message) => apiClient.post("/chat", { message }),
  getSuggestions: () => apiClient.get("/chat/suggestions"),
};

export const deliveryAPI = {
  sendEmail: (photoId, recipient) =>
    apiClient.post("/delivery/email", { photo_id: photoId, recipient }),
  sendWhatsApp: (photoId, recipient) =>
    apiClient.post("/delivery/whatsapp", { photo_id: photoId, recipient }),
  getHistory: () => apiClient.get("/delivery/history"),
  getStats: () => apiClient.get("/delivery/stats"),
};

export default apiClient;

// frontend/src/services/api.ts
import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response?.status, error.response?.data);
    return Promise.reject(error);
  },
);

export const fetchProjects = async () => {
  try {
    const response = await api.get("/projects/");
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Error fetching projects:", error);
    return [];
  }
};

export const fetchSkills = async () => {
  try {
    const response = await api.get("/skills/");
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Error fetching skills:", error);
    return [];
  }
};

export const fetchTestimonials = async () => {
  try {
    const response = await api.get("/testimonials/");
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Error fetching testimonials:", error);
    return [];
  }
};

export const fetchExperiences = async () => {
  try {
    const response = await api.get("/experiences/");
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Error fetching experiences:", error);
    return [];
  }
};

export const fetchEducation = async () => {
  try {
    const response = await api.get("/education/");
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Error fetching education:", error);
    return [];
  }
};

export const fetchBlogPosts = async () => {
  try {
    const response = await api.get("/blog/");
    const data = response.data;
    if (data && typeof data === "object") {
      if (Array.isArray(data.results)) return data.results;
      if (Array.isArray(data)) return data;
    }
    return [];
  } catch (error) {
    console.error("Error fetching blog posts:", error);
    return [];
  }
};

export const submitContact = async (data: any) => {
  const response = await api.post("/contact/", data);
  return response.data;
};

export default api;

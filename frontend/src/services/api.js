import axios from "axios";

const API = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000",
});

export const analyzeResumeRoles = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await API.post(
    "/resume/role-analysis",
    formData
  );

  return response.data;
};

export const getAnalysisHistory = async () => {
  const response = await API.get("/history");
  return response.data.history;
};

export const getAnalysis = async (id) => {
  const response = await API.get(
    `/history/${id}`
  );

  return response.data;
};

export const deleteAnalysis = async (id) => {
  const response = await API.delete(
    `/history/${id}`
  );

  return response.data;
};

export default API;
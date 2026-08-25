import axios from "axios";

const API = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    "https://career-lens-api-2obr.onrender.com",
});

export const analyzeResumeRoles = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  try {

    const response = await API.post(
      "/resume/role-analysis",
      formData
    );

    return response.data;

  } catch (error) {

    console.error(
      "Resume analysis API error:",
      error
    );

    console.error(
      "API URL:",
      API.defaults.baseURL
    );

    throw error;
  }
};


export const getAnalysisHistory = async () => {

  const response = await API.get(
    "/history"
  );

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
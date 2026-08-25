import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const analyzeResumeRoles = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await API.post(
    "/resume/role-analysis",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export default API;
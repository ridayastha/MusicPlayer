import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

export const fetchPatients = () => API.get("patients/");
export const createPatient = (data) => API.post("patients/", data);
export const deletePatient = (id) => API.delete(`patients/${id}/`);
export const updatePatient = (id, data) => API.put(`patients/${id}/`, data);

export const fetchMedicines = () => API.get("medicines/");
export const createMedicine = (data) => API.post("medicines/", data);
export const deleteMedicine = (id) => API.delete(`medicines/${id}/`);
export const updateMedicine = (id, data) => API.put(`medicines/${id}/`, data);

export default API;

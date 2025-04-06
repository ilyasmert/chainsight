// src/api/uploadApi.js
import axios from 'axios';

const UPLOAD_URL = 'http://127.0.0.1:8000/api/inventory/upload-table/';

export const uploadExcelFile = async (file, tableName, archivedBy = 'admin') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('tableName', tableName);
  formData.append('archivedBy', archivedBy);

  const response = await axios.post(UPLOAD_URL, formData);
  return response.data;
};

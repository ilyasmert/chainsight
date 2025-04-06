import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/inventory';

export const fetchReady = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/ready/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching ready data:', error);
    throw error;
  }
};

export const fetchAtpStock = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/atp-stock/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching ATP stock data:', error);
    throw error;
  }
};

export const fetchIntransit = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/intransit/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching intransit data:', error);
    throw error;
  }
};

export const fetchSales = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/sales/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching sales data:', error);
    throw error;
  }
};

export const fetchToBeProduced = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/to-be-produced/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching To Be Produced data:', error);
    throw error;
  }
};

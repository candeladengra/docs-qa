import axios from 'axios';
import { Document, QueryResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const documentsApi = {
  list: async (): Promise<Document[]> => {
    const response = await api.get<Document[]>('/api/documents/');
    return response.data;
  },

  upload: async (file: File, title: string): Promise<Document> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);

    const response = await api.post<Document>('/api/documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/documents/${id}/`);
  },

  query: async (question: string): Promise<QueryResponse> => {
    const response = await api.post<QueryResponse>('/api/documents/query/', {
      question,
    });
    return response.data;
  },
};

export default api;

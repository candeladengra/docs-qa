export interface Document {
  id: number;
  title: string;
  file: string;
  status: 'processing' | 'ready' | 'failed';
  error_message?: string;
  page_count?: number;
  created_at: string;
  updated_at: string;
}

export interface Source {
  content: string;
  document_name: string;
  page_number: number;
  document_id: number;
}

export interface QueryResponse {
  answer: string;
  sources: Source[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: Date;
}

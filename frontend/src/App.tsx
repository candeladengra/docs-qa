import { useState, useEffect } from 'react';
import './App.css';
import DocumentUpload from './components/DocumentUpload';
import DocumentList from './components/DocumentList';
import ChatInterface from './components/ChatInterface';
import { Document } from './types';
import { documentsApi } from './services/api';

function App() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDocuments = async () => {
    try {
      const docs = await documentsApi.list();
      setDocuments(docs);
    } catch (error) {
      console.error('Failed to fetch documents:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
    const interval = setInterval(fetchDocuments, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleUploadSuccess = () => {
    fetchDocuments();
  };

  const handleDelete = async (id: number) => {
    try {
      await documentsApi.delete(id);
      fetchDocuments();
    } catch (error) {
      console.error('Failed to delete document:', error);
      alert('Failed to delete document');
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>📚 Docs Q&A</h1>
        <p>Upload PDFs and ask questions in natural language</p>
      </header>
      
      <main className="main-content">
        <div className="sidebar">
          <DocumentUpload onUploadSuccess={handleUploadSuccess} />
          <DocumentList
            documents={documents}
            loading={loading}
            onDelete={handleDelete}
          />
        </div>
        
        <div className="chat-area">
          <ChatInterface hasDocuments={documents.some(d => d.status === 'ready')} />
        </div>
      </main>
    </div>
  );
}

export default App;

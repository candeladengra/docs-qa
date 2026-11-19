import { Document } from '../types';
import './DocumentList.css';

interface Props {
  documents: Document[];
  loading: boolean;
  onDelete: (id: number) => void;
}

function DocumentList({ documents, loading, onDelete }: Props) {
  const getStatusBadge = (status: string) => {
    const badges = {
      processing: { text: 'Processing', class: 'status-processing' },
      ready: { text: 'Ready', class: 'status-ready' },
      failed: { text: 'Failed', class: 'status-failed' },
    };
    const badge = badges[status as keyof typeof badges] || badges.processing;
    return <span className={`status-badge ${badge.class}`}>{badge.text}</span>;
  };

  if (loading && documents.length === 0) {
    return (
      <div className="document-list">
        <h2>Documents</h2>
        <div className="loading">Loading documents...</div>
      </div>
    );
  }

  return (
    <div className="document-list">
      <h2>Documents ({documents.length})</h2>
      {documents.length === 0 ? (
        <div className="empty-state">
          <p>No documents yet</p>
          <p className="hint">Upload a PDF to get started</p>
        </div>
      ) : (
        <div className="documents">
          {documents.map((doc) => (
            <div key={doc.id} className="document-item">
              <div className="document-header">
                <span className="document-icon">📄</span>
                <div className="document-info">
                  <div className="document-title">{doc.title}</div>
                  <div className="document-meta">
                    {doc.page_count && `${doc.page_count} pages`}
                  </div>
                </div>
                <button
                  className="delete-button"
                  onClick={() => onDelete(doc.id)}
                  title="Delete document"
                >
                  ×
                </button>
              </div>
              <div className="document-footer">
                {getStatusBadge(doc.status)}
                {doc.status === 'failed' && doc.error_message && (
                  <div className="error-message">{doc.error_message}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default DocumentList;

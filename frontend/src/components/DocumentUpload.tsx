import { useState, ChangeEvent, FormEvent } from 'react';
import { documentsApi } from '../services/api';
import './DocumentUpload.css';

interface Props {
  onUploadSuccess: () => void;
}

function DocumentUpload({ onUploadSuccess }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type === 'application/pdf') {
        setFile(selectedFile);
      } else {
        alert('Please select a PDF file');
      }
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    try {
      const title = file.name.replace('.pdf', '');
      await documentsApi.upload(file, title);
      setFile(null);
      onUploadSuccess();
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="document-upload">
      <h2>Upload Document</h2>
      <form onSubmit={handleSubmit}>
        <div className="file-input-wrapper">
          <input
            id="file-input"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={uploading}
          />
          {file && (
            <div className="file-info">
              <span className="file-icon">📄</span>
              <span className="file-name">{file.name}</span>
            </div>
          )}
        </div>
        <button
          type="submit"
          disabled={!file || uploading}
          className="upload-button"
        >
          {uploading ? 'Uploading...' : 'Upload PDF'}
        </button>
      </form>
    </div>
  );
}

export default DocumentUpload;

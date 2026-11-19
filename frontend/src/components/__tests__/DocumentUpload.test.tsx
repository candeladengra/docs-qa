import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import DocumentUpload from '../DocumentUpload';

describe('DocumentUpload', () => {
  it('renders upload form', () => {
    const onUploadSuccess = vi.fn();
    render(<DocumentUpload onUploadSuccess={onUploadSuccess} />);
    
    expect(screen.getByText('Upload Document')).toBeInTheDocument();
    expect(screen.getByText('Upload PDF')).toBeInTheDocument();
  });

  it('upload button is disabled when no file selected', () => {
    const onUploadSuccess = vi.fn();
    render(<DocumentUpload onUploadSuccess={onUploadSuccess} />);
    
    const button = screen.getByRole('button', { name: /upload pdf/i });
    expect(button).toBeDisabled();
  });

  it('shows file name when file is selected', () => {
    const onUploadSuccess = vi.fn();
    render(<DocumentUpload onUploadSuccess={onUploadSuccess} />);
    
    const file = new File(['pdf content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/file/i) || document.querySelector('input[type="file"]');
    
    if (input) {
      fireEvent.change(input, { target: { files: [file] } });
      expect(screen.getByText('test.pdf')).toBeInTheDocument();
    }
  });
});

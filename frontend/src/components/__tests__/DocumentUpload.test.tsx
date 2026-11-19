import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
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
});

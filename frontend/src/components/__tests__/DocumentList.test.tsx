import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import DocumentList from '../DocumentList';
import { Document } from '../../types';

describe('DocumentList', () => {
  it('shows loading state', () => {
    render(<DocumentList documents={[]} loading={true} onDelete={vi.fn()} />);
    expect(screen.getByText('Loading documents...')).toBeInTheDocument();
  });

  it('shows empty state when no documents', () => {
    render(<DocumentList documents={[]} loading={false} onDelete={vi.fn()} />);
    expect(screen.getByText('No documents yet')).toBeInTheDocument();
  });

  it('renders document list', () => {
    const docs: Document[] = [
      {
        id: 1,
        title: 'Test Doc',
        file: 'test.pdf',
        status: 'ready',
        page_count: 5,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];

    render(<DocumentList documents={docs} loading={false} onDelete={vi.fn()} />);
    
    expect(screen.getByText('Test Doc')).toBeInTheDocument();
    expect(screen.getByText('5 pages')).toBeInTheDocument();
    expect(screen.getByText('Ready')).toBeInTheDocument();
  });

  it('shows status badges correctly', () => {
    const docs: Document[] = [
      {
        id: 1,
        title: 'Processing Doc',
        file: 'test.pdf',
        status: 'processing',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        id: 2,
        title: 'Ready Doc',
        file: 'test2.pdf',
        status: 'ready',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];

    render(<DocumentList documents={docs} loading={false} onDelete={vi.fn()} />);
    
    expect(screen.getByText('Processing')).toBeInTheDocument();
    expect(screen.getByText('Ready')).toBeInTheDocument();
  });
});

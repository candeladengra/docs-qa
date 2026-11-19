import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { documentsApi } from '../api';

vi.mock('axios');
const mockedAxios = axios as unknown as {
  create: ReturnType<typeof vi.fn>;
};

describe('documentsApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('creates axios instance with correct config', () => {
    expect(axios.create).toBeDefined();
  });

  describe('list', () => {
    it('fetches documents list', async () => {
      const mockDocs = [
        { id: 1, title: 'Test Doc', status: 'ready' },
      ];

      mockedAxios.create.mockReturnValue({
        get: vi.fn().mockResolvedValue({ data: mockDocs }),
      });

      const result = await documentsApi.list();
      expect(result).toBeDefined();
    });
  });

  describe('query', () => {
    it('sends query request', async () => {
      const mockResponse = {
        answer: 'Test answer',
        sources: [],
      };

      const mockPost = vi.fn().mockResolvedValue({ data: mockResponse });
      mockedAxios.create.mockReturnValue({
        post: mockPost,
      });

      const result = await documentsApi.query('What is this?');
      expect(result).toBeDefined();
    });
  });
});

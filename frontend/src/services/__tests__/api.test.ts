import { describe, it, expect } from 'vitest';
import { documentsApi } from '../api';

describe('documentsApi', () => {
  it('exports api methods', () => {
    expect(documentsApi).toBeDefined();
    expect(documentsApi.list).toBeDefined();
    expect(documentsApi.upload).toBeDefined();
    expect(documentsApi.delete).toBeDefined();
    expect(documentsApi.query).toBeDefined();
  });
});

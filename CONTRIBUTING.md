# Contributing to Docs Q&A

Thank you for your interest in contributing!

## Development Setup

1. Fork and clone the repository
2. Follow setup instructions in [SETUP.md](./SETUP.md)
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Run tests: `make test`
6. Commit with clear messages
7. Push and create a Pull Request

## Code Style

### Backend (Python)
- Follow PEP 8
- Use Black for formatting: `black .`
- Run flake8: `flake8 . --max-line-length=100`

### Frontend (TypeScript)
- Follow TypeScript best practices
- Use ESLint: `npm run lint`
- Format with Prettier if available

## Testing

All new features should include tests:
- Backend: pytest tests in `apps/*/tests/`
- Frontend: Vitest tests in `**/__tests__/`

Run tests before submitting:
```bash
make test
```

## Pull Request Process

1. Update README.md if needed
2. Ensure all tests pass
3. Update documentation
4. Link related issues
5. Request review

## Questions?

Open an issue for discussion!

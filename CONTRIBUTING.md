# Contributing to TE-explico

Thank you for your interest in contributing to TE-explico! This document provides guidelines for contributing to this project.

## Important Notice

This project contains proprietary technology under TOKRAGGCORP. Please review [PATENTS.md](PATENTS.md) before contributing.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Install dependencies
npm install
cd frontend && npm install
cd ../backend && npm install
cd ../ai && pip install -r ../requirements.txt

# Start development environment
docker-compose up -d

# Run tests
npm test
```

## Code Standards

### TypeScript/JavaScript
- Use TypeScript for type safety
- Follow ESLint configuration
- Write unit tests for all new features
- Maintain 80%+ code coverage

### Python
- Follow PEP 8 style guide
- Use type hints
- Write pytest tests
- Document all functions

### Git Commit Messages
- Use conventional commits format
- Be descriptive and concise
- Reference issue numbers when applicable

Example:
```
feat(backend): add user authentication
fix(ai): resolve memory leak in inference
docs(readme): update deployment instructions
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Testing Requirements

- Unit tests for all new code
- Integration tests for API changes
- E2E tests for UI changes
- Performance tests for optimization changes

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## Questions?

Contact: dev@tokraggcorp.com

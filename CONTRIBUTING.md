# Contributing to TE-explico

Welcome to the TE-explico project! We appreciate your interest in contributing to our multi-platform AI learning assistant system.

## 🎯 Project Vision

TE-explico (OmniMaestro Core) is a contextual learning copilot designed to assist users in learning software through an AI-powered layer that operates across multiple platforms (Windows, macOS, Linux, Android).

## 🏗️ Architecture Overview

The project follows a modular architecture:

- **`/core`** - Core business logic and shared utilities
- **`/frontend`** - User-facing applications (web, mobile, desktop)
- **`/backend`** - Backend services, APIs, and data processing
- **`/ai`** - AI/ML models, training scripts, and inference engines
- **`/infra`** - Infrastructure as code, deployment configurations
- **`/tests`** - Comprehensive test suites
- **`/docs`** - Technical and user documentation

## 🚀 Getting Started

### Prerequisites

Depending on the component you're working on, you may need:

- **Python 3.10+** (for AI/ML and backend services)
- **Node.js 18+** (for web frontend)
- **Flutter/Dart** (for mobile applications)
- **Go 1.21+** (for high-performance backend services)
- **Docker** (for containerized development)

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/TE-explico.git
   cd TE-explico
   ```

2. **Install Dependencies** (module-specific)
   ```bash
   # For backend services
   cd backend
   pip install -r requirements.txt
   
   # For frontend
   cd frontend/web
   npm install
   ```

3. **Run Tests**
   ```bash
   # From project root
   ./scripts/run-tests.sh
   ```

## 📝 Contribution Guidelines

### Code Standards

1. **Code Quality**
   - Write clean, maintainable, and well-documented code
   - Follow language-specific style guides (PEP 8 for Python, Airbnb for JavaScript, etc.)
   - Ensure all tests pass before submitting PR
   - Maintain test coverage above 80%

2. **Commit Messages**
   Follow the conventional commits specification:
   ```
   <type>(<scope>): <subject>
   
   <body>
   
   <footer>
   ```
   
   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   
   Example:
   ```
   feat(ai): add multimodal input processing for screen captures
   
   Implements vision model integration to analyze user screenshots
   and provide contextual assistance based on visual input.
   
   Closes #123
   ```

3. **Branch Naming**
   - Feature: `feature/short-description`
   - Bugfix: `fix/issue-number-description`
   - Hotfix: `hotfix/critical-issue`
   - Documentation: `docs/what-changed`

### Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write code following project standards
   - Add/update tests as needed
   - Update documentation if necessary

3. **Test Thoroughly**
   - Run unit tests
   - Run integration tests
   - Test manually if UI changes are involved

4. **Submit Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure CI/CD checks pass
   - Request review from appropriate code owners

5. **Code Review**
   - Address feedback promptly
   - Keep discussions professional and constructive
   - Be open to suggestions and improvements

### Testing Requirements

- **Unit Tests**: All new functions/methods must have unit tests
- **Integration Tests**: API endpoints and module interactions require integration tests
- **E2E Tests**: Critical user flows must have end-to-end tests
- **Performance Tests**: High-traffic components need performance benchmarks

### Security Considerations

- Never commit secrets, API keys, or credentials
- Follow OWASP security best practices
- Report security vulnerabilities privately to maintainers
- Use dependency scanning tools before adding new dependencies

## 🔍 Code Review Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New code has appropriate test coverage
- [ ] Documentation is updated
- [ ] No hardcoded credentials or secrets
- [ ] Performance implications considered
- [ ] Backward compatibility maintained (if applicable)
- [ ] CI/CD pipeline passes

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Celebrate successes and learn from failures
- Focus on the problem, not the person

## 📚 Resources

- [Architecture Documentation](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Development Setup Guide](docs/dev-setup.md)
- [Testing Guide](docs/testing.md)

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. Clear description of the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, versions, etc.)
6. Screenshots or logs (if applicable)

## 💡 Suggesting Enhancements

We welcome feature suggestions! Please:

1. Check if the feature already exists or is planned
2. Provide clear use cases
3. Explain the expected benefits
4. Consider implementation complexity
5. Be open to alternative approaches

## 📞 Getting Help

- **Issues**: GitHub Issues for bugs and feature requests
- **Discussions**: GitHub Discussions for general questions
- **Documentation**: Check `/docs` folder for guides

## 🎓 Learning Path for Contributors

New to the project? Start here:

1. Read the README and architecture docs
2. Set up your development environment
3. Run the test suite to understand the codebase
4. Pick a "good first issue" to work on
5. Join discussions to understand project direction

## ⚡ TOKRAGGCORP Directive: 100x100 + 1

We strive for excellence in every contribution:

- **100%** code quality
- **100%** test coverage for critical paths
- **+1** innovation and continuous improvement

Quality over quantity. Precision over speed. Excellence as standard.

---

Thank you for contributing to TE-explico! Together, we're building the future of contextual learning assistance.

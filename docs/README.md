# Documentation

## Overview

The `/docs` directory contains comprehensive technical and user documentation for the TE-explico system.

## Structure

```
docs/
├── architecture/        # System architecture documentation
├── api/                 # API reference and specifications
├── guides/              # User and developer guides
├── runbooks/            # Operational runbooks
├── security/            # Security policies and procedures
└── README.md
```

## Documentation Index

### Architecture
- [System Architecture Overview](architecture/system-overview.md)
- [Component Design](architecture/components.md)
- [Data Flow](architecture/data-flow.md)
- [Security Architecture](architecture/security.md)

### API Reference
- [REST API Documentation](api/rest-api.md)
- [WebSocket API](api/websocket.md)
- [Authentication](api/authentication.md)

### Developer Guides
- [Development Setup](guides/dev-setup.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Code Style Guide](guides/code-style.md)
- [Testing Guide](guides/testing.md)

### User Guides
- [Getting Started](guides/getting-started.md)
- [User Manual](guides/user-manual.md)
- [FAQ](guides/faq.md)

### Operations
- [Deployment Guide](runbooks/deployment.md)
- [Incident Response](runbooks/incident-response.md)
- [Monitoring](runbooks/monitoring.md)

## Contributing to Documentation

1. Follow Markdown best practices
2. Include code examples where applicable
3. Keep documentation up-to-date with code changes
4. Use clear, concise language
5. Add diagrams for complex concepts

## Building Documentation

```bash
# Generate API docs
npm run docs:api

# Build static site (if using docs framework)
npm run docs:build

# Serve locally
npm run docs:serve
```

## Status

🚧 **Under Construction** - Documentation is being created to support system development and operations.

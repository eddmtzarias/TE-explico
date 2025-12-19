# Tests

## Overview

The `/tests` directory contains comprehensive test suites for the TE-explico system, ensuring code quality, reliability, and performance across all modules.

## Structure

```
tests/
├── unit/                # Unit tests for individual components
├── integration/         # Integration tests for module interactions
├── e2e/                 # End-to-end tests for user flows
├── performance/         # Load and stress tests
├── security/            # Security and penetration tests
├── fixtures/            # Test data and fixtures
├── utils/               # Test utilities and helpers
└── README.md
```

## Testing Strategy

### Test Pyramid
```
        /\
       /E2E\        (Few, slow, high-level)
      /------\
     /Integr.\     (More, medium speed)
    /----------\
   /   Unit     \   (Many, fast, low-level)
  /--------------\
```

### Coverage Goals
- **Overall**: > 80% code coverage
- **Critical Paths**: > 95% coverage
- **Core Module**: > 90% coverage
- **UI Components**: > 75% coverage

## Test Categories

### 1. Unit Tests

Test individual functions, methods, and classes in isolation.

**Example Structure:**
```
unit/
├── core/
│   ├── services/
│   │   └── test_context_service.py
│   └── utils/
│       └── test_validators.py
├── backend/
│   └── api/
│       └── test_auth.py
└── ai/
    └── models/
        └── test_vision_model.py
```

**Running Unit Tests:**
```bash
# Python
pytest tests/unit/

# JavaScript
npm run test:unit

# Go
go test ./tests/unit/...
```

### 2. Integration Tests

Test interactions between modules, services, and external dependencies.

**Example Scenarios:**
- API endpoint to database operations
- Frontend to backend communication
- AI service integration with backend
- Cache layer interactions

**Running Integration Tests:**
```bash
# Requires services to be running
docker-compose -f docker/docker-compose.test.yml up -d

# Run tests
pytest tests/integration/
npm run test:integration

# Cleanup
docker-compose -f docker/docker-compose.test.yml down
```

### 3. End-to-End (E2E) Tests

Test complete user flows from frontend to backend.

**Tools:**
- **Web**: Playwright / Cypress
- **Mobile**: Detox / Appium
- **Desktop**: Playwright / Spectron

**Example Scenarios:**
- User authentication flow
- Screenshot capture and analysis
- Context-aware response generation
- Multi-modal input processing

**Running E2E Tests:**
```bash
# Start full application stack
docker-compose up -d

# Run E2E tests
npm run test:e2e

# Headless mode
npm run test:e2e:ci
```

### 4. Performance Tests

Load testing, stress testing, and performance benchmarking.

**Tools:**
- **Load Testing**: k6, Locust
- **Profiling**: py-spy, Node.js profiler
- **Database**: pgbench

**Scenarios:**
```
performance/
├── load_tests/
│   ├── api_load_test.js        # API endpoint load testing
│   ├── ai_inference_load.py    # AI service stress testing
│   └── concurrent_users.js     # Multi-user scenarios
└── benchmarks/
    ├── vision_model_bench.py   # Model inference benchmarks
    └── db_query_bench.sql      # Database query performance
```

**Running Performance Tests:**
```bash
# Load test with k6
k6 run tests/performance/load_tests/api_load_test.js

# Python load test
locust -f tests/performance/load_tests/ai_inference_load.py

# Benchmark AI model
python tests/performance/benchmarks/vision_model_bench.py
```

**Performance Targets:**
- API response time: p95 < 200ms
- AI inference: p95 < 500ms
- Database queries: p95 < 50ms
- Concurrent users: > 1000 users

### 5. Security Tests

Automated security testing and vulnerability scanning.

**Tools:**
- **SAST**: Bandit (Python), ESLint security plugin (JS)
- **DAST**: OWASP ZAP
- **Dependency Scanning**: Snyk, npm audit
- **Secret Scanning**: TruffleHog, git-secrets

**Test Categories:**
```
security/
├── sast/                # Static analysis
├── dast/                # Dynamic analysis
├── dependency/          # Dependency vulnerabilities
├── penetration/         # Pen testing scripts
└── compliance/          # Compliance checks
```

**Running Security Tests:**
```bash
# SAST
bandit -r backend/
npm audit

# Dependency check
snyk test

# OWASP ZAP scan
./scripts/security-scan.sh
```

## Test Data & Fixtures

### Fixtures Organization
```
fixtures/
├── database/
│   ├── seed_data.sql        # Database seed data
│   └── test_users.json      # Test user accounts
├── screenshots/
│   ├── sample_ui_*.png      # Sample screenshots for vision tests
│   └── annotations.json     # Ground truth annotations
└── responses/
    └── mock_ai_responses.json
```

### Test Data Management
- Use factories for generating test data
- Mock external API responses
- Anonymize production data for testing
- Clean up test data after execution

## Continuous Integration

### CI Pipeline Tests
```yaml
# .github/workflows/test.yml
on: [push, pull_request]
jobs:
  unit-tests:
    - Run linting
    - Run unit tests
    - Upload coverage
  
  integration-tests:
    - Start services
    - Run integration tests
    - Collect logs
  
  e2e-tests:
    - Deploy to staging
    - Run E2E suite
    - Capture screenshots
  
  security-scan:
    - SAST analysis
    - Dependency scan
    - Container scanning
```

### Test Reports
- Coverage reports: Codecov / Coveralls
- Test results: JUnit XML format
- Performance reports: HTML dashboards
- Security reports: SARIF format

## Best Practices

### Writing Tests
1. **Arrange-Act-Assert (AAA)** pattern
2. **Descriptive test names**: `test_should_return_error_when_invalid_input()`
3. **One assertion per test** (when possible)
4. **Test isolation**: No dependencies between tests
5. **Fast execution**: Mock slow operations

### Test Maintenance
- Keep tests simple and readable
- Refactor tests along with production code
- Remove flaky tests or fix them
- Update tests when requirements change

### Code Review
- All PRs must include tests
- Review test coverage reports
- Verify test quality, not just quantity

## Test Utilities

Shared test utilities in `/tests/utils/`:
```python
# tests/utils/helpers.py
def create_test_user(**kwargs):
    """Factory for creating test users"""
    pass

def mock_ai_response(context):
    """Generate mock AI responses"""
    pass

def assert_api_response(response, expected_status=200):
    """Common API response assertions"""
    pass
```

## Debugging Tests

```bash
# Run specific test
pytest tests/unit/core/test_context_service.py::test_context_creation

# Run with verbose output
pytest -vv tests/

# Run with debugger
pytest --pdb tests/unit/

# Show print statements
pytest -s tests/
```

## Performance Monitoring

Track test execution time:
```bash
# pytest with duration report
pytest --durations=10

# npm test with timing
npm test -- --verbose
```

## Status

🚧 **Under Construction** - Test infrastructure is being established with focus on comprehensive coverage and automation.

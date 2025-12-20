# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: security@tokraggcorp.com

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

## Security Measures

Our application implements the following security measures:

### OWASP Top 10 Protection
1. ✅ Broken Access Control - JWT authentication + RBAC
2. ✅ Cryptographic Failures - HTTPS, encrypted secrets
3. ✅ Injection - Input validation, parameterized queries
4. ✅ Insecure Design - Security-first architecture
5. ✅ Security Misconfiguration - Helmet.js, secure headers
6. ✅ Vulnerable Components - Automated scanning
7. ✅ Authentication Failures - JWT + rate limiting
8. ✅ Software Integrity - Code signing, SBOM
9. ✅ Logging Failures - Comprehensive monitoring
10. ✅ SSRF - URL validation, whitelist

### Additional Security
- Rate limiting (100 requests/15 minutes)
- DDoS protection
- Input sanitization
- CORS configuration
- Security headers (CSP, X-Frame-Options, etc.)
- Automated vulnerability scanning (Trivy, Snyk, CodeQL)
- Regular dependency updates

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported versions
4. Release new security fix versions as soon as possible

## Comments on this Policy

If you have suggestions on how this process could be improved, please submit a pull request.

---

**Last Updated**: December 2025  
**Contact**: security@tokraggcorp.com

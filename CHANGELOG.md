# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-11-27

### Added
- **Backend**: FastAPI application with Auth, Family/Profile CRUD, Policy API, and Event Logging.
- **Frontend**: React PWA Dashboard for managing families and viewing logs.
- **Resolver**: Go-based DNS resolver with policy enforcement and blocking logic.
- **Extension**: Chrome Extension (Manifest V3) for browser-level enforcement and block page redirection.
- **Docs**: Router setup guide, Privacy Policy (NDPA/NDPR), and API Reference.
- **Infrastructure**: Docker Compose setup for local development.
- **CI/CD**: GitHub Actions workflow for build and test.

### Fixed
- **Resolver**: Fixed Docker build by disabling CGO and installing git.
- **Backend**: Added demo user seeding (`user@db`) and fixed CORS for local development.

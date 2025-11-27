# NIRA-X-Guardian

NIRA-X-Guardian is a DNS-level parental control product MVP. It includes a PWA dashboard, a managed DNS resolver, a Chrome extension, and a backend API.

## Features

- **PWA Dashboard**: Manage family profiles, blocklists, and view logs.
- **DNS Resolver**: Recursive resolver that blocks domains based on family policy.
- **Chrome Extension**: Enforces policy in the browser and handles block page redirection.
- **Block Page**: Custom branded block page with override request functionality.

## Architecture

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + PostgreSQL
- **Resolver**: Go (miekg/dns)
- **Extension**: Chrome WebExtension (Manifest V3)

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js (for local frontend dev)
- Go (for local resolver dev)
- Python 3.11+ (for local backend dev)

### Run with Docker Compose

1.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
2.  Start services:
    ```bash
    docker-compose up --build
    ```
3.  Access the services:
    - **Dashboard**: http://localhost:3000
    - **Block Page**: http://localhost:8000/blockpage/test-family (via backend for now)
    - **Resolver**: localhost:5353 (UDP/TCP)

### Development Commands

See individual directories for specific development instructions.

- `frontend/README.md`
- `backend/README.md`
- `resolver/README.md`
- `extension/README.md`

## Security & Ops

- **Secrets**: Do NOT store secrets in the repo. Use `.env` for local dev and secure environment variables in production.
- **TLS**: Use a reverse proxy (e.g., Nginx, Traefik) with Let's Encrypt or Cloudflare for TLS termination in production.
- **Uninstall Protection**: This MVP relies on network-level blocking (DNS). For robust protection on unmanaged devices, MDM or router-level enforcement is required.

## License

Proprietary / Hackathon MVP

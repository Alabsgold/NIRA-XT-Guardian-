# API Reference

Base URL: `http://localhost:8000`

## Auth

### POST /api/auth/register
Register a new parent account.
- **Body**: `{"email": "user@example.com", "password": "securepassword"}`

### POST /api/auth/token
Login to get access token.
- **Body (Form Data)**: `username=user@example.com&password=securepassword`
- **Response**: `{"access_token": "...", "token_type": "bearer"}`

## Policy

### GET /api/policy/families
List all families.
- **Header**: `Authorization: Bearer <token>`

### POST /api/policy/families
Create a family.
- **Header**: `Authorization: Bearer <token>`
- **Body**: `{"name": "Home"}`

### GET /api/policy/{family_id}
Get public policy (used by Resolver/Extension).
- **Response**: `{"blocklist": ["bad.com"], "block_adult": true, ...}`

### POST /api/policy/families/{family_id}/blocklist
Add domain to blocklist.
- **Header**: `Authorization: Bearer <token>`
- **Body**: `{"domain": "example.com", "entry_type": "block"}`

## Events

### POST /api/events/
Log a blocking event (Internal/Resolver).
- **Body**: `{"domain": "bad.com", "blocked": true, "reason": "Policy", "client_ip": "1.2.3.4", "family_id": 1}`

### GET /api/events/families/{family_id}
Get recent events.
- **Header**: `Authorization: Bearer <token>`

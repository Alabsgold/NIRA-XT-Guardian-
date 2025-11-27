# MVP Acceptance Checklist

## 1. PWA Dashboard
- [ ] Run `docker-compose up --build`
- [ ] Visit `http://localhost:3000`
- [ ] Register a new account
- [ ] Create a family "Home"
- [ ] Add `example.com` to blocklist

## 2. Backend API
- [ ] Verify `http://localhost:8000/docs` loads Swagger UI
- [ ] Verify `/api/policy/{id}` returns JSON

## 3. DNS Resolver
- [ ] Run `dig @127.0.0.1 -p 5353 example.com`
- [ ] Expected: NXDOMAIN (if blocked) or A record
- [ ] Verify event logged in Dashboard "Logs" tab

## 4. Chrome Extension
- [ ] Load unpacked extension
- [ ] Enter Family ID
- [ ] Visit `example.com` -> Should redirect to Block Page

## 5. Block Page
- [ ] Visit `http://localhost:8000/blockpage/1?domain=example.com`
- [ ] Click "Request Override" -> Verify alert

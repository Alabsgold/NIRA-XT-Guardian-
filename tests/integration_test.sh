#!/bin/bash

echo "Starting Integration Test..."

# Ensure services are up
# docker-compose up -d

# Wait for services
sleep 5

# 1. Register User & Get Token
echo "Registering user..."
curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "integration@test.com", "password": "password"}'

echo "Logging in..."
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token \
  -d "username=integration@test.com&password=password" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"

# 2. Create Family
echo "Creating Family..."
FAMILY_ID=$(curl -s -X POST http://localhost:8000/api/policy/families \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Family"}' | grep -o '"id":[0-9]*' | cut -d':' -f2)

echo "Family ID: $FAMILY_ID"

# 3. Add Block
echo "Blocking example.com..."
curl -s -X POST http://localhost:8000/api/policy/families/$FAMILY_ID/blocklist \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "entry_type": "block"}'

# 4. Test DNS (Simulate via dig or just check policy API)
# Note: Real DNS test requires dig and binding to port.
# We will just verify policy API returns the block.

echo "Verifying Policy..."
POLICY=$(curl -s http://localhost:8000/api/policy/$FAMILY_ID)
echo $POLICY

if [[ $POLICY == *"example.com"* ]]; then
  echo "SUCCESS: example.com found in policy."
else
  echo "FAILURE: example.com not found in policy."
  exit 1
fi

echo "Integration Test Complete."

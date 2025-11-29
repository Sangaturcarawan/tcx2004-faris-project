# backend/tests/manual/test_user_story_1_auth.sh

#!/bin/bash
# User Story 1: Signup, Login, Logout

BASE="http://127.0.0.1:8000"

echo "[TEST] Creating test user..."
curl -s -X POST "$BASE/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"alice"}' > /dev/null

echo "[TEST] Logging in..."
TOKEN=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"alice"}' | jq -r '.access_token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "Login failed"
  exit 1
fi

echo "[TEST] Calling /me"
curl -s -X GET "$BASE/me" -H "Authorization: Bearer $TOKEN" | jq

exit 0

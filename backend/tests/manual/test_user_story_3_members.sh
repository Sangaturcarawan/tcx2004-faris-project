# backend/tests/manual/test_user_story_3_group_members.sh

#!/bin/bash
BASE="http://127.0.0.1:8000"

echo "[TEST] Logging in as Alice..."
TOKEN_A=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"alice"}' | jq -r '.access_token')

echo "[TEST] Signing up Bob..."
curl -s -X POST "$BASE/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"bob@test.com","password":"bob"}' > /dev/null

echo "[TEST] Logging in Bob..."
TOKEN_B=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"bob@test.com","password":"bob"}' | jq -r '.access_token')

# Create group
GROUP_ID=$(curl -s -X POST "$BASE/groups/" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"name":"Group Members Test"}' | jq -r '.id')

echo "[TEST] Alice adds Bob..."
curl -s -X POST "$BASE/groups/$GROUP_ID/members/" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"user_id":2}' | jq

echo "[TEST] Listing members..."
curl -s -X GET "$BASE/groups/$GROUP_ID/members/" \
  -H "Authorization: Bearer $TOKEN_A" | jq

exit 0

#backend/tests/manual/test_user_story_2_groups.sh

#!/bin/bash
BASE="http://127.0.0.1:8000"

echo "[TEST] Logging in as Alice..."
TOKEN=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"alice"}' | jq -r '.access_token')

echo "[TEST] Creating group..."
GROUP=$(curl -s -X POST "$BASE/groups/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Group"}')

GROUP_ID=$(echo "$GROUP" | jq -r '.id')

echo "[TEST] Retrieving group..."
curl -s -X GET "$BASE/groups/$GROUP_ID" \
  -H "Authorization: Bearer $TOKEN" | jq

exit 0


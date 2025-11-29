# backend/tests/manual/test_user_story_4_invitations.sh

#!/bin/bash
BASE="http://127.0.0.1:8000"

echo "[TEST] Logging in as Alice..."
TOKEN_A=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"alice"}' | jq -r '.access_token')

echo "[TEST] Logging in Bob..."
TOKEN_B=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"bob@test.com","password":"bob"}' | jq -r '.access_token')

echo "[TEST] Creating new invitation test group..."
GROUP_ID=$(curl -s -X POST "$BASE/groups/" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"name":"Invitation Test"}' | jq -r '.id')

echo "[TEST] Alice invites Bob..."
INVITE=$(curl -s -X POST "$BASE/invitations/groups/$GROUP_ID/invite" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"email":"bob@test.com"}')

INV_ID=$(echo "$INVITE" | jq -r '.id')

echo "[TEST] Bob views received invitations..."
curl -s -X GET "$BASE/invitations/received" \
  -H "Authorization: Bearer $TOKEN_B" | jq

echo "[TEST] Bob accepts invitation..."
curl -s -X POST "$BASE/invitations/$INV_ID/accept" \
  -H "Authorization: Bearer $TOKEN_B" | jq

exit 0

# backend/tests/manual/test_user_story_5_expenses.sh

#!/bin/bash
# User Story 5 — Audit Trail

BASE="http://127.0.0.1:8000"

echo "[TEST] Login as Alice..."
TOKEN_A=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"alice"}' | jq -r '.access_token')

echo "[TEST] Creating new audit test group..."
GROUP_ID=$(curl -s -X POST "$BASE/groups/" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"name":"Audit Group"}' | jq -r '.id')

echo "[TEST] Creating expense..."
curl -s -X POST "$BASE/expenses/group/$GROUP_ID" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"amount":15.50,"description":"Snacks"}' > /dev/null

echo "[TEST] Fetching audit logs..."
curl -s -X GET "$BASE/audit/group/$GROUP_ID" \
  -H "Authorization: Bearer $TOKEN_A" | jq

exit 0


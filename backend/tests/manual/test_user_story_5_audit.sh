# /Users/kubu/tcx2004-faris-project/backend/tests/manual/test_user_story_5_audit.sh

#!/bin/bash
# User Story 5: View Detailed Audit Logs

BASE="http://127.0.0.1:8000"

echo "============================================"
echo "[USER STORY 5] Testing Audit Trail"
echo "============================================"

# --------------------------
# 1. LOGIN USERS
# --------------------------

echo "[TEST] Logging in Alice (admin)..."
TOKEN_A=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"alice"}' | jq -r '.access_token')

echo "[TEST] Logging in Bob (member)..."
TOKEN_B=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"bob@test.com","password":"bob"}' | jq -r '.access_token')

if [ -z "$TOKEN_A" ] || [ "$TOKEN_A" == "null" ]; then
  echo "❌ Admin login failed"
  exit 1
fi

if [ -z "$TOKEN_B" ] || [ "$TOKEN_B" == "null" ]; then
  echo "❌ Member login failed"
  exit 1
fi


# --------------------------
# 2. CREATE GROUP
# --------------------------

echo "[TEST] Alice creates a group for audit testing..."
GROUP_ID=$(curl -s -X POST "$BASE/groups/" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"name":"Audit Test Group"}' | jq -r '.id')

echo "Group ID: $GROUP_ID"


# --------------------------
# 3. ADD BOB AS MEMBER
# --------------------------

echo "[TEST] Alice adds Bob..."
curl -s -X POST "$BASE/groups/$GROUP_ID/members/" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2}' > /dev/null


# --------------------------
# 4. TRIGGER AUDIT EVENTS
# --------------------------

echo "[TEST] Creating expense to trigger audit log..."

EXP_ID=$(curl -s -X POST "$BASE/expenses/group/$GROUP_ID" \
  -H "Authorization: Bearer $TOKEN_B" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10, "description": "Coffee"}' | jq -r '.id')

echo "Expense ID created by Bob: $EXP_ID"

echo "[TEST] Updating expense..."
curl -s -X PUT "$BASE/expenses/$EXP_ID" \
  -H "Authorization: Bearer $TOKEN_B" \
  -H "Content-Type: application/json" \
  -d '{"amount": 12, "description": "Coffee Updated"}' > /dev/null

echo "[TEST] Deleting expense..."
curl -s -X DELETE "$BASE/expenses/$EXP_ID" \
  -H "Authorization: Bearer $TOKEN_B" > /dev/null


# --------------------------
# 5. ADMIN FETCHES AUDIT LOGS (SHOULD PASS)
# --------------------------

echo "[TEST] Admin fetches audit logs..."
AUDIT=$(curl -s -X GET "$BASE/audit/group/$GROUP_ID" \
  -H "Authorization: Bearer $TOKEN_A")

echo "$AUDIT" | jq


# --------------------------
# 6. VERIFY AUDIT LOGS ARE PRESENT
# --------------------------

COUNT=$(echo "$AUDIT" | jq length)

if [ "$COUNT" -lt 3 ]; then
  echo "❌ Expected at least 3 audit log entries, got $COUNT"
  exit 1
fi

echo "✔ Found $COUNT audit log entries"


# --------------------------
# 7. MEMBER SHOULD *NOT* SEE AUDIT LOGS
# --------------------------

echo "[TEST] Bob tries to read audit logs (should be 403)..."

STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X GET "$BASE/audit/group/$GROUP_ID" \
  -H "Authorization: Bearer $TOKEN_B")

if [ "$STATUS" != "403" ]; then
  echo "❌ Expected 403, got $STATUS"
  exit 1
fi

echo "✔ Bob is correctly blocked from viewing audit logs"


echo "============================================"
echo "✔ User Story 5 tests PASSED"
echo "============================================"

exit 0

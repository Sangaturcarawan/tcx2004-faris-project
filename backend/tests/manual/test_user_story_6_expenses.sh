# backend/tests/manual/test_user_story_6_expenses.sh

#!/bin/bash
# User Story 6: Group Member Expense CRUD

BASE="http://127.0.0.1:8000"

echo "============================================"
echo "[USER STORY 6] Testing Expense Functionality"
echo "============================================"

# --------------------------
# 1. LOGIN EXISTING USERS
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
# 2. CREATE GROUP FOR TESTING
# --------------------------

echo "[TEST] Alice creates a new group..."
GROUP_ID=$(curl -s -X POST "$BASE/groups/" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"name":"US6 Expense Test Group"}' | jq -r '.id')

echo "Created group ID: $GROUP_ID"


# --------------------------
# 3. ADD BOB AS MEMBER
# --------------------------

echo "[TEST] Alice adds Bob to the group..."
curl -s -X POST "$BASE/groups/$GROUP_ID/members/" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2}' > /dev/null


# --------------------------
# 4. BOB CREATES AN EXPENSE
# --------------------------

echo "[TEST] Bob creates a new expense..."
EXPENSE=$(curl -s -X POST "$BASE/expenses/group/$GROUP_ID" \
  -H "Authorization: Bearer $TOKEN_B" \
  -H "Content-Type: application/json" \
  -d '{
        "amount": 50.0,
        "description": "Lunch",
        "shares": {"1": 25, "2": 25}
      }')

EXP_ID=$(echo "$EXPENSE" | jq -r '.id')

echo "Expense created with ID: $EXP_ID"


if [ "$EXP_ID" == "null" ] || [ -z "$EXP_ID" ]; then
  echo "❌ Expense creation failed"
  exit 1
fi


# --------------------------
# 5. BOB UPDATES HIS OWN EXPENSE
# --------------------------

echo "[TEST] Bob updates his own expense..."
curl -s -X PUT "$BASE/expenses/$EXP_ID" \
  -H "Authorization: Bearer $TOKEN_B" \
  -H "Content-Type: application/json" \
  -d '{
        "amount": 60.0,
        "description": "Lunch (updated)",
        "shares": {"1": 30, "2": 30}
      }' | jq


# --------------------------
# 6. BOB DELETES HIS OWN EXPENSE
# --------------------------

echo "[TEST] Bob deletes his own expense..."
curl -s -X DELETE "$BASE/expenses/$EXP_ID" \
  -H "Authorization: Bearer $TOKEN_B" | jq


# --------------------------
# 7. ADMIN CREATES EXPENSE
# --------------------------

echo "[TEST] Admin creates an expense Bob CANNOT modify..."
ADMIN_EXP=$(curl -s -X POST "$BASE/expenses/group/$GROUP_ID" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.0, "description": "Hotel"}')

ADMIN_EXP_ID=$(echo "$ADMIN_EXP" | jq -r '.id')


# --------------------------
# 8. BOB TRIES TO UPDATE ADMIN'S EXPENSE (SHOULD FAIL)
# --------------------------

echo "[TEST] Bob tries to update admin's expense (should be 403)..."
INVALID_UPDATE=$(curl -s -o /dev/null -w "%{http_code}" \
  -X PUT "$BASE/expenses/$ADMIN_EXP_ID" \
  -H "Authorization: Bearer $TOKEN_B" \
  -H "Content-Type: application/json" \
  -d '{"amount": 999.0, "description": "ILLEGAL"}')

if [ "$INVALID_UPDATE" != "403" ]; then
  echo "❌ Expected 403, got $INVALID_UPDATE"
  exit 1
fi

echo "✔ Bob is correctly blocked from updating admin's expense"


# --------------------------
# 9. ADMIN UPDATES ADMIN EXPENSE (SHOULD PASS)
# --------------------------

echo "[TEST] Admin updates own expense..."
curl -s -X PUT "$BASE/expenses/$ADMIN_EXP_ID" \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"amount": 120.0, "description": "Hotel Updated"}' | jq


echo "============================================"
echo "✔ User Story 6 tests PASSED"
echo "============================================"

exit 0

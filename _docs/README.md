User Stories:

1. As a new user, I can sign up, log in, and log out using my email so that I can securely manage my account and expenses

- SIGN UP (Create Account) (new user)

  - create a user account with email + hashed password
  - POST /auth/signup
  - store email and password as environment variables:
  - expected output:
  - {"id":3,"email":"zachary@gmail.com"}

- LOG IN (get JWT Token)

  - validates user credentials & returns a JWT access token
  - POST /auth/login
  - expected output:

- CHECK LOGIN STATUS (get current user)

  - checks the user is logged in by decoding JWT token
  - GET /me
  - expected output:

- securely manage my account and expenses:

  - use of JWT token for all protected endpoints ensure security
  - Authorization: Bearer <JWT_TOKEN>
  - only logged-in users can access their groups/expenses
  - all actions are tied to the authenticated user and none other
  - no password needed to be sent after login

- LOG OUT (delete JWT Token)
  - JWT tokens not invalidated on server, logout returns confirmation message
  - JWT token will be deleted client-side to complete logout
  - POST /auth/logout
  - expected output:
  - {"message":"Logged out successfully. Token invalidated client-side"}

2. As a registered user, I can create, view, update, and delete expense groups so that I can organize shared expenses for different contexts

- CREATE EXPENSE GROUPS (registered + logged in)
  - POST /groups/
- VIEW EXPENSE GROUPS (registered + logged in)
  - GET /groups/
- UPDATE EXPENSE GROUPS (registered + logged in)
  - PUT /groups/{group_id}
- DELETE EXPENSE GROUPS (registered + logged in)
  - DELETE /groups/{group_id}

3. As a group admin (Defined as the creator of the expense group), I can add, update, and remove group members so that I can manage group membership and ensure only relevant people are included.

   - ADD MEMBERS TO EXPENSE GROUP
     - POST /groups/{group_id}/members/
   - UPDATE EXPENSE GROUP MEMBERS
   - REMOVE EXPENSE GROUP MEMBER
   - LIST MEMBERS OF EXPENSE GROUP

FLOW OF EVENTS:

Store email & password as environment variables:
EMAIL="<email>"
PASSWORD="<password>"

Sign up:
curl -X POST "http://127.0.0.1:8000/auth/signup" -H "Content-Type: application/json" -d '{"email":"'"$EMAIL"'","password":"'"$PASSWORD"'"}'

Log in:
curl -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"email":"'"$EMAIL"'","password":"'"$PASSWORD"'"}'

Store JWT token:
TOKEN=<JWT_TOKEN>

Check user status:
curl -X GET "http://127.0.0.1:8000/me" -H "Authorization: Bearer $TOKEN"

Logout:
curl -X POST "http://127.0.0.1:8000/auth/logout" -H "Authorization: Bearer $TOKEN"

Log in:
curl -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"email":"'"$EMAIL"'","password":"'"$PASSWORD"'"}'

Store group name:
GRPNAME=

Create group:
curl -X POST "http://127.0.0.1:8000/groups/" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name": "'"$GRPNAME"'"}'

View groups:
curl -X GET "http://127.0.0.1:8000/groups/" -H "Authorization: Bearer $TOKEN"

Store new group name
NEWGRPNAME=

Store group id to be updated
GRPIDUPD=

Update group:
curl -X PUT "http://127.0.0.1:8000/groups/$GRPIDUPD" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name": "'"$NEWGRPNAME"'"}'

View groups:
curl -X GET "http://127.0.0.1:8000/groups/" -H "Authorization: Bearer $TOKEN"

Store group id to be deleted:
GRPIDDEL=

Delete group:

Delete group:
curl -X DELETE "http://127.0.0.1:8000/groups/$GRPIDDEL" -H "Authorization: Bearer $TOKEN"

View groups:
curl -X GET "http://127.0.0.1:8000/groups/" -H "Authorization: Bearer $TOKEN"

Store group id to list all members:
GRPMBRGETID=

List members of a group:
curl -X GET "http://127.0.0.1:8000/groups/$GRPMBRGETID/members/" -H "Authorization: Bearer $TOKEN"

Store group id you want to add a member to:
GRPMBRADDID=2

Store user id you want to add as member of a group:
USRIDADD=3

Add member to group:
curl -X POST "http://127.0.0.1:8000/groups/$GRPMBRADDID/members/" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"user_id": '"$USRIDADD"',"role": "member"}'

Update member role in group:
curl -X PUT "http://127.0.0.1:8000/groups/2/members/1" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"role": "admin"}'

Remove member from group:
curl -X DELETE "http://127.0.0.1:8000/groups/2/members/2" -H "Authorization: Bearer $TOKEN"

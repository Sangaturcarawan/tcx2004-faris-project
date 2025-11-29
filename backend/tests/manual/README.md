# Manual API Test Scripts

This directory contains `.sh` shell scripts used to manually test each user story in the TCX2004 Iteration 1 backend.

This project includes a full automated manual test suite under:
```
tests/manual/
```

## How to Run

1. Make all scripts executable:

```bash
chmod +x *.sh
```

2. Start your backend:

```
uvicorn app.main:app --reload
```

3. Run any test file:
```
./test_user_story_1_auth.sh
```

4. Run all tests:
```
./tests/manual/run_all_tests.sh
```

All scripts assume:
```
Base URL = http://127.0.0.1:8000
```
You are using macOS/Linux/WSL (bash supported)

### Scripts Included

| Script                             | Tests          | Summary                               |
|------------------------------------|----------------|----------------------------------------|
| `test_user_story_1_auth.sh`        | User Story 1   | Signup, Login, Logout                  |
| `test_user_story_2_groups.sh`      | User Story 2   | CRUD expense groups                    |
| `test_user_story_3_group_members.sh` | User Story 3 | Add/Update/Remove members              |
| `test_user_story_4_invitations.sh` | User Story 4   | Invite, accept, decline                |
| `test_user_story_5_expenses.sh`    | User Story 5   | Create, update, delete expenses        |

These scripts help verify that your backend is functioning correctly after each change.

#!/bin/bash
# Run all user story test scripts

GREEN="\e[32m"
RED="\e[31m"
NC="\e[0m"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}      TCX2004 BACKEND TEST SUITE       ${NC}"
echo -e "${GREEN}========================================${NC}"

SCRIPTS=(
  "test_user_story_1_auth.sh"
  "test_user_story_2_groups.sh"
  "test_user_story_3_members.sh"
  "test_user_story_4_invitations.sh"
  "test_user_story_5_audit.sh"
)

for script in "${SCRIPTS[@]}"; do
  echo -e "\n${GREEN}➡ Running $script...${NC}"
  bash "$(dirname "$0")/$script"

  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✔ $script PASSED${NC}"
  else
    echo -e "${RED}✘ $script FAILED${NC}"
  fi

  echo -e "${GREEN}----------------------------------------${NC}"
done

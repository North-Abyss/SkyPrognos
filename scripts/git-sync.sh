#!/bin/bash

# Git Commit & Sync Script - /scripts/git-sync.sh
# Syncs local repository with remote
# Usage: ./scripts/git-sync.sh [commit_message]

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting SkyPrognos git sync...${NC}"

# Stage all changes
echo -e "${BLUE}Staging changes...${NC}"
git add .

# Commit changes
echo -e "${BLUE}Committing changes...${NC}"
commit_message="$1"
if [[ -z "$commit_message" ]]; then
    read -p "Enter commit message (leave blank for auto-timestamp): " commit_message
fi

if [[ -z "$commit_message" ]]; then
    commit_message="$(date '+%d-%b-%Y-T-%H:%M')"
    echo -e "${YELLOW}Using auto commit message: $commit_message${NC}"
fi

git commit -m "$commit_message" || echo "No changes to commit"

# Check if origin is configured
if ! git remote get-url origin > /dev/null 2>&1; then
    echo -e "${YELLOW}No remote 'origin' configured. Skipping fetch/pull/push.${NC}"
    echo -e "${GREEN}Local git commit completed successfully!${NC}"
    exit 0
fi

# Fetch latest changes from remote (this also fetches the latest tags)
echo -e "${BLUE}Fetching from remote...${NC}"
git fetch origin "$(git rev-parse --abbrev-ref HEAD)" --tags

# Pull latest changes to current branch
echo -e "${BLUE}Pulling changes...${NC}"
git pull origin "$(git rev-parse --abbrev-ref HEAD)"

# Push local commits to remote
echo -e "${BLUE}Pushing changes...${NC}"
git push origin "$(git rev-parse --abbrev-ref HEAD)"

echo -e "${GREEN}Git sync completed successfully!${NC}"
echo ""

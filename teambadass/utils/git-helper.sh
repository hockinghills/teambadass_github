#!/bin/bash
# TeamBadass Git Helper Script
# Usage: ./git-helper.sh commit "Commit message"

REPO_DIR="/home/louthenw/Documents/teambadass_github/teambadass"

function commit_changes() {
  echo "Committing changes to TeamBadass repository..."
  cd $REPO_DIR
  
  # Check for changes
  if git status --porcelain | grep -q .; then
    # Changes exist, commit them
    git add .
    git commit -m "$1"
    
    echo "Changes committed with message: $1"
    echo "Use 'git push' to push changes to remote repository"
  else
    echo "No changes to commit"
  fi
}

function show_status() {
  echo "Checking TeamBadass repository status..."
  cd $REPO_DIR
  git status
}

# Main script
case "$1" in
  commit)
    if [ -z "$2" ]; then
      echo "Error: Commit message required"
      echo "Usage: ./git-helper.sh commit \"Commit message\""
      exit 1
    fi
    commit_changes "$2"
    ;;
  status)
    show_status
    ;;
  *)
    echo "TeamBadass Git Helper"
    echo "Usage:"
    echo "  ./git-helper.sh commit \"Commit message\" - Commit changes"
    echo "  ./git-helper.sh status - Show repository status"
    ;;
esac

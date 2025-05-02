#!/bin/bash
# TeamBadass Cleanup Script
# Makes cleanup.py executable and runs it

# Path to repository
REPO_PATH="/home/louthenw/Documents/teambadass_github/teambadass"
SCRIPT_PATH="$REPO_PATH/utils/cleanup.py"

# Make script executable
chmod +x "$SCRIPT_PATH"

# Run the script
python3 "$SCRIPT_PATH"

# Exit with same status as the script
exit $?

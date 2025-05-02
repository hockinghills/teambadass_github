#!/usr/bin/env python3
"""
TeamBadass Cleanup Utility
- Safely removes the tmp_backup directory
- Records deletion in system log
"""

import os
import shutil
from datetime import datetime

# Configuration
REPO_PATH = "/home/louthenw/Documents/teambadass_github/teambadass"
BACKUP_DIR = os.path.join(REPO_PATH, "tmp_backup")
LOG_PATH = os.path.join(REPO_PATH, "memory", "system_log.txt")

def main():
    """Main execution function"""
    print(f"TeamBadass Cleanup Utility")
    print(f"Target: {BACKUP_DIR}")
    
    # Verify directory exists
    if not os.path.exists(BACKUP_DIR):
        print(f"Error: Directory not found: {BACKUP_DIR}")
        return False
    
    # Get directory size before deletion
    size_bytes = get_dir_size(BACKUP_DIR)
    size_kb = size_bytes / 1024
    
    # List files to be deleted
    print(f"\nFiles to be deleted:")
    files = os.listdir(BACKUP_DIR)
    for file in files:
        file_path = os.path.join(BACKUP_DIR, file)
        file_size = os.path.getsize(file_path) / 1024  # KB
        print(f"- {file} ({file_size:.1f} KB)")
    
    # Confirmation
    print(f"\nTotal size: {size_kb:.1f} KB")
    confirm = input("\nConfirm deletion (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print("Deletion cancelled.")
        return False
    
    # Perform deletion
    try:
        shutil.rmtree(BACKUP_DIR)
        print(f"Successfully deleted directory: {BACKUP_DIR}")
        
        # Log the operation
        log_deletion(files, size_kb)
        
        return True
    except Exception as e:
        print(f"Error during deletion: {e}")
        return False

def get_dir_size(path):
    """Calculate total directory size"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def log_deletion(files, size_kb):
    """Log the deletion operation"""
    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    # Create log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] CLEANUP: Removed tmp_backup directory ({size_kb:.1f} KB)\n"
    log_entry += f"Files deleted: {', '.join(files)}\n\n"
    
    # Write to log file
    with open(LOG_PATH, "a") as log_file:
        log_file.write(log_entry)
    
    print(f"Operation logged to: {LOG_PATH}")

if __name__ == "__main__":
    main()

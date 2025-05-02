#!/usr/bin/env python3
"""
TeamBadass Enhanced Cleanup Utility
Move directories to external storage instead of deleting
"""

import os
import sys
import shutil
import argparse
from datetime import datetime

# Import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.storage_manager import StorageManager

def get_dir_size(path):
    """Calculate total directory size"""
    total_size = 0
    file_count = 0
    
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            file_size = os.path.getsize(fp)
            total_size += file_size
            file_count += 1
    
    return total_size, file_count

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Clean up repository directories")
    parser.add_argument('--target', type=str, required=True, help='Target directory to clean up')
    parser.add_argument('--delete', action='store_true', help='Delete instead of moving to external storage')
    parser.add_argument('--no-confirm', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()
    
    # Create storage manager
    manager = StorageManager()
    
    # Normalize target path
    target = args.target
    if not os.path.isabs(target):
        target = os.path.join(manager.repo_path, target)
    
    # Verify target exists
    if not os.path.exists(target):
        print(f"Error: Target directory not found: {target}")
        return False
    
    print(f"TeamBadass Enhanced Cleanup")
    print(f"Target: {target}")
    
    # Get directory size
    size_bytes, file_count = get_dir_size(target)
    size_kb = size_bytes / 1024
    
    print(f"Size: {size_kb:.2f} KB ({file_count} files)")
    print(f"Operation: {'Delete' if args.delete else 'Move to external storage'}")
    
    # List files to be processed
    print(f"\nFiles to process:")
    files = os.listdir(target)
    for file in files:
        file_path = os.path.join(target, file)
        try:
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"- {file} ({file_size:.1f} KB)")
            else:
                dir_size, dir_files = get_dir_size(file_path)
                print(f"- {file}/ ({(dir_size/1024):.1f} KB, {dir_files} files)")
        except Exception as e:
            print(f"- {file} (Error: {e})")
    
    # Confirm action unless skipped
    if not args.no_confirm:
        action = "Delete" if args.delete else "Move to external storage"
        confirm = input(f"\nConfirm {action}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Operation cancelled")
            return False
    
    # Perform operation
    try:
        if args.delete:
            # Remove directory
            shutil.rmtree(target)
            print(f"Deleted directory: {target}")
        else:
            # Move to external storage
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            basename = os.path.basename(target)
            dest_dir = f"{basename}_{timestamp}"
            
            # Create archive directory
            archive_path = os.path.join(manager.archive_path, dest_dir)
            
            # Move directory
            shutil.move(target, archive_path)
            print(f"Moved directory: {target} → {archive_path}")
        
        # Create log entry
        log_path = os.path.join(manager.repo_path, "memory", "system_log.txt")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        with open(log_path, "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if args.delete:
                log_file.write(f"[{timestamp}] DELETED {os.path.basename(target)} ({size_kb:.2f} KB, {file_count} files)\n")
            else:
                log_file.write(f"[{timestamp}] ARCHIVED {os.path.basename(target)} ({size_kb:.2f} KB, {file_count} files) to {archive_path}\n")
        
        print(f"Operation completed successfully!")
        return True
    except Exception as e:
        print(f"Error during operation: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)

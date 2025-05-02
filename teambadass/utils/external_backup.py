#!/usr/bin/env python3
"""
TeamBadass External Backup Utility
Move directories from repository to external storage
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
    parser = argparse.ArgumentParser(description="Move directories to external storage")
    parser.add_argument('--source', type=str, required=True, help='Source directory in repository')
    parser.add_argument('--category', type=str, default="archive", help='Category in external storage')
    parser.add_argument('--keep', action='store_true', help='Keep original directory')
    parser.add_argument('--no-confirm', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()
    
    # Create storage manager
    manager = StorageManager()
    
    # Normalize source path
    source = args.source
    if not os.path.isabs(source):
        source = os.path.join(manager.repo_path, source)
    
    # Verify source exists
    if not os.path.exists(source):
        print(f"Error: Source directory not found: {source}")
        return False
    
    # Create timestamp for directory name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    basename = os.path.basename(source)
    dest_dir = f"{basename}_{timestamp}"
    
    # Create category directory
    category_path = os.path.join(manager.external_path, args.category)
    os.makedirs(category_path, exist_ok=True)
    
    # Full destination path
    dest_path = os.path.join(category_path, dest_dir)
    
    print(f"TeamBadass External Backup")
    print(f"Source: {source}")
    print(f"Destination: {dest_path}")
    
    # Get directory size
    size_bytes, file_count = get_dir_size(source)
    size_kb = size_bytes / 1024
    
    print(f"Size: {size_kb:.2f} KB ({file_count} files)")
    
    # Confirm action unless skipped
    if not args.no_confirm:
        action = "Copy" if args.keep else "Move"
        confirm = input(f"\n{action} to external storage? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Operation cancelled")
            return False
    
    # Perform operation
    try:
        if args.keep:
            shutil.copytree(source, dest_path)
            print(f"Copied: {source} → {dest_path}")
        else:
            shutil.move(source, dest_path)
            print(f"Moved: {source} → {dest_path}")
        
        # Create log entry
        log_path = os.path.join(manager.repo_path, "memory", "system_log.txt")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        with open(log_path, "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            action = "Copied" if args.keep else "Moved"
            log_file.write(f"[{timestamp}] {action} {basename} ({size_kb:.2f} KB) to external storage: {dest_path}\n")
        
        print(f"Operation completed successfully!")
        return True
    except Exception as e:
        print(f"Error during operation: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)

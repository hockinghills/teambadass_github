#!/usr/bin/env python3
"""
TeamBadass External Storage Setup
Creates and configures external storage locations
"""

import os
import sys
import json
import argparse
from pathlib import Path

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Set up external storage for TeamBadass")
    parser.add_argument('--external-path', type=str, help='Path to external storage location')
    parser.add_argument('--repo-path', type=str, help='Path to TeamBadass repository')
    args = parser.parse_args()
    
    # Set default paths if not provided
    repo_path = args.repo_path or "/home/louthenw/Documents/teambadass_github/teambadass"
    external_path = args.external_path or "/home/louthenw/teambadass_external"
    
    print(f"TeamBadass External Storage Setup")
    print(f"Repository: {repo_path}")
    print(f"External Storage: {external_path}")
    
    # Verify repository exists
    if not os.path.exists(repo_path):
        print(f"Error: Repository path not found: {repo_path}")
        return False
    
    # Create external storage structure
    directories = [
        external_path,
        os.path.join(external_path, "backups"),
        os.path.join(external_path, "temp"),
        os.path.join(external_path, "archive")
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created: {directory}")
        except Exception as e:
            print(f"Error creating {directory}: {e}")
            return False
    
    # Create storage configuration
    config = {
        "external_path": external_path,
        "backup_path": os.path.join(external_path, "backups"),
        "temp_path": os.path.join(external_path, "temp"),
        "archive_path": os.path.join(external_path, "archive"),
        "cloud_enabled": False,
        "cloud_provider": None,
        "cloud_config": {}
    }
    
    # Save configuration to repository
    config_path = os.path.join(repo_path, "memory", "config", "storage.json")
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to: {config_path}")
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False
    
    # Create symbolic link
    try:
        link_path = os.path.join(repo_path, ".external")
        if os.path.exists(link_path) or os.path.islink(link_path):
            os.unlink(link_path)
        
        os.symlink(external_path, link_path)
        print(f"Created symbolic link: {link_path} → {external_path}")
    except Exception as e:
        print(f"Error creating symbolic link: {e}")
        
    print("\nExternal storage setup complete!")
    print("\nTest your setup by running the storage manager:")
    print(f"python3 {os.path.join(repo_path, 'utils', 'storage_manager.py')}")
    
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)

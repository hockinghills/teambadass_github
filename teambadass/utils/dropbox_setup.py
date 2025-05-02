#!/usr/bin/env python3
"""
TeamBadass Dropbox Integration Setup
Configure Dropbox API access for cloud storage
"""

import os
import sys
import json
import argparse
import webbrowser
from datetime import datetime

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Set up Dropbox integration for TeamBadass")
    parser.add_argument('--repo-path', type=str, help='Path to TeamBadass repository')
    parser.add_argument('--token', type=str, help='Dropbox API access token')
    parser.add_argument('--folder', type=str, default="TeamBadass", help='Dropbox folder to use')
    args = parser.parse_args()
    
    # Set default paths if not provided
    repo_path = args.repo_path or "/home/louthenw/Documents/teambadass_github/teambadass"
    
    print(f"TeamBadass Dropbox Integration Setup")
    print(f"Repository: {repo_path}")
    
    # Verify repository exists
    if not os.path.exists(repo_path):
        print(f"Error: Repository path not found: {repo_path}")
        return False
    
    # Check if storage config exists
    config_path = os.path.join(repo_path, "memory", "config", "storage.json")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False
    else:
        print(f"Error: Storage configuration not found. Run setup_external_storage.py first.")
        return False
    
    # Check for token
    token = args.token
    if not token:
        print("\nNo Dropbox API token provided. You need to:")
        print("1. Create a Dropbox app at https://www.dropbox.com/developers/apps")
        print("2. Generate an access token for your app")
        print("3. Run this script again with --token YOUR_TOKEN")
        
        open_browser = input("\nOpen Dropbox developer site now? (yes/no): ").strip().lower()
        if open_browser == "yes":
            webbrowser.open("https://www.dropbox.com/developers/apps")
        
        return False
    
    # Get folder name
    folder_name = args.folder
    
    # Create folder paths
    folder_path = f"/{folder_name}"
    backup_path = f"/{folder_name}/backups"
    temp_path = f"/{folder_name}/temp"
    archive_path = f"/{folder_name}/archive"
    
    # Update configuration
    config["cloud_enabled"] = True
    config["cloud_provider"] = "dropbox"
    config["cloud_config"] = {
        "access_token": token,
        "root_path": folder_path,
        "backup_path": backup_path,
        "temp_path": temp_path,
        "archive_path": archive_path,
        "setup_date": datetime.now().isoformat()
    }
    
    # Save updated configuration
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Dropbox configuration saved to: {config_path}")
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False
    
    # Try to install Dropbox SDK
    try:
        import subprocess
        print("\nInstalling Dropbox SDK...")
        result = subprocess.run(["pip", "install", "dropbox"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Dropbox SDK installed successfully")
        else:
            print(f"Error installing Dropbox SDK: {result.stderr}")
            print("You may need to install it manually: pip install dropbox")
    except Exception as e:
        print(f"Error installing Dropbox SDK: {e}")
        print("You may need to install it manually: pip install dropbox")
    
    # Create dropbox client test script
    test_script_path = os.path.join(repo_path, "utils", "dropbox_test.py")
    try:
        with open(test_script_path, 'w') as f:
            f.write('''#!/usr/bin/env python3
"""
TeamBadass Dropbox Integration Test
Test Dropbox API connection and folder access
"""

import os
import sys
import json
import argparse
from datetime import datetime

try:
    import dropbox
    from dropbox import exceptions
except ImportError:
    print("Dropbox SDK not installed. Run: pip install dropbox")
    sys.exit(1)

# Import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.storage_manager import StorageManager

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Test Dropbox integration for TeamBadass")
    parser.add_argument('--verbose', action='store_true', help='Display detailed information')
    args = parser.parse_args()
    
    # Create storage manager
    manager = StorageManager()
    
    # Check if cloud is enabled
    if not manager.config.get("cloud_enabled"):
        print("Error: Cloud storage is not enabled")
        return False
    
    # Check if provider is Dropbox
    provider = manager.config.get("cloud_provider")
    if provider != "dropbox":
        print(f"Error: Cloud provider is not Dropbox ({provider})")
        return False
    
    # Get Dropbox configuration
    dropbox_config = manager.config.get("cloud_config", {})
    token = dropbox_config.get("access_token")
    
    if not token:
        print("Error: No Dropbox access token found")
        return False
    
    # Connect to Dropbox
    try:
        dbx = dropbox.Dropbox(token)
        account = dbx.users_get_current_account()
        print(f"Connected to Dropbox as {account.name.display_name}")
    except exceptions.AuthError:
        print("Error: Invalid access token")
        return False
    except Exception as e:
        print(f"Error connecting to Dropbox: {e}")
        return False
    
    # Create test directories if they don't exist
    root_path = dropbox_config.get("root_path", "/TeamBadass")
    paths = [
        root_path,
        dropbox_config.get("backup_path", f"{root_path}/backups"),
        dropbox_config.get("temp_path", f"{root_path}/temp"),
        dropbox_config.get("archive_path", f"{root_path}/archive")
    ]
    
    for path in paths:
        try:
            dbx.files_create_folder_v2(path)
            print(f"Created Dropbox folder: {path}")
        except exceptions.ApiError as e:
            if not isinstance(e.error, dropbox.files.CreateFolderError) or \
               e.error.get_path().is_conflict() is None:
                print(f"Error creating folder {path}: {e}")
            elif args.verbose:
                print(f"Folder already exists: {path}")
    
    # Create test file
    test_file_path = f"{root_path}/test_file.txt"
    test_content = f"TeamBadass Dropbox test file\\nCreated: {datetime.now().isoformat()}"
    
    try:
        dbx.files_upload(
            test_content.encode('utf-8'),
            test_file_path,
            mode=dropbox.files.WriteMode.overwrite
        )
        print(f"Created test file: {test_file_path}")
    except Exception as e:
        print(f"Error creating test file: {e}")
    
    # List files in root folder
    try:
        results = dbx.files_list_folder(root_path)
        
        print(f"\\nFiles in {root_path}:")
        for entry in results.entries:
            entry_type = "File" if isinstance(entry, dropbox.files.FileMetadata) else "Folder"
            print(f"- {entry_type}: {entry.name}")
    except Exception as e:
        print(f"Error listing files: {e}")
    
    print("\\nDropbox integration test completed")
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
''')
        print(f"Dropbox test script created: {test_script_path}")
    except Exception as e:
        print(f"Error creating test script: {e}")
    
    print("\nDropbox integration setup complete!")
    print("\nTo test your Dropbox integration, run:")
    print(f"python3 {test_script_path}")
    
    print("\nYou can now use Dropbox storage by implementing the CloudStorageManager class.")
    
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)

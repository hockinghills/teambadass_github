#!/usr/bin/env python3
"""
TeamBadass Storage Manager
Unified interface for repository, external and cloud storage
"""

import os
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("StorageManager")

class StorageManager:
    """Manages external storage locations and operations"""
    
    def __init__(self, config_path=None):
        """Initialize with optional config path"""
        self.repo_path = "/home/louthenw/Documents/teambadass_github/teambadass"
        
        # Default external storage location (outside repo)
        self.external_path = "/home/louthenw/teambadass_external"
        
        # Load config if available
        self.config = self._load_config(config_path)
        
        # Apply configuration
        self._apply_config()
    
    def _load_config(self, config_path=None):
        """Load configuration from file"""
        # Default config path
        if not config_path:
            config_path = os.path.join(self.repo_path, "memory", "config", "storage.json")
        
        # Try to load config
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load config: {e}")
        
        # Return default config
        return {
            "external_path": self.external_path,
            "backup_path": os.path.join(self.external_path, "backups"),
            "temp_path": os.path.join(self.external_path, "temp"),
            "archive_path": os.path.join(self.external_path, "archive"),
            "cloud_enabled": False,
            "cloud_provider": None,
            "cloud_config": {}
        }
    
    def _apply_config(self):
        """Apply configuration settings"""
        # Set paths from config
        self.external_path = self.config.get("external_path", self.external_path)
        self.backup_path = self.config.get("backup_path", os.path.join(self.external_path, "backups"))
        self.temp_path = self.config.get("temp_path", os.path.join(self.external_path, "temp"))
        self.archive_path = self.config.get("archive_path", os.path.join(self.external_path, "archive"))
        
        # Ensure directories exist
        for path in [self.external_path, self.backup_path, self.temp_path, self.archive_path]:
            os.makedirs(path, exist_ok=True)
    
    def save_config(self, config_path=None):
        """Save current configuration"""
        if not config_path:
            config_path = os.path.join(self.repo_path, "memory", "config", "storage.json")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Save config
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        logger.info(f"Configuration saved to: {config_path}")
        return True
    
    def backup_file(self, source_path, category="general"):
        """Backup a file to external storage"""
        # Normalize source path
        if not os.path.isabs(source_path):
            source_path = os.path.join(self.repo_path, source_path)
        
        # Ensure source exists
        if not os.path.exists(source_path):
            logger.error(f"Source file not found: {source_path}")
            return False
        
        # Create category directory
        category_dir = os.path.join(self.backup_path, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Create destination path
        filename = os.path.basename(source_path)
        dest_path = os.path.join(category_dir, filename)
        
        # Copy file
        try:
            shutil.copy2(source_path, dest_path)
            logger.info(f"Backed up: {source_path} → {dest_path}")
            return dest_path
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
    
    def create_external_directory(self, directory, exist_ok=True):
        """Create directory in external storage"""
        path = os.path.join(self.external_path, directory)
        os.makedirs(path, exist_ok=exist_ok)
        logger.info(f"Created external directory: {path}")
        return path
    
    def move_to_external(self, source_path, dest_dir=None, remove_original=True):
        """Move file or directory to external storage"""
        # Normalize source path
        if not os.path.isabs(source_path):
            source_path = os.path.join(self.repo_path, source_path)
        
        # Ensure source exists
        if not os.path.exists(source_path):
            logger.error(f"Source not found: {source_path}")
            return False
        
        # Determine destination directory
        if not dest_dir:
            dest_dir = ""
        
        dest_path = os.path.join(self.external_path, dest_dir)
        os.makedirs(dest_path, exist_ok=True)
        
        # Get destination filename
        filename = os.path.basename(source_path)
        full_dest_path = os.path.join(dest_path, filename)
        
        # Perform move/copy
        try:
            if remove_original:
                shutil.move(source_path, full_dest_path)
                logger.info(f"Moved: {source_path} → {full_dest_path}")
            else:
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, full_dest_path)
                else:
                    shutil.copytree(source_path, full_dest_path)
                logger.info(f"Copied: {source_path} → {full_dest_path}")
            
            return full_dest_path
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            return False
    
    def archive_directory(self, source_path, archive_name=None):
        """Archive a directory to the archive location"""
        # Normalize source path
        if not os.path.isabs(source_path):
            source_path = os.path.join(self.repo_path, source_path)
        
        # Ensure source exists
        if not os.path.exists(source_path):
            logger.error(f"Source not found: {source_path}")
            return False
        
        # Generate archive name if not provided
        if not archive_name:
            dirname = os.path.basename(source_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{dirname}_{timestamp}"
        
        # Create archive path
        archive_path = os.path.join(self.archive_path, archive_name)
        
        # Move directory to archive
        try:
            shutil.move(source_path, archive_path)
            logger.info(f"Archived: {source_path} → {archive_path}")
            return archive_path
        except Exception as e:
            logger.error(f"Archive failed: {e}")
            return False
    
    def get_external_path(self, relative_path=None):
        """Get absolute path in external storage"""
        if not relative_path:
            return self.external_path
        
        return os.path.join(self.external_path, relative_path)
    
    def list_external_directory(self, relative_path=None):
        """List contents of external directory"""
        path = self.get_external_path(relative_path)
        
        if not os.path.exists(path):
            logger.error(f"Path not found: {path}")
            return []
        
        try:
            return os.listdir(path)
        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            return []

# Run tests if executed directly
if __name__ == "__main__":
    # Create storage manager
    manager = StorageManager()
    
    # Display paths
    print(f"TeamBadass Storage Manager")
    print(f"===========================")
    print(f"Repository Path: {manager.repo_path}")
    print(f"External Path: {manager.external_path}")
    print(f"Backup Path: {manager.backup_path}")
    print(f"Temp Path: {manager.temp_path}")
    print(f"Archive Path: {manager.archive_path}")
    
    # Display cloud status
    cloud_enabled = manager.config.get("cloud_enabled", False)
    cloud_provider = manager.config.get("cloud_provider")
    print(f"\nCloud Storage: {'Enabled' if cloud_enabled else 'Disabled'}")
    if cloud_enabled and cloud_provider:
        print(f"Cloud Provider: {cloud_provider}")
    
    # List external directories
    print(f"\nExternal Directories:")
    for directory in ["backups", "temp", "archive"]:
        path = manager.get_external_path(directory)
        if os.path.exists(path):
            items = manager.list_external_directory(directory)
            print(f"- {directory}: {len(items)} items")

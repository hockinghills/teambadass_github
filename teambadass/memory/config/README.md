# TeamBadass Storage Configuration

This directory contains configuration files for the TeamBadass storage system.

## Key Files

- **storage.json** - External storage configuration
- **system.json** - Memory system configuration

## Storage Configuration

The `storage.json` file contains configuration for external and cloud storage:

```json
{
  "external_path": "/home/louthenw/teambadass_external",
  "backup_path": "/home/louthenw/teambadass_external/backups",
  "temp_path": "/home/louthenw/teambadass_external/temp",
  "archive_path": "/home/louthenw/teambadass_external/archive",
  "cloud_enabled": false,
  "cloud_provider": null,
  "cloud_config": {}
}
```

## Setup Instructions

To set up external storage:

```bash
python3 utils/setup_external_storage.py
```

To configure Dropbox integration:

```bash
python3 utils/dropbox_setup.py --token YOUR_API_TOKEN
```

## Usage Examples

Using external storage with the storage manager:

```python
from utils.storage_manager import StorageManager

# Create manager
manager = StorageManager()

# Move a directory to external storage
manager.move_to_external("tmp_backup", "archive")

# Create a backup of a file
manager.backup_file("important_file.txt", "backups")
```

Using the enhanced cleanup utility:

```bash
python3 utils/enhanced_cleanup.py --target tmp_backup
```

## Configuration Migration

If you've previously used other storage methods, you can migrate your configuration by:

1. Run setup_external_storage.py to establish the basic structure
2. Manually copy important files to the external location
3. Update any scripts that referenced old locations
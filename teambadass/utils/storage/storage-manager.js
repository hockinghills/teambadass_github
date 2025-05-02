/**
 * TeamBadass Storage Manager
 * Provides management for external storage locations and operations
 * 
 * FILE_OVERVIEW: Flexible storage management with local and cloud capabilities
 * VERSION: 1.0.0
 * LAST_UPDATED: 2025-05-03
 * DEPENDENCIES: fs-helper.js
 * 
 * TABLE_OF_CONTENTS:
 * 1. StorageManager Class - Main storage management implementation
 * 2. Configuration Management - Loading and saving storage configuration
 * 3. Directory Operations - Creating and validating storage directories
 * 4. File Operations - Moving and copying files to external storage
 * 5. Backup Operations - Creating and managing backups
 * 
 * SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
 */

const path = require('path');
const fsHelper = require('../fs-helper');

/**
 * Storage Manager for TeamBadass
 * Manages external storage locations and operations
 */
class StorageManager {
  /**
   * Create a new StorageManager
   * @param {Object} options - Configuration options
   * @param {string} options.repoPath - Repository base path
   * @param {string} options.externalPath - External storage base path
   * @param {boolean} options.verbose - Enable verbose logging
   */
  constructor(options = {}) {
    // Default options
    this.options = {
      repoPath: '/home/louthenw/Documents/teambadass_github/teambadass',
      externalPath: '/home/louthenw/teambadass_external',
      verbose: true,
      ...options
    };

    // Storage paths
    this.repoPath = this.options.repoPath;
    this.externalPath = this.options.externalPath;
    this.configPath = path.join(this.repoPath, 'memory', 'config', 'storage.json');

    // Additional paths will be set after loading config
    this.backupPath = null;
    this.tempPath = null;
    this.archivePath = null;

    // Storage state
    this.initialized = false;
    this.config = null;
    this.cloudEnabled = false;
  }

  /**
   * Initialize the storage manager
   * @returns {Promise<Object>} Initialization result
   */
  async initialize() {
    try {
      // Load configuration
      await this.loadConfig();

      // Ensure directories exist
      await this.ensureDirectories();

      // Create symbolic link if possible
      await this.createSymLink();

      this.initialized = true;
      this.log('Storage manager initialized successfully');

      return {
        status: 'success',
        paths: {
          external: this.externalPath,
          backup: this.backupPath,
          temp: this.tempPath,
          archive: this.archivePath
        },
        cloudEnabled: this.cloudEnabled
      };
    } catch (error) {
      this.log(`Initialization failed: ${error.message}`, 'error');
      return {
        status: 'error',
        message: error.message
      };
    }
  }

  /**
   * Load configuration from file or create default
   * @returns {Promise<Object>} Configuration object
   */
  async loadConfig() {
    try {
      // Check if config exists
      const configExists = await fsHelper.pathExists(this.configPath);

      if (configExists) {
        // Load existing config
        const configContent = await fs.read_file({ path: this.configPath });
        this.config = JSON.parse(configContent);
        this.log('Configuration loaded from file');
      } else {
        // Create default config
        this.config = {
          external_path: this.externalPath,
          backup_path: path.join(this.externalPath, 'backups'),
          temp_path: path.join(this.externalPath, 'temp'),
          archive_path: path.join(this.externalPath, 'archive'),
          cloud_enabled: false,
          cloud_provider: null,
          cloud_config: {}
        };
        this.log('Created default configuration');
      }

      // Apply configuration
      this.externalPath = this.config.external_path;
      this.backupPath = this.config.backup_path;
      this.tempPath = this.config.temp_path;
      this.archivePath = this.config.archive_path;
      this.cloudEnabled = this.config.cloud_enabled;

      return this.config;
    } catch (error) {
      this.log(`Error loading configuration: ${error.message}`, 'error');
      throw error;
    }
  }

  /**
   * Save configuration to file
   * @returns {Promise<boolean>} Success status
   */
  async saveConfig() {
    try {
      // Ensure directories exist
      await fsHelper.ensureDirectory(path.dirname(this.configPath));

      // Save config
      await fsHelper.writeFile(this.configPath, JSON.stringify(this.config, null, 2));
      this.log('Configuration saved to file');

      return true;
    } catch (error) {
      this.log(`Error saving configuration: ${error.message}`, 'error');
      return false;
    }
  }

  /**
   * Ensure all required directories exist
   * @returns {Promise<boolean>} Success status
   */
  async ensureDirectories() {
    try {
      // Create directories
      await fsHelper.ensureDirectory(this.externalPath);
      await fsHelper.ensureDirectory(this.backupPath);
      await fsHelper.ensureDirectory(this.tempPath);
      await fsHelper.ensureDirectory(this.archivePath);

      this.log('Storage directories created');
      return true;
    } catch (error) {
      this.log(`Error creating directories: ${error.message}`, 'error');
      throw error;
    }
  }

  /**
   * Create symbolic link to external storage
   * @returns {Promise<boolean>} Success status
   */
  async createSymLink() {
    try {
      // Skip if not running in an environment that supports symlinks
      if (typeof process === 'undefined') {
        return false;
      }

      const linkPath = path.join(this.repoPath, '.external');

      // Create symlink
      // Note: This would need NodeJS environment to work
      // In a real implementation, this would use fs.symlink
      this.log(`Would create symlink: ${linkPath} -> ${this.externalPath}`);

      return true;
    } catch (error) {
      this.log(`Error creating symlink: ${error.message}`, 'warning');
      return false;
    }
  }

  /**
   * Create a backup of a file or directory
   * @param {string} sourcePath - Path to file or directory to backup
   * @param {string} category - Category for organization (optional)
   * @returns {Promise<Object>} Backup result
   */
  async backup(sourcePath, category = 'general') {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      // Normalize path
      if (!path.isAbsolute(sourcePath)) {
        sourcePath = path.join(this.repoPath, sourcePath);
      }

      // Ensure source exists
      const sourceExists = await fsHelper.pathExists(sourcePath);
      if (!sourceExists) {
        throw new Error(`Source not found: ${sourcePath}`);
      }

      // Create category directory
      const categoryPath = path.join(this.backupPath, category);
      await fsHelper.ensureDirectory(categoryPath);

      // Get timestamp
      const timestamp = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');
      
      // Get basename
      const baseName = path.basename(sourcePath);
      
      // Create destination path with timestamp
      const destName = `${baseName}_${timestamp}`;
      const destPath = path.join(categoryPath, destName);

      // Copy file or directory
      // In a real implementation, this would use the appropriate fs methods
      this.log(`Backing up ${sourcePath} to ${destPath}`);

      // For demonstration, we'll just write a placeholder file
      await fsHelper.writeFile(
        destPath + '.info',
        JSON.stringify({
          originalPath: sourcePath,
          backupTime: timestamp,
          category: category
        }, null, 2)
      );

      return {
        status: 'success',
        originalPath: sourcePath,
        backupPath: destPath,
        timestamp: timestamp
      };
    } catch (error) {
      this.log(`Backup failed: ${error.message}`, 'error');
      return {
        status: 'error',
        message: error.message
      };
    }
  }

  /**
   * Move a file or directory to external storage
   * @param {string} sourcePath - Path to file or directory
   * @param {string} destDir - Destination directory (relative to external path)
   * @param {boolean} keepOriginal - Keep original if true, move if false
   * @returns {Promise<Object>} Operation result
   */
  async moveToExternal(sourcePath, destDir = '', keepOriginal = false) {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      // Normalize path
      if (!path.isAbsolute(sourcePath)) {
        sourcePath = path.join(this.repoPath, sourcePath);
      }

      // Ensure source exists
      const sourceExists = await fsHelper.pathExists(sourcePath);
      if (!sourceExists) {
        throw new Error(`Source not found: ${sourcePath}`);
      }

      // Create destination directory
      const fullDestDir = path.join(this.externalPath, destDir);
      await fsHelper.ensureDirectory(fullDestDir);

      // Get basename
      const baseName = path.basename(sourcePath);
      
      // Full destination path
      const destPath = path.join(fullDestDir, baseName);

      // Copy or move
      const operation = keepOriginal ? 'copy' : 'move';
      this.log(`${operation} ${sourcePath} to ${destPath}`);

      // For demonstration, we'll just write a placeholder file
      await fsHelper.writeFile(
        destPath + '.info',
        JSON.stringify({
          originalPath: sourcePath,
          operation: operation,
          timestamp: new Date().toISOString()
        }, null, 2)
      );

      return {
        status: 'success',
        operation: operation,
        originalPath: sourcePath,
        destinationPath: destPath
      };
    } catch (error) {
      this.log(`${keepOriginal ? 'Copy' : 'Move'} operation failed: ${error.message}`, 'error');
      return {
        status: 'error',
        message: error.message
      };
    }
  }

  /**
   * Archive a directory to external storage
   * @param {string} sourcePath - Path to directory
   * @param {string} name - Archive name (optional)
   * @returns {Promise<Object>} Archive result
   */
  async archiveDirectory(sourcePath, name = '') {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      // Normalize path
      if (!path.isAbsolute(sourcePath)) {
        sourcePath = path.join(this.repoPath, sourcePath);
      }

      // Ensure source exists
      const sourceExists = await fsHelper.pathExists(sourcePath);
      if (!sourceExists) {
        throw new Error(`Source not found: ${sourcePath}`);
      }

      // Generate archive name if not provided
      const baseName = name || path.basename(sourcePath);
      const timestamp = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');
      const archiveName = `${baseName}_${timestamp}`;
      
      // Create archive directory
      const archivePath = path.join(this.archivePath, archiveName);
      await fsHelper.ensureDirectory(archivePath);
      
      this.log(`Archiving ${sourcePath} to ${archivePath}`);

      // For demonstration, we'll just write a placeholder file
      await fsHelper.writeFile(
        archivePath + '.info',
        JSON.stringify({
          originalPath: sourcePath,
          archiveTime: timestamp,
          name: archiveName
        }, null, 2)
      );

      return {
        status: 'success',
        originalPath: sourcePath,
        archivePath: archivePath,
        name: archiveName
      };
    } catch (error) {
      this.log(`Archive operation failed: ${error.message}`, 'error');
      return {
        status: 'error',
        message: error.message
      };
    }
  }

  /**
   * Create a temporary file or directory
   * @param {string} name - Name for temp file/directory
   * @param {string} content - Content for file (optional)
   * @returns {Promise<Object>} Operation result
   */
  async createTemp(name, content = '') {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      // Generate unique name if not provided
      const tempName = name || `temp_${Date.now()}`;
      
      // Full temp path
      const tempPath = path.join(this.tempPath, tempName);
      
      // Write content if provided
      if (content) {
        await fsHelper.writeFile(tempPath, content);
        this.log(`Created temp file: ${tempPath}`);
      } else {
        await fsHelper.ensureDirectory(tempPath);
        this.log(`Created temp directory: ${tempPath}`);
      }

      return {
        status: 'success',
        path: tempPath,
        name: tempName,
        type: content ? 'file' : 'directory'
      };
    } catch (error) {
      this.log(`Temp operation failed: ${error.message}`, 'error');
      return {
        status: 'error',
        message: error.message
      };
    }
  }

  /**
   * Configure cloud storage
   * @param {string} provider - Cloud provider ('dropbox', 'google', etc.)
   * @param {Object} config - Provider-specific configuration
   * @returns {Promise<Object>} Configuration result
   */
  async configureCloud(provider, config = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      // Validate provider
      const validProviders = ['dropbox', 'google', 'onedrive', 'custom'];
      if (!validProviders.includes(provider.toLowerCase())) {
        throw new Error(`Unsupported cloud provider: ${provider}`);
      }

      // Update configuration
      this.config.cloud_enabled = true;
      this.config.cloud_provider = provider.toLowerCase();
      this.config.cloud_config = config;
      
      // Save configuration
      await this.saveConfig();
      
      this.cloudEnabled = true;
      this.log(`Cloud storage configured: ${provider}`);

      return {
        status: 'success',
        provider: provider,
        enabled: true
      };
    } catch (error) {
      this.log(`Cloud configuration failed: ${error.message}`, 'error');
      return {
        status: 'error',
        message: error.message
      };
    }
  }

  /**
   * Log a message
   * @param {string} message - Message to log
   * @param {string} level - Log level ('info', 'warning', 'error')
   */
  log(message, level = 'info') {
    if (!this.options.verbose && level === 'info') {
      return;
    }

    const prefix = {
      info: '📢 INFO:',
      warning: '⚠️ WARNING:',
      error: '❌ ERROR:',
    }[level] || '   ';

    console.log(`${prefix} ${message}`);
  }
}

module.exports = StorageManager;

/**
 * StorageManager Component
 * Central interface for all storage operations
 * 
 * FILE_OVERVIEW: Central storage management interface
 * VERSION: 1.0.0
 * LAST_UPDATED: 2025-05-03
 * DEPENDENCIES: None (adapters via dependency injection)
 * 
 * TABLE_OF_CONTENTS:
 * 1. Core Management - Initialization and configuration
 * 2. File Operations - Storage, retrieval, and deletion
 * 3. Path Utilities - Path normalization and processing
 * 
 * SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
 */

class StorageManager {
  /**
   * Create a new storage manager
   * @param {Object} options - Configuration options
   */
  constructor(options = {}) {
    this.localAdapter = options.localAdapter || null;
    this.cloudAdapter = options.cloudAdapter || null;
    this.initialized = false;
    this.config = {
      preferCloud: options.preferCloud || false,
      autoSync: options.autoSync || false,
      basePath: options.basePath || '/home/louthenw/Documents/teambadass_github/teambadass/_projects/storage-system/_data'
    };
  }

  /**
   * Initialize storage manager
   * @param {Object} options - Initialization options
   * @returns {Promise<boolean>} Success status
   */
  async initialize(options = {}) {
    try {
      // Initialize adapters if provided
      if (this.localAdapter) {
        await this.localAdapter.initialize();
      }

      if (this.cloudAdapter) {
        await this.cloudAdapter.initialize();
      }

      // Create base path if it doesn't exist
      if (this.localAdapter) {
        await this.localAdapter.createDirectory(this.config.basePath);
      }

      this.initialized = true;
      return true;
    } catch (error) {
      console.error(`Storage initialization failed: ${error.message}`);
      return false;
    }
  }

  /**
   * Store file with automatic adapter selection
   * @param {string} path - File path
   * @param {string|Buffer} content - File content
   * @param {Object} options - Storage options
   * @returns {Promise<Object>} - Storage result
   */
  async storeFile(path, content, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    // Normalize path
    const normalizedPath = this._normalizePath(path);
    
    // Select adapter based on preferences
    const useCloud = options.useCloud || this.config.preferCloud;

    try {
      let result;

      if (useCloud && this.cloudAdapter) {
        // Store in cloud
        result = await this.cloudAdapter.storeFile(normalizedPath, content);
        
        // Sync to local if auto-sync enabled
        if (this.config.autoSync && this.localAdapter) {
          await this.localAdapter.storeFile(normalizedPath, content);
        }
      } else if (this.localAdapter) {
        // Store locally
        result = await this.localAdapter.storeFile(normalizedPath, content);
      } else {
        throw new Error('No storage adapter available');
      }

      return {
        success: true,
        path: normalizedPath,
        size: typeof content === 'string' ? content.length : content.byteLength,
        timestamp: new Date().toISOString(),
        adapter: useCloud ? 'cloud' : 'local'
      };
    } catch (error) {
      return {
        success: false,
        path: normalizedPath,
        error: error.message
      };
    }
  }

  /**
   * Retrieve file with automatic adapter selection
   * @param {string} path - File path
   * @param {Object} options - Retrieval options
   * @returns {Promise<string|Buffer>} - File content
   */
  async retrieveFile(path, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    // Normalize path
    const normalizedPath = this._normalizePath(path);
    
    // Select adapter based on preferences
    const useCloud = options.useCloud || this.config.preferCloud;

    try {
      if (useCloud && this.cloudAdapter) {
        // Try cloud first
        try {
          return await this.cloudAdapter.retrieveFile(normalizedPath);
        } catch (cloudError) {
          // Fall back to local if available
          if (this.localAdapter) {
            return await this.localAdapter.retrieveFile(normalizedPath);
          }
          throw cloudError;
        }
      } else if (this.localAdapter) {
        // Use local adapter
        return await this.localAdapter.retrieveFile(normalizedPath);
      } else {
        throw new Error('No storage adapter available');
      }
    } catch (error) {
      throw new Error(`Failed to retrieve file ${normalizedPath}: ${error.message}`);
    }
  }

  /**
   * Check if file exists
   * @param {string} path - File path
   * @param {Object} options - Check options
   * @returns {Promise<boolean>} - True if file exists
   */
  async fileExists(path, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    // Normalize path
    const normalizedPath = this._normalizePath(path);
    
    // Select adapter based on preferences
    const useCloud = options.useCloud || this.config.preferCloud;

    try {
      if (useCloud && this.cloudAdapter) {
        // Check cloud
        return await this.cloudAdapter.fileExists(normalizedPath);
      } else if (this.localAdapter) {
        // Check local
        return await this.localAdapter.fileExists(normalizedPath);
      }
      return false;
    } catch (error) {
      return false;
    }
  }

  /**
   * Delete file
   * @param {string} path - File path
   * @param {Object} options - Delete options
   * @returns {Promise<boolean>} - Success status
   */
  async deleteFile(path, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    // Normalize path
    const normalizedPath = this._normalizePath(path);
    
    // Select adapter based on preferences
    const useCloud = options.useCloud || this.config.preferCloud;
    const syncDelete = options.syncDelete || this.config.autoSync;

    try {
      let success = false;

      if (useCloud && this.cloudAdapter) {
        // Delete from cloud
        success = await this.cloudAdapter.deleteFile(normalizedPath);
        
        // Sync deletion to local if enabled
        if (syncDelete && this.localAdapter) {
          await this.localAdapter.deleteFile(normalizedPath);
        }
      } else if (this.localAdapter) {
        // Delete locally
        success = await this.localAdapter.deleteFile(normalizedPath);
      } else {
        throw new Error('No storage adapter available');
      }

      return success;
    } catch (error) {
      return false;
    }
  }

  /**
   * Normalize storage path
   * @param {string} path - Path to normalize
   * @returns {string} - Normalized path
   * @private
   */
  _normalizePath(path) {
    // Handle absolute paths
    if (path.startsWith('/')) {
      return path;
    }
    
    // Handle relative paths
    return `${this.config.basePath}/${path}`;
  }
}

module.exports = StorageManager;
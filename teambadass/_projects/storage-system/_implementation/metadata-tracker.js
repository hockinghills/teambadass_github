/**
 * MetadataTracker Component
 * Tracks file metadata and versions
 * 
 * FILE_OVERVIEW: File metadata management and versioning
 * VERSION: 1.0.0
 * LAST_UPDATED: 2025-05-03
 * DEPENDENCIES: StorageManager (optional)
 * 
 * TABLE_OF_CONTENTS:
 * 1. Core Tracking - Initialization and configuration
 * 2. Metadata Management - Creation, updating, and retrieval
 * 3. Version History - Tracking file versions and changes
 * 
 * SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
 */

class MetadataTracker {
  /**
   * Create a new metadata tracker
   * @param {Object} options - Configuration options
   */
  constructor(options = {}) {
    this.basePath = options.basePath || '/home/louthenw/Documents/teambadass_github/teambadass/_projects/storage-system/_data/.metadata';
    this.storageManager = options.storageManager || null;
    this.localAdapter = options.localAdapter || null;
    this.initialized = false;
    this.metadata = {};
  }

  /**
   * Initialize metadata tracker
   * @returns {Promise<boolean>} Success status
   */
  async initialize() {
    try {
      // Create metadata directory if it doesn't exist
      if (this.localAdapter) {
        await this.localAdapter.createDirectory(this.basePath);
      } else if (this.storageManager) {
        const adapter = this.storageManager.localAdapter;
        if (adapter) {
          await adapter.createDirectory(this.basePath);
        }
      } else {
        // Create directory using MCP directly if no adapter is available
        try {
          await fs.create_directory({ path: this.basePath });
        } catch (dirError) {
          // Directory might already exist, which is fine
        }
      }

      // Load existing metadata
      await this.loadMetadata();

      this.initialized = true;
      return true;
    } catch (error) {
      console.error(`Metadata tracker initialization failed: ${error.message}`);
      return false;
    }
  }

  /**
   * Load metadata from storage
   * @returns {Promise<Object>} Loaded metadata
   */
  async loadMetadata() {
    try {
      const indexPath = `${this.basePath}/index.json`;
      let content = null;
      
      // Try to read the index file
      if (this.storageManager) {
        // Check if index exists
        const exists = await this.storageManager.fileExists(indexPath);
        
        if (exists) {
          // Read from storage manager
          content = await this.storageManager.retrieveFile(indexPath);
        }
      } else if (this.localAdapter) {
        // Check if index exists
        const exists = await this.localAdapter.fileExists(indexPath);
        
        if (exists) {
          // Read from local adapter
          content = await this.localAdapter.retrieveFile(indexPath);
        }
      } else {
        // Direct file access using MCP
        try {
          content = await fs.read_file({ path: indexPath });
        } catch (readError) {
          // File might not exist yet, which is fine
        }
      }
      
      // Parse content if available
      if (content) {
        this.metadata = JSON.parse(content);
      }

      return this.metadata;
    } catch (error) {
      // If loading fails, start with empty metadata
      this.metadata = {};
      return this.metadata;
    }
  }

  /**
   * Save metadata to storage
   * @returns {Promise<boolean>} Success status
   */
  async saveMetadata() {
    try {
      const indexPath = `${this.basePath}/index.json`;
      const content = JSON.stringify(this.metadata, null, 2);
      
      if (this.storageManager) {
        // Save using storage manager
        await this.storageManager.storeFile(indexPath, content);
      } else if (this.localAdapter) {
        // Save using local adapter
        await this.localAdapter.storeFile(indexPath, content);
      } else {
        // Direct file access using MCP
        
        // Ensure directory exists
        try {
          await fs.create_directory({ path: this.basePath });
        } catch (dirError) {
          // Directory might already exist, which is fine
        }
        
        // Write file
        await fs.write_file({
          path: indexPath,
          content
        });
      }

      return true;
    } catch (error) {
      console.error(`Failed to save metadata: ${error.message}`);
      return false;
    }
  }

  /**
   * Track file metadata
   * @param {string} path - File path
   * @param {Object} fileDetails - File details
   * @returns {Promise<Object>} Updated metadata record
   */
  async trackFile(path, fileDetails) {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      // Create or update metadata record
      if (!this.metadata[path]) {
        // New file
        this.metadata[path] = {
          path,
          size: fileDetails.size || 0,
          created: new Date().toISOString(),
          modified: new Date().toISOString(),
          versions: []
        };
      }

      // Add version
      const version = {
        timestamp: new Date().toISOString(),
        size: fileDetails.size || 0,
        hash: fileDetails.hash || null
      };

      // Add to versions
      this.metadata[path].versions.push(version);
      
      // Update modification timestamp
      this.metadata[path].modified = version.timestamp;
      
      // Update size
      this.metadata[path].size = fileDetails.size || 0;

      // Save updated metadata
      await this.saveMetadata();

      return this.metadata[path];
    } catch (error) {
      console.error(`Failed to track file ${path}: ${error.message}`);
      return null;
    }
  }

  /**
   * Get file metadata
   * @param {string} path - File path
   * @returns {Promise<Object>} Metadata record
   */
  async getMetadata(path) {
    if (!this.initialized) {
      await this.initialize();
    }

    return this.metadata[path] || null;
  }

  /**
   * List all tracked files
   * @returns {Promise<string[]>} List of file paths
   */
  async listTrackedFiles() {
    if (!this.initialized) {
      await this.initialize();
    }

    return Object.keys(this.metadata);
  }

  /**
   * Get file version history
   * @param {string} path - File path
   * @returns {Promise<Object[]>} Version history
   */
  async getVersionHistory(path) {
    if (!this.initialized) {
      await this.initialize();
    }

    const record = this.metadata[path];
    return record ? record.versions : [];
  }

  /**
   * Delete file metadata
   * @param {string} path - File path
   * @returns {Promise<boolean>} Success status
   */
  async deleteMetadata(path) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (this.metadata[path]) {
      delete this.metadata[path];
      await this.saveMetadata();
      return true;
    }

    return false;
  }
  
  /**
   * Search metadata by criteria
   * @param {Function} filterFn - Filter function
   * @returns {Promise<Object[]>} Matching metadata records
   */
  async searchMetadata(filterFn) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    const results = [];
    
    for (const path in this.metadata) {
      if (filterFn(this.metadata[path])) {
        results.push(this.metadata[path]);
      }
    }
    
    return results;
  }
  
  /**
   * Get statistics about tracked files
   * @returns {Promise<Object>} Statistics object
   */
  async getStatistics() {
    if (!this.initialized) {
      await this.initialize();
    }
    
    const fileCount = Object.keys(this.metadata).length;
    let totalSize = 0;
    let totalVersions = 0;
    
    for (const path in this.metadata) {
      const file = this.metadata[path];
      totalSize += file.size || 0;
      totalVersions += file.versions.length;
    }
    
    return {
      fileCount,
      totalSize,
      totalVersions,
      averageSize: fileCount > 0 ? Math.round(totalSize / fileCount) : 0,
      averageVersions: fileCount > 0 ? (totalVersions / fileCount).toFixed(1) : 0
    };
  }
}

module.exports = MetadataTracker;
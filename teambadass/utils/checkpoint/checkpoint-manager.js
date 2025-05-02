/**
 * TeamBadass Checkpoint Manager
 * Resilient implementation tracking with recovery capabilities
 * 
 * FILE_OVERVIEW: Implementation tracking and recovery system
 * VERSION: 1.0.0
 * LAST_UPDATED: 2025-05-03
 * DEPENDENCIES: fs-helper.js
 * 
 * TABLE_OF_CONTENTS:
 * 1. Core Checkpoint Management - Loading, saving, verification
 * 2. Component Tracking - Status of individual components
 * 3. Implementation Plan - Component sequencing and dependencies
 * 4. Recovery Operations - Session resumption and integrity checking
 * 
 * SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
 */

const fs = require('fs');
const path = require('path');
const fsHelper = require('../fs-helper');

/**
 * Checkpoint Manager for tracking implementation progress
 */
class CheckpointManager {
  /**
   * Create a new checkpoint manager
   * @param {Object} options - Configuration options
   */
  constructor(options = {}) {
    // Base paths and configuration
    this.repoPath = options.repoPath || '/home/louthenw/Documents/teambadass_github/teambadass';
    this.checkpointPath = options.checkpointPath || path.join(this.repoPath, 'checkpoint.json');
    this.backupPath = options.backupPath || path.join(this.repoPath, 'checkpoint.backup.json');
    this.projectName = options.projectName || 'default-project';
    this.verbose = options.verbose !== false;
    
    // State tracking
    this.initialized = false;
    this.recoveryMode = false;
    
    // Checkpoint data
    this.checkpoint = {
      project: this.projectName,
      last_update: new Date().toISOString(),
      last_completed: null,
      next_component: null,
      components_completed: [],
      components_pending: [],
      session_count: 0,
      first_session: new Date().toISOString(),
      current_session: new Date().toISOString()
    };
  }

  /**
   * Initialize the checkpoint system
   * @returns {Promise<Object>} Initialization status
   */
  async initialize() {
    try {
      // Try to load existing checkpoint
      const loaded = await this.loadCheckpoint();
      
      if (loaded) {
        this.log(`Checkpoint loaded for project: ${this.checkpoint.project}`);
        
        // Update session tracking
        this.checkpoint.session_count++;
        this.checkpoint.current_session = new Date().toISOString();
        
        // Check for recovery mode
        if (this.checkpoint.components_pending.length > 0) {
          this.recoveryMode = true;
          this.log(`Recovery mode activated - resuming from: ${this.checkpoint.next_component}`);
        }
      } else {
        this.log(`New checkpoint created for project: ${this.projectName}`);
      }
      
      // Save updated checkpoint
      await this.saveCheckpoint();
      
      this.initialized = true;
      return {
        status: 'success',
        recoveryMode: this.recoveryMode,
        nextComponent: this.checkpoint.next_component,
        completedCount: this.checkpoint.components_completed.length,
        pendingCount: this.checkpoint.components_pending.length
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
   * Load checkpoint from file
   * @returns {Promise<boolean>} Success status
   */
  async loadCheckpoint() {
    try {
      // Check if checkpoint file exists
      const exists = await fsHelper.pathExists(this.checkpointPath);
      
      if (!exists) {
        return false;
      }
      
      // Load checkpoint data
      const content = await fs.read_file({ path: this.checkpointPath });
      const data = JSON.parse(content);
      
      // Update checkpoint
      this.checkpoint = {
        ...this.checkpoint,
        ...data
      };
      
      return true;
    } catch (error) {
      this.log(`Error loading checkpoint: ${error.message}`, 'warning');
      
      // Try loading from backup
      try {
        const backupExists = await fsHelper.pathExists(this.backupPath);
        
        if (backupExists) {
          this.log('Attempting to load from backup checkpoint', 'warning');
          const backupContent = await fs.read_file({ path: this.backupPath });
          const backupData = JSON.parse(backupContent);
          
          this.checkpoint = {
            ...this.checkpoint,
            ...backupData
          };
          
          this.log('Successfully loaded from backup checkpoint', 'warning');
          return true;
        }
      } catch (backupError) {
        this.log(`Backup loading failed: ${backupError.message}`, 'error');
      }
      
      return false;
    }
  }

  /**
   * Save checkpoint to file
   * @returns {Promise<boolean>} Success status
   */
  async saveCheckpoint() {
    try {
      // Update timestamp
      this.checkpoint.last_update = new Date().toISOString();
      
      // Create backup of existing checkpoint if it exists
      const exists = await fsHelper.pathExists(this.checkpointPath);
      
      if (exists) {
        // Read current checkpoint
        const currentContent = await fs.read_file({ path: this.checkpointPath });
        
        // Write to backup
        await fsHelper.writeFile(this.backupPath, currentContent);
      }
      
      // Write updated checkpoint
      await fsHelper.writeFile(
        this.checkpointPath,
        JSON.stringify(this.checkpoint, null, 2)
      );
      
      return true;
    } catch (error) {
      this.log(`Error saving checkpoint: ${error.message}`, 'error');
      return false;
    }
  }

  /**
   * Get implementation status
   * @returns {Object} Current status
   */
  getStatus() {
    return {
      project: this.checkpoint.project,
      recoveryMode: this.recoveryMode,
      lastCompleted: this.checkpoint.last_completed,
      nextComponent: this.checkpoint.next_component,
      completed: this.checkpoint.components_completed,
      pending: this.checkpoint.components_pending,
      sessionCount: this.checkpoint.session_count,
      progress: this.calculateProgress()
    };
  }

  /**
   * Calculate implementation progress
   * @returns {Object} Progress metrics
   */
  calculateProgress() {
    const total = this.checkpoint.components_completed.length + this.checkpoint.components_pending.length;
    const completed = this.checkpoint.components_completed.length;
    
    return {
      total: total,
      completed: completed,
      pending: this.checkpoint.components_pending.length,
      percentage: total > 0 ? Math.round((completed / total) * 100) : 0
    };
  }

  /**
   * Set implementation plan with ordered components
   * @param {Array<string>} components - Ordered list of components
   * @returns {Promise<boolean>} Success status
   */
  async setImplementationPlan(components) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    // Filter out already completed components
    const pendingComponents = components.filter(
      component => !this.checkpoint.components_completed.includes(component)
    );
    
    // Update pending components
    this.checkpoint.components_pending = pendingComponents;
    
    // Set next component
    if (pendingComponents.length > 0) {
      this.checkpoint.next_component = pendingComponents[0];
    } else {
      this.checkpoint.next_component = null;
    }
    
    // Save changes
    const saved = await this.saveCheckpoint();
    
    if (saved) {
      this.log(`Implementation plan set with ${pendingComponents.length} pending components`);
    }
    
    return saved;
  }

  /**
   * Complete a component
   * @param {string} component - Component name
   * @returns {Promise<Object>} Completion status
   */
  async completeComponent(component) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    try {
      // Check if component is already completed
      if (this.checkpoint.components_completed.includes(component)) {
        return {
          status: 'already_completed',
          component: component
        };
      }
      
      // Update completed components
      this.checkpoint.components_completed.push(component);
      this.checkpoint.last_completed = component;
      
      // Remove from pending components
      const pendingIndex = this.checkpoint.components_pending.indexOf(component);
      
      if (pendingIndex !== -1) {
        this.checkpoint.components_pending.splice(pendingIndex, 1);
      }
      
      // Update next component
      if (this.checkpoint.components_pending.length > 0) {
        this.checkpoint.next_component = this.checkpoint.components_pending[0];
      } else {
        this.checkpoint.next_component = null;
      }
      
      // Save changes
      await this.saveCheckpoint();
      
      this.log(`Component completed: ${component}`);
      
      return {
        status: 'success',
        component: component,
        next: this.checkpoint.next_component,
        progress: this.calculateProgress()
      };
    } catch (error) {
      this.log(`Error completing component: ${error.message}`, 'error');
      
      return {
        status: 'error',
        message: error.message
      };
    }
  }

  /**
   * Check if component is already completed
   * @param {string} component - Component name
   * @returns {boolean} Completion status
   */
  isCompleted(component) {
    return this.checkpoint.components_completed.includes(component);
  }

  /**
   * Get next component to implement
   * @returns {string|null} Next component
   */
  getNextComponent() {
    return this.checkpoint.next_component;
  }

  /**
   * Log a message if verbose mode enabled
   * @param {string} message - Message to log
   * @param {string} level - Log level
   */
  log(message, level = 'info') {
    if (!this.verbose && level === 'info') {
      return;
    }
    
    const prefix = {
      info: '📋 CHECKPOINT:',
      warning: '⚠️ CHECKPOINT:',
      error: '❌ CHECKPOINT:',
    }[level] || '   ';
    
    console.log(`${prefix} ${message}`);
  }
}

module.exports = CheckpointManager;

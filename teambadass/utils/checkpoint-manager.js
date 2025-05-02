/**
 * TeamBadass Checkpoint Manager
 * Tracks implementation progress and enables recovery
 * 
 * FILE_OVERVIEW: Resilient implementation progress tracking
 * VERSION: 1.0.0
 * LAST_UPDATED: 2025-05-03
 * DEPENDENCIES: fs-helper.js
 * 
 * TABLE_OF_CONTENTS:
 * 1. Checkpoint Management - Core progress tracking
 * 2. Component Tracking - Implementation state management
 * 3. Recovery Procedures - Handling interrupted sessions
 * 4. Filesystem Operations - Safe state persistence
 * 
 * SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
 */

const path = require('path');
const fsHelper = require('./fs-helper');

/**
 * Manages implementation checkpoints for resilient development
 */
class CheckpointManager {
  /**
   * Create a new checkpoint manager
   * @param {Object} options - Configuration options
   * @param {string} options.checkpointPath - Path to checkpoint file
   * @param {string} options.projectName - Name of current project
   */
  constructor(options = {}) {
    this.checkpointPath = options.checkpointPath || 
      '/home/louthenw/Documents/teambadass_github/teambadass/checkpoint.json';
    this.projectName = options.projectName || 'default';
    this.checkpoints = {
      project: this.projectName,
      last_update: new Date().toISOString(),
      last_completed: null,
      next_component: null,
      components_completed: [],
      components_pending: [],
      recovery_mode: false
    };
    this.loaded = false;
  }

  /**
   * Initialize the checkpoint system
   * @returns {Promise<boolean>} Success status
   */
  async initialize() {
    try {
      // Always try to load existing checkpoint first
      await this.loadCheckpoint();
      return true;
    } catch (error) {
      // Create new checkpoint file if it doesn't exist
      return this.saveCheckpoint();
    }
  }

  /**
   * Load checkpoint from file
   * @returns {Promise<Object>} Loaded checkpoint data
   */
  async loadCheckpoint() {
    try {
      // Check if checkpoint file exists
      const exists = await fsHelper.pathExists(this.checkpointPath);
      if (!exists) {
        this.loaded = true;
        return this.checkpoints;
      }
      
      // Load checkpoint data
      const content = await fs.read_file({ path: this.checkpointPath });
      this.checkpoints = JSON.parse(content);
      this.loaded = true;
      
      // Activate recovery mode if needed
      if (this.checkpoints.next_component && !this.checkpoints.recovery_mode) {
        this.checkpoints.recovery_mode = true;
        await this.saveCheckpoint();
      }
      
      return this.checkpoints;
    } catch (error) {
      console.error(`Error loading checkpoint: ${error.message}`);
      this.loaded = true;
      return this.checkpoints;
    }
  }

  /**
   * Save checkpoint to file
   * @returns {Promise<boolean>} Success status
   */
  async saveCheckpoint() {
    try {
      // Update timestamp
      this.checkpoints.last_update = new Date().toISOString();
      
      // Ensure parent directory exists
      await fsHelper.ensureDirectory(path.dirname(this.checkpointPath));
      
      // Create backup of current checkpoint if it exists
      try {
        const exists = await fsHelper.pathExists(this.checkpointPath);
        if (exists) {
          const backupPath = `${this.checkpointPath}.bak`;
          await fsHelper.writeFile(backupPath, await fs.read_file({ path: this.checkpointPath }));
        }
      } catch (backupError) {
        console.error(`Backup creation failed: ${backupError.message}`);
        // Continue with save even if backup fails
      }
      
      // Save checkpoint
      await fsHelper.writeFile(
        this.checkpointPath, 
        JSON.stringify(this.checkpoints, null, 2)
      );
      
      return true;
    } catch (error) {
      console.error(`Error saving checkpoint: ${error.message}`);
      return false;
    }
  }
  
  /**
   * Mark a component as completed and update next component
   * @param {string} componentName - Name of completed component
   * @returns {Promise<boolean>} Success status
   */
  async completeComponent(componentName) {
    if (!this.loaded) await this.initialize();
    
    // Update completion status
    this.checkpoints.last_completed = componentName;
    
    // Move from pending to completed
    const pendingIndex = this.checkpoints.components_pending.indexOf(componentName);
    if (pendingIndex > -1) {
      this.checkpoints.components_pending.splice(pendingIndex, 1);
    }
    
    // Add to completed if not already there
    if (!this.checkpoints.components_completed.includes(componentName)) {
      this.checkpoints.components_completed.push(componentName);
    }
    
    // Set next component
    this.checkpoints.next_component = 
      this.checkpoints.components_pending.length > 0 ? 
      this.checkpoints.components_pending[0] : null;
    
    return this.saveCheckpoint();
  }

  /**
   * Check if component is already completed
   * @param {string} componentName - Component to check
   * @returns {boolean} True if component is completed
   */
  isCompleted(componentName) {
    return this.checkpoints.components_completed.includes(componentName);
  }
  
  /**
   * Get next component to implement
   * @returns {string|null} Name of next component or null if done
   */
  getNextComponent() {
    return this.checkpoints.next_component;
  }
  
  /**
   * Set implementation plan with ordered components
   * @param {string[]} components - Array of component names in implementation order
   * @returns {Promise<boolean>} Success status
   */
  async setImplementationPlan(components) {
    if (!this.loaded) await this.initialize();
    
    // Filter out completed components
    const pendingComponents = components.filter(
      component => !this.checkpoints.components_completed.includes(component)
    );
    
    this.checkpoints.components_pending = pendingComponents;
    
    // Set next component if there are pending components
    if (pendingComponents.length > 0) {
      this.checkpoints.next_component = pendingComponents[0];
    }
    
    return this.saveCheckpoint();
  }
  
  /**
   * Check if we're in recovery mode
   * @returns {boolean} True if recovering from interruption
   */
  isRecovery() {
    return this.checkpoints.recovery_mode;
  }
  
  /**
   * Clear recovery mode after successful recovery
   * @returns {Promise<boolean>} Success status
   */
  async clearRecovery() {
    this.checkpoints.recovery_mode = false;
    return this.saveCheckpoint();
  }
  
  /**
   * Get implementation status summary
   * @returns {Object} Status summary
   */
  getStatus() {
    const completed = this.checkpoints.components_completed.length;
    const pending = this.checkpoints.components_pending.length;
    const total = completed + pending;
    const progress = total > 0 ? Math.round((completed / total) * 100) : 100;
    
    return {
      project: this.checkpoints.project,
      completed: completed,
      pending: pending,
      total: total,
      progress: progress,
      last_completed: this.checkpoints.last_completed,
      next_component: this.checkpoints.next_component,
      recovery_mode: this.checkpoints.recovery_mode,
      last_update: this.checkpoints.last_update
    };
  }
}

module.exports = CheckpointManager;

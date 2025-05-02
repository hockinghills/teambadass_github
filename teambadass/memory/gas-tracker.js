/**
 * TeamBadass Gas Tracker
 * Monitors and records Claude's processing capacity with minimal overhead
 */

const fsHelper = require('../utils/fs-helper');

const BASE_PATH = '/home/louthenw/Documents/teambadass_github/teambadass';
const CONFIG_PATH = `${BASE_PATH}/memory/config/system.json`;
const METRICS_PATH = `${BASE_PATH}/memory/metrics`;

const gasTracker = {
  // Tracking state
  state: {
    startTime: new Date(),
    sessionId: `session-${Date.now()}`,
    initialMeasurement: true,
    operations: [],
    currentUsage: 0,
    thresholds: {
      warning: 60,
      hardStop: 90
    },
    warningObserved: false,
    warningUsage: null,
    hardStopObserved: false,
    hardStopUsage: null
  },
  
  /**
   * Initialize the gas tracker
   * @returns {Promise<object>} Initialization status
   */
  async initialize() {
    try {
      // Ensure metrics directory exists
      await fsHelper.ensureDirectory(METRICS_PATH);
      
      // Load configuration if available
      try {
        const configContent = await fs.read_file({ path: CONFIG_PATH });
        const config = JSON.parse(configContent);
        
        if (config && config.thresholds) {
          this.state.thresholds = config.thresholds;
        }
      } catch (error) {
        // Config file might not exist yet, that's ok
        console.log('Using default thresholds');
      }
      
      // Record initialization
      this.recordOperation('initialization', { type: 'system' });
      
      return {
        status: 'success',
        sessionId: this.state.sessionId,
        thresholds: this.state.thresholds
      };
    } catch (error) {
      console.error(`Gas tracker initialization error: ${error}`);
      return {
        status: 'error',
        message: error.message
      };
    }
  },
  
  /**
   * Record an operation with gas usage
   * @param {string} operationType - Type of operation
   * @param {object} details - Operation details
   * @returns {object} Updated state
   */
  recordOperation(operationType, details = {}) {
    // Calculate gas usage based on operation type
    const gasUsage = this.calculateGasUsage(operationType, details);
    
    // Add to current usage
    this.state.currentUsage += gasUsage;
    
    // Check if we've hit thresholds
    if (!this.state.warningObserved && this.state.currentUsage >= this.state.thresholds.warning) {
      this.state.warningObserved = true;
      this.state.warningUsage = this.state.currentUsage;
    }
    
    if (!this.state.hardStopObserved && this.state.currentUsage >= this.state.thresholds.hardStop) {
      this.state.hardStopObserved = true;
      this.state.hardStopUsage = this.state.currentUsage;
    }
    
    // Record the operation
    const operation = {
      type: operationType,
      details,
      gasUsage,
      cumulativeUsage: this.state.currentUsage,
      timestamp: new Date().toISOString()
    };
    
    this.state.operations.push(operation);
    
    return {
      operation,
      currentUsage: this.state.currentUsage,
      status: this.getStatus()
    };
  },
  
  /**
   * Calculate gas usage for operation type
   * @param {string} operationType - Type of operation
   * @param {object} details - Operation details
   * @returns {number} Gas usage percentage
   */
  calculateGasUsage(operationType, details = {}) {
    // Base costs for different operation types
    const baseCosts = {
      initialization: 0.5,
      contextLoading: 0.1, // Per KB
      discussion: 0.5,     // Base cost for a small exchange
      code: 2.0,           // Base cost for small code
      search: 2.0,         // Base cost for a simple search
      artifact: 3.0,       // Base cost for a simple artifact
      analysis: 1.0        // Base cost for simple analysis
    };
    
    // Size multipliers
    const sizeFactor = {
      small: 1,
      medium: 2,
      large: 4,
      xlarge: 8
    };
    
    // Complexity multipliers
    const complexityFactor = {
      low: 0.5,
      medium: 1,
      high: 2,
      extreme: 4
    };
    
    // Default values
    const size = details.size || 'small';
    const complexity = details.complexity || 'medium';
    
    // Special case for context loading which is based on KB
    if (operationType === 'contextLoading' && details.kb) {
      return baseCosts.contextLoading * details.kb;
    }
    
    // Get base cost (default to discussion if unknown)
    const baseCost = baseCosts[operationType] || baseCosts.discussion;
    
    // Calculate total cost
    const sizeMultiplier = sizeFactor[size] || 1;
    const complexityMultiplier = complexityFactor[complexity] || 1;
    
    return baseCost * sizeMultiplier * complexityMultiplier;
  },
  
  /**
   * Get current status
   * @returns {string} Status string
   */
  getStatus() {
    if (this.state.currentUsage >= this.state.thresholds.hardStop) {
      return 'CRITICAL';
    } else if (this.state.currentUsage >= this.state.thresholds.warning) {
      return 'WARNING';
    } else if (this.state.currentUsage >= this.state.thresholds.warning * 0.8) {
      return 'CAUTION';
    } else {
      return 'NORMAL';
    }
  },
  
  /**
   * Save current metrics to file
   * @returns {Promise<object>} Save result
   */
  async saveMetrics() {
    try {
      const metrics = {
        sessionId: this.state.sessionId,
        startTime: this.state.startTime.toISOString(),
        endTime: new Date().toISOString(),
        duration: (Date.now() - this.state.startTime) / 1000, // seconds
        finalUsage: this.state.currentUsage,
        status: this.getStatus(),
        thresholds: this.state.thresholds,
        warningObserved: this.state.warningObserved,
        warningUsage: this.state.warningUsage,
        hardStopObserved: this.state.hardStopObserved,
        hardStopUsage: this.state.hardStopUsage,
        operations: this.state.operations,
        operationCounts: this.getOperationCounts()
      };
      
      // Create metrics filename with timestamp
      const timestamp = new Date().toISOString()
        .replace(/:/g, '-')
        .replace(/\..+/, '');
      const metricsFile = `${METRICS_PATH}/gas-${this.state.sessionId}-${timestamp}.json`;
      
      // Save metrics
      await fsHelper.writeFile(metricsFile, JSON.stringify(metrics, null, 2));
      
      return {
        status: 'success',
        path: metricsFile
      };
    } catch (error) {
      console.error(`Error saving metrics: ${error}`);
      return {
        status: 'error',
        message: error.message
      };
    }
  },
  
  /**
   * Get operation counts by type
   * @returns {object} Count by operation type
   */
  getOperationCounts() {
    const counts = {};
    
    for (const op of this.state.operations) {
      if (!counts[op.type]) {
        counts[op.type] = 0;
      }
      counts[op.type]++;
    }
    
    return counts;
  },
  
  /**
   * Register threshold observation
   * @param {string} type - Threshold type (warning, hardStop)
   * @returns {object} Updated thresholds
   */
  registerThreshold(type, value = null) {
    if (type !== 'warning' && type !== 'hardStop') {
      return {
        status: 'error',
        message: `Invalid threshold type: ${type}`
      };
    }
    
    // If value not provided, use current usage
    const newValue = value !== null ? value : this.state.currentUsage;
    
    // Update threshold with weighted average (70% new, 30% old)
    this.state.thresholds[type] = Math.round((newValue * 0.7 + this.state.thresholds[type] * 0.3) * 10) / 10;
    
    // Record observation
    if (type === 'warning') {
      this.state.warningObserved = true;
      this.state.warningUsage = newValue;
    } else {
      this.state.hardStopObserved = true;
      this.state.hardStopUsage = newValue;
    }
    
    return {
      status: 'success',
      thresholds: this.state.thresholds
    };
  },
  
  /**
   * Get complete status report
   * @param {boolean} detailed - Include detailed operation list
   * @returns {object} Status report
   */
  getStatusReport(detailed = false) {
    const now = new Date();
    const duration = (now - this.state.startTime) / 1000 / 60; // minutes
    
    const report = {
      sessionId: this.state.sessionId,
      currentUsage: this.state.currentUsage,
      status: this.getStatus(),
      duration: Math.round(duration * 10) / 10, // 1 decimal place
      operationCount: this.state.operations.length,
      warningObserved: this.state.warningObserved,
      hardStopObserved: this.state.hardStopObserved,
      remaining: Math.max(0, 100 - this.state.currentUsage),
      recommendation: this.getRecommendation()
    };
    
    // Add operation counts
    report.operationCounts = this.getOperationCounts();
    
    // Add detailed operations if requested
    if (detailed) {
      report.operations = this.state.operations;
    }
    
    return report;
  },
  
  /**
   * Get recommendation based on current state
   * @returns {string} Recommendation
   */
  getRecommendation() {
    const usage = this.state.currentUsage;
    
    if (usage >= this.state.thresholds.hardStop) {
      return 'CRITICAL: Hop immediately to avoid data loss';
    } else if (usage >= this.state.thresholds.warning) {
      return 'WARNING: Prepare to wrap up and hop soon';
    } else if (usage >= this.state.thresholds.warning * 0.8) {
      return 'CAUTION: Monitor closely and avoid complex operations';
    } else {
      return 'NORMAL: Continue with planned operations';
    }
  }
};

module.exports = gasTracker;

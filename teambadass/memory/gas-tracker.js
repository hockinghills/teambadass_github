/**
 * TeamBadass Gas Tracker
 * Monitors and records Claude's processing capacity with minimal overhead
 */

const BASE_PATH = "/home/louthenw/Documents/teambadass_github/teambadass";
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
      // Load configuration
      const config = await this._loadConfig();
      
      if (config && config.thresholds) {
        this.state.thresholds = config.thresholds;
      }
      
      // Create metrics path if needed
      await fs.create_directory({
        path: METRICS_PATH
      }).catch(() => {
        /* Directory might already exist, that's fine */
      });
      
      // Record initial state
      await this.
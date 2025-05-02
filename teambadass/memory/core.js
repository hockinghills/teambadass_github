/**
 * TeamBadass Memory System - Core Module
 * Provides persistent storage using filesystem MCP
 */

const BASE_PATH = "/home/louthenw/Documents/teambadass_github/teambadass";

/**
 * Core memory system using filesystem MCP
 */
const memory = {
  /**
   * Store data to memory system
   * @param {string} category - Memory category (sessions, knowledge, metrics)
   * @param {string} id - Unique identifier for data
   * @param {object|string} data - Data to store
   * @returns {Promise<boolean>} - Success status
   */
  async store(category, id, data) {
    try {
      const path = `${BASE_PATH}/memory/${category}/${id}.json`;
      const content = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
      
      await fs.write_file({
        path,
        content
      });
      
      return true;
    } catch (error) {
      console.error(`Error storing memory: ${error}`);
      return false;
    }
  },
  
  /**
   * Retrieve data from memory system
   * @param {string} category - Memory category
   * @param {string} id - Unique identifier for data
   * @returns {Promise<object|null>} - Retrieved data or null if not found
   */
  async retrieve(category, id) {
    try {
      const path = `${BASE_PATH}/memory/${category}/${id}.json`;
      
      const content = await fs.read_file({
        path
      });
      
      return JSON.parse(content);
    } catch (error) {
      // File might not exist yet, that's ok
      return null;
    }
  },
  
  /**
   * List memory entries in a category
   * @param {string} category - Memory category
   * @returns {Promise<string[]>} - List of memory IDs
   */
  async list(category) {
    try {
      const path = `${BASE_PATH}/memory/${category}`;
      
      const contents = await fs.list_directory({
        path
      });
      
      // Convert directory listing to memory IDs
      return contents
        .filter(item => item.startsWith('[FILE]'))
        .map(item => {
          const filename = item.replace('[FILE] ', '');
          return filename.replace('.json', '');
        });
    } catch (error) {
      console.error(`Error listing memory: ${error}`);
      return [];
    }
  },
  
  /**
   * Record session metrics
   * @param {string} sessionId - Current session ID
   * @param {object} metrics - Session metrics data
   * @returns {Promise<boolean>} - Success status
   */
  async recordMetrics(sessionId, metrics) {
    const timestamp = new Date().toISOString().replace(/:/g, '-');
    const id = `${sessionId}-${timestamp}`;
    
    return this.store('metrics', id, {
      sessionId,
      timestamp,
      metrics
    });
  },
  
  /**
   * Store session info
   * @param {string} sessionId - Session identifier
   * @param {object} sessionData - Session data
   * @returns {Promise<boolean>} - Success status
   */
  async storeSession(sessionId, sessionData) {
    return this.store('sessions', sessionId, sessionData);
  },
  
  /**
   * Store knowledge item
   * @param {string} topic - Knowledge topic
   * @param {object} data - Knowledge data
   * @returns {Promise<boolean>} - Success status
   */
  async storeKnowledge(topic, data) {
    const timestamp = new Date().toISOString().slice(0, 10);
    const id = `${topic}-${timestamp}`;
    
    return this.store('knowledge', id, data);
  }
};

module.exports = memory;

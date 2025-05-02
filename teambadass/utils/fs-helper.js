/**
 * TeamBadass FileSystem Helper
 * Provides efficient filesystem operations with caching
 */

const fsHelper = {
  // Cache storage
  _cache: {
    directoryTree: null,
    lastTreeUpdate: null,
    // Cache duration in milliseconds (30 minutes)
    cacheDuration: 30 * 60 * 1000,
  },
  
  /**
   * Get directory tree with caching
   * @param {string} basePath - Base path to get tree for
   * @param {boolean} forceRefresh - Force fresh tree even if cache exists
   * @returns {Promise<object>} Directory tree
   */
  async getDirectoryTree(basePath = '/home/louthenw/Documents/teambadass_github/teambadass', forceRefresh = false) {
    const cacheValid = this._cache.directoryTree && 
                       this._cache.lastTreeUpdate && 
                       (Date.now() - this._cache.lastTreeUpdate < this._cache.cacheDuration);
    
    if (!cacheValid || forceRefresh) {
      try {
        // Fetch fresh directory tree using MCP function
        // This returns a JSON string, so we need to parse it
        const treeResponse = await directory_tree({ path: basePath });
        this._cache.directoryTree = JSON.parse(treeResponse);
        this._cache.lastTreeUpdate = Date.now();
      } catch (error) {
        console.error(`Error getting directory tree: ${error}`);
        // Return empty tree if we can't get a fresh one
        return { name: basePath, type: 'directory', children: [] };
      }
    }
    
    return this._cache.directoryTree;
  },
  
  /**
   * Check if path exists in directory tree
   * @param {string} path - Path to check
   * @param {object} tree - Directory tree (optional, will fetch if not provided)
   * @returns {Promise<boolean>} True if path exists
   */
  async pathExists(path, tree = null) {
    // Get tree if not provided
    if (!tree) {
      tree = await this.getDirectoryTree();
    }
    
    // Normalize path to remove trailing slash
    const normalizedPath = path.endsWith('/') ? path.slice(0, -1) : path;
    
    // Function to search tree
    const searchTree = (node, remainingPath) => {
      // If we've found the target node, we're done
      if (remainingPath === '' || remainingPath === '/' || remainingPath === node.name) {
        return true;
      }
      
      // If this isn't a directory, we can't go deeper
      if (node.type !== 'directory' || !node.children) {
        return false;
      }
      
      // Split path into current dir and remaining path
      const parts = remainingPath.split('/');
      const currentDir = parts[0] || '/';
      const nextPathPart = parts.slice(1).join('/');
      
      // Look for matching child
      for (const child of node.children) {
        // If child name matches, search that subtree
        if (child.name === currentDir) {
          return searchTree(child, nextPathPart);
        }
      }
      
      // No matching child found
      return false;
    };
    
    // Start search from root
    return searchTree(tree, normalizedPath);
  },
  
  /**
   * Ensure directory exists, creating it if needed
   * @param {string} path - Directory path
   * @returns {Promise<boolean>} Success status
   */
  async ensureDirectory(path) {
    try {
      // Check if directory already exists
      const exists = await this.pathExists(path);
      
      if (!exists) {
        // Create directory if it doesn't exist
        await create_directory({ path });
        // Invalidate cache since we modified the structure
        this._cache.lastTreeUpdate = null;
      }
      
      return true;
    } catch (error) {
      console.error(`Error ensuring directory exists: ${error}`);
      return false;
    }
  },
  
  /**
   * Create file with path verification
   * @param {string} path - File path
   * @param {string} content - File content
   * @returns {Promise<boolean>} Success status
   */
  async writeFile(path, content) {
    try {
      // Ensure parent directory exists
      const lastSlash = path.lastIndexOf('/');
      if (lastSlash > 0) {
        const dirPath = path.substring(0, lastSlash);
        await this.ensureDirectory(dirPath);
      }
      
      // Write file
      await write_file({ path, content });
      return true;
    } catch (error) {
      console.error(`Error writing file: ${error}`);
      return false;
    }
  },
  
  /**
   * Generate simplified ASCII directory tree for README
   * @param {string} basePath - Base path to start from
   * @param {number} depth - Maximum tree depth
   * @returns {Promise<string>} ASCII directory tree
   */
  async generateAsciiTree(basePath = '/home/louthenw/Documents/teambadass_github/teambadass', depth = 2) {
    const tree = await this.getDirectoryTree(basePath, true);
    let result = `${basePath}\n`;
    
    const buildTree = (node, prefix = '', depth = 2, currentDepth = 0) => {
      if (currentDepth > depth) return;
      
      if (!node.children) return;
      
      // Sort children - directories first, then files
      const sorted = [...node.children].sort((a, b) => {
        if (a.type === b.type) return a.name.localeCompare(b.name);
        return a.type === 'directory' ? -1 : 1;
      });
      
      // Last item flag for line drawing
      const count = sorted.length;
      
      sorted.forEach((child, index) => {
        const isLast = index === count - 1;
        const linePrefix = isLast ? '└── ' : '├── ';
        const childPrefix = isLast ? '    ' : '│   ';
        
        result += `${prefix}${linePrefix}${child.name}${child.type === 'directory' ? '/' : ''}\n`;
        
        if (child.type === 'directory' && child.children && child.children.length > 0 && currentDepth < depth) {
          buildTree(child, prefix + childPrefix, depth, currentDepth + 1);
        }
      });
    };
    
    buildTree(tree, '', depth);
    return result;
  }
};

module.exports = fsHelper;

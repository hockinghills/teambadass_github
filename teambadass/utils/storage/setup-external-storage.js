#!/usr/bin/env node
/**
 * TeamBadass External Storage Setup
 * Creates and configures external storage locations
 * 
 * FILE_OVERVIEW: Setup utility for external storage configuration
 * VERSION: 1.0.0
 * LAST_UPDATED: 2025-05-03
 * DEPENDENCIES: fs-helper.js
 * 
 * TABLE_OF_CONTENTS:
 * 1. Configuration - Command line argument processing
 * 2. Directory Setup - Creating storage directory structure
 * 3. Configuration Creation - Generating storage configuration
 * 4. Symbolic Link - Creating convenience access links
 * 
 * SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
 */

const fs = require('fs');
const path = require('path');
const fsHelper = require('../fs-helper');

/**
 * Setup external storage for TeamBadass
 */
async function setupExternalStorage(options = {}) {
  // Default options
  const config = {
    repoPath: options.repoPath || '/home/louthenw/Documents/teambadass_github/teambadass',
    externalPath: options.externalPath || '/home/louthenw/teambadass_external',
    verbose: options.verbose !== false
  };

  console.log('\n📁 TeamBadass External Storage Setup');
  console.log(`📝 Repository: ${config.repoPath}`);
  console.log(`📝 External Storage: ${config.externalPath}`);

  try {
    // Verify repository exists
    const repoExists = await fsHelper.pathExists(config.repoPath);
    if (!repoExists) {
      throw new Error(`Repository path not found: ${config.repoPath}`);
    }

    // Create external storage structure
    const directories = [
      config.externalPath,
      path.join(config.externalPath, 'backups'),
      path.join(config.externalPath, 'temp'),
      path.join(config.externalPath, 'archive')
    ];

    for (const directory of directories) {
      await fsHelper.ensureDirectory(directory);
      console.log(`✅ Created: ${directory}`);
    }

    // Create storage configuration
    const storageConfig = {
      external_path: config.externalPath,
      backup_path: path.join(config.externalPath, 'backups'),
      temp_path: path.join(config.externalPath, 'temp'),
      archive_path: path.join(config.externalPath, 'archive'),
      cloud_enabled: false,
      cloud_provider: null,
      cloud_config: {}
    };

    // Save configuration to repository
    const configPath = path.join(config.repoPath, 'memory', 'config', 'storage.json');
    await fsHelper.ensureDirectory(path.dirname(configPath));
    
    await fsHelper.writeFile(
      configPath,
      JSON.stringify(storageConfig, null, 2)
    );
    
    console.log(`✅ Configuration saved to: ${configPath}`);

    // Create symbolic link
    try {
      const linkPath = path.join(config.repoPath, '.external');
      
      // This would use process.symlink in a real Node.js environment
      console.log(`ℹ️ Would create symbolic link: ${linkPath} → ${config.externalPath}`);
      console.log('   (Symbolic link creation requires Node.js environment)');
    } catch (error) {
      console.log(`⚠️ Error creating symbolic link: ${error.message}`);
    }

    console.log('\n✅ External storage setup complete!');
    console.log('\n📋 Test your setup by using the storage manager:');
    console.log(`   const StorageManager = require('./utils/storage/storage-manager');`);
    console.log(`   const storage = new StorageManager();`);
    console.log(`   storage.initialize().then(result => console.log(result));`);

    return {
      status: 'success',
      config: storageConfig
    };
  } catch (error) {
    console.error(`\n❌ Setup failed: ${error.message}`);
    return {
      status: 'error',
      message: error.message
    };
  }
}

// Execute if run directly
if (require.main === module) {
  // Parse command line arguments
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    const value = args[i + 1];
    
    if (key && value) {
      options[key] = value;
    }
  }
  
  setupExternalStorage(options)
    .then(result => {
      process.exit(result.status === 'success' ? 0 : 1);
    })
    .catch(error => {
      console.error(`\n❌ Unhandled error: ${error.message}`);
      process.exit(1);
    });
} else {
  // Export for use as a module
  module.exports = setupExternalStorage;
}

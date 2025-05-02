/**
 * Storage System Test Script
 * Comprehensive test for the TeamBadass Storage System
 * 
 * FILE_OVERVIEW: Test suite for storage system components
 * VERSION: 1.0.0
 * LAST_UPDATED: 2025-05-03
 * DEPENDENCIES: All storage system components
 * 
 * TABLE_OF_CONTENTS:
 * 1. Test Setup - Configuration and initialization
 * 2. Local Storage Tests - Local adapter functionality
 * 3. Cloud Storage Tests - Cloud adapter functionality
 * 4. Metadata Tests - Metadata tracking functionality
 * 5. Integration Tests - Complete system functionality
 * 
 * SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
 */

// Import components
const StorageManager = require('./storage-manager');
const LocalAdapter = require('./local-adapter');
const CloudAdapter = require('./cloud-adapter');
const MetadataTracker = require('./metadata-tracker');

/**
 * Storage System Test Suite
 * Tests all components of the storage system
 */
async function runStorageTests() {
  console.log('🧪 Starting Storage System Tests\n');
  
  // Create test directory
  const testDir = '/home/louthenw/Documents/teambadass_github/teambadass/_projects/storage-system/_test';
  try {
    await fs.create_directory({ path: testDir });
  } catch (error) {
    // Directory might already exist
  }
  
  // Initialize adapters
  console.log('⚙️ Initializing components...');
  
  const localAdapter = new LocalAdapter({
    basePath: `${testDir}/local`
  });
  
  const cloudAdapter = new CloudAdapter({
    provider: 'mock',
    basePath: '/storage-test'
  });
  
  const storageManager = new StorageManager({
    localAdapter,
    cloudAdapter,
    basePath: testDir
  });
  
  const metadataTracker = new MetadataTracker({
    storageManager,
    basePath: `${testDir}/.metadata`
  });
  
  await localAdapter.initialize();
  await cloudAdapter.initialize();
  await storageManager.initialize();
  await metadataTracker.initialize();
  
  console.log('✅ All components initialized\n');
  
  // Run test suites
  let errors = 0;
  
  errors += await runLocalAdapterTests(localAdapter);
  errors += await runCloudAdapterTests(cloudAdapter);
  errors += await runMetadataTests(metadataTracker, storageManager);
  errors += await runIntegrationTests(storageManager, metadataTracker);
  
  // Test summary
  console.log(`\n🏁 Storage System Tests Completed`);
  console.log(`📊 Total errors: ${errors}`);
  
  if (errors === 0) {
    console.log('✅ All tests passed successfully!');
  } else {
    console.log(`❌ Some tests failed. See log for details.`);
  }
  
  return errors === 0;
}

/**
 * Local Adapter Tests
 * @param {LocalAdapter} localAdapter - Local adapter instance
 * @returns {Promise<number>} Number of errors
 */
async function runLocalAdapterTests(localAdapter) {
  console.log('🧪 Running Local Adapter Tests...');
  let errors = 0;
  
  try {
    // Test file storage
    const testPath = `${localAdapter.basePath}/test-file.txt`;
    const testContent = 'This is a test file for LocalAdapter.';
    
    console.log(`📝 Testing file storage...`);
    const storeResult = await localAdapter.storeFile(testPath, testContent);
    
    if (!storeResult.success) {
      console.error(`❌ Failed to store file: ${JSON.stringify(storeResult)}`);
      errors++;
    }
    
    // Test file retrieval
    console.log(`📄 Testing file retrieval...`);
    try {
      const retrievedContent = await localAdapter.retrieveFile(testPath);
      
      if (retrievedContent !== testContent) {
        console.error(`❌ Retrieved content doesn't match: ${retrievedContent}`);
        errors++;
      }
    } catch (error) {
      console.error(`❌ Failed to retrieve file: ${error.message}`);
      errors++;
    }
    
    // Test file existence
    console.log(`🔍 Testing file existence...`);
    const exists = await localAdapter.fileExists(testPath);
    
    if (!exists) {
      console.error(`❌ File existence check failed`);
      errors++;
    }
    
    // Test directory creation
    console.log(`📁 Testing directory creation...`);
    const dirPath = `${localAdapter.basePath}/test-dir`;
    const dirResult = await localAdapter.createDirectory(dirPath);
    
    if (!dirResult) {
      console.error(`❌ Failed to create directory`);
      errors++;
    }
    
    // Test directory listing
    console.log(`📋 Testing directory listing...`);
    const listing = await localAdapter.listDirectory(localAdapter.basePath);
    
    if (!listing || listing.length === 0) {
      console.error(`❌ Directory listing failed or returned empty`);
      errors++;
    }
    
    // Test file deletion (simulated)
    console.log(`🗑️ Testing file deletion...`);
    const deleteResult = await localAdapter.deleteFile(testPath);
    
    if (!deleteResult) {
      console.error(`❌ File deletion failed`);
      errors++;
    }
    
    if (errors === 0) {
      console.log('✅ All local adapter tests passed\n');
    } else {
      console.log(`❌ Local adapter tests completed with ${errors} errors\n`);
    }
  } catch (error) {
    console.error(`❌ Unexpected error in local adapter tests: ${error.message}`);
    errors++;
  }
  
  return errors;
}

/**
 * Cloud Adapter Tests
 * @param {CloudAdapter} cloudAdapter - Cloud adapter instance
 * @returns {Promise<number>} Number of errors
 */
async function runCloudAdapterTests(cloudAdapter) {
  console.log('🧪 Running Cloud Adapter Tests...');
  let errors = 0;
  
  try {
    // Test file storage
    const testPath = '/test-cloud-file.txt';
    const testContent = 'This is a test file for CloudAdapter.';
    
    console.log(`☁️ Testing cloud file storage...`);
    const storeResult = await cloudAdapter.storeFile(testPath, testContent);
    
    if (!storeResult.success) {
      console.error(`❌ Failed to store cloud file: ${JSON.stringify(storeResult)}`);
      errors++;
    }
    
    // Test file retrieval
    console.log(`☁️ Testing cloud file retrieval...`);
    try {
      const retrievedContent = await cloudAdapter.retrieveFile(testPath);
      
      if (retrievedContent !== testContent) {
        console.error(`❌ Retrieved cloud content doesn't match: ${retrievedContent}`);
        errors++;
      }
    } catch (error) {
      console.error(`❌ Failed to retrieve cloud file: ${error.message}`);
      errors++;
    }
    
    // Test file existence
    console.log(`🔍 Testing cloud file existence...`);
    const exists = await cloudAdapter.fileExists(testPath);
    
    if (!exists) {
      console.error(`❌ Cloud file existence check failed`);
      errors++;
    }
    
    // Test directory creation
    console.log(`📁 Testing cloud directory creation...`);
    const dirPath = '/test-cloud-dir';
    const dirResult = await cloudAdapter.createDirectory(dirPath);
    
    if (!dirResult) {
      console.error(`❌ Failed to create cloud directory`);
      errors++;
    }
    
    // Test file listing
    console.log(`📋 Testing cloud file listing...`);
    const listing = await cloudAdapter.listFiles('/');
    
    if (!listing) {
      console.error(`❌ Cloud file listing failed`);
      errors++;
    }
    
    // Test file deletion
    console.log(`🗑️ Testing cloud file deletion...`);
    const deleteResult = await cloudAdapter.deleteFile(testPath);
    
    if (!deleteResult) {
      console.error(`❌ Cloud file deletion failed`);
      errors++;
    }
    
    if (errors === 0) {
      console.log('✅ All cloud adapter tests passed\n');
    } else {
      console.log(`❌ Cloud adapter tests completed with ${errors} errors\n`);
    }
  } catch (error) {
    console.error(`❌ Unexpected error in cloud adapter tests: ${error.message}`);
    errors++;
  }
  
  return errors;
}

/**
 * Metadata Tests
 * @param {MetadataTracker} metadataTracker - Metadata tracker instance
 * @param {StorageManager} storageManager - Storage manager instance
 * @returns {Promise<number>} Number of errors
 */
async function runMetadataTests(metadataTracker, storageManager) {
  console.log('🧪 Running Metadata Tracker Tests...');
  let errors = 0;
  
  try {
    // Create test file via storage manager
    const testPath = 'metadata-test-file.txt';
    const testContent = 'This is a test file for MetadataTracker.';
    
    console.log(`📝 Creating test file for metadata tracking...`);
    const storeResult = await storageManager.storeFile(testPath, testContent);
    
    if (!storeResult.success) {
      console.error(`❌ Failed to create test file: ${JSON.stringify(storeResult)}`);
      errors++;
      return errors;
    }
    
    // Track file metadata
    console.log(`📊 Testing metadata tracking...`);
    const metadataResult = await metadataTracker.trackFile(testPath, {
      size: testContent.length,
      hash: 'test-hash-value'
    });
    
    if (!metadataResult) {
      console.error(`❌ Failed to track metadata`);
      errors++;
    }
    
    // Get file metadata
    console.log(`📊 Testing metadata retrieval...`);
    const metadata = await metadataTracker.getMetadata(testPath);
    
    if (!metadata) {
      console.error(`❌ Failed to retrieve metadata`);
      errors++;
    } else if (metadata.size !== testContent.length) {
      console.error(`❌ Metadata size doesn't match: ${metadata.size} vs ${testContent.length}`);
      errors++;
    }
    
    // Test version tracking with updated file
    console.log(`🔄 Testing version tracking...`);
    const updatedContent = testContent + '\nThis line was added in an update.';
    const updateResult = await storageManager.storeFile(testPath, updatedContent);
    
    if (!updateResult.success) {
      console.error(`❌ Failed to update test file: ${JSON.stringify(updateResult)}`);
      errors++;
    } else {
      // Track updated metadata
      const updatedMetadata = await metadataTracker.trackFile(testPath, {
        size: updatedContent.length,
        hash: 'updated-hash-value'
      });
      
      if (!updatedMetadata) {
        console.error(`❌ Failed to track updated metadata`);
        errors++;
      } else if (updatedMetadata.versions.length !== 2) {
        console.error(`❌ Version history not properly updated: ${updatedMetadata.versions.length} versions`);
        errors++;
      }
    }
    
    // Test listing tracked files
    console.log(`📋 Testing tracked files listing...`);
    const trackedFiles = await metadataTracker.listTrackedFiles();
    
    if (!trackedFiles || !trackedFiles.includes(testPath)) {
      console.error(`❌ Tracked files listing failed or missing test file`);
      errors++;
    }
    
    // Test version history retrieval
    console.log(`📜 Testing version history retrieval...`);
    const versionHistory = await metadataTracker.getVersionHistory(testPath);
    
    if (!versionHistory || versionHistory.length !== 2) {
      console.error(`❌ Version history retrieval failed: ${versionHistory?.length || 0} versions`);
      errors++;
    }
    
    // Test metadata deletion
    console.log(`🗑️ Testing metadata deletion...`);
    const deleteResult = await metadataTracker.deleteMetadata(testPath);
    
    if (!deleteResult) {
      console.error(`❌ Metadata deletion failed`);
      errors++;
    }
    
    // Cleanup test file
    await storageManager.deleteFile(testPath);
    
    if (errors === 0) {
      console.log('✅ All metadata tracker tests passed\n');
    } else {
      console.log(`❌ Metadata tracker tests completed with ${errors} errors\n`);
    }
  } catch (error) {
    console.error(`❌ Unexpected error in metadata tests: ${error.message}`);
    errors++;
  }
  
  return errors;
}

/**
 * Integration Tests
 * @param {StorageManager} storageManager - Storage manager instance
 * @param {MetadataTracker} metadataTracker - Metadata tracker instance
 * @returns {Promise<number>} Number of errors
 */
async function runIntegrationTests(storageManager, metadataTracker) {
  console.log('🧪 Running Integration Tests...');
  let errors = 0;
  
  try {
    // Test local storage with metadata tracking
    const localPath = 'integration-local-test.txt';
    const localContent = 'This is a local integration test file.';
    
    console.log(`📝 Testing local storage with metadata tracking...`);
    const localResult = await storageManager.storeFile(localPath, localContent);
    
    if (!localResult.success) {
      console.error(`❌ Failed to store local file: ${JSON.stringify(localResult)}`);
      errors++;
    } else {
      // Track metadata
      const localMetadata = await metadataTracker.trackFile(localPath, {
        size: localContent.length,
        hash: 'local-test-hash'
      });
      
      if (!localMetadata) {
        console.error(`❌ Failed to track local file metadata`);
        errors++;
      }
    }
    
    // Test cloud storage with metadata tracking
    const cloudPath = 'integration-cloud-test.txt';
    const cloudContent = 'This is a cloud integration test file.';
    
    console.log(`☁️ Testing cloud storage with metadata tracking...`);
    const cloudResult = await storageManager.storeFile(cloudPath, cloudContent, {
      useCloud: true
    });
    
    if (!cloudResult.success) {
      console.error(`❌ Failed to store cloud file: ${JSON.stringify(cloudResult)}`);
      errors++;
    } else {
      // Track metadata
      const cloudMetadata = await metadataTracker.trackFile(cloudPath, {
        size: cloudContent.length,
        hash: 'cloud-test-hash'
      });
      
      if (!cloudMetadata) {
        console.error(`❌ Failed to track cloud file metadata`);
        errors++;
      }
    }
    
    // Test retrieval with adapter selection
    console.log(`📄 Testing retrieval with adapter selection...`);
    try {
      const retrievedLocal = await storageManager.retrieveFile(localPath);
      
      if (retrievedLocal !== localContent) {
        console.error(`❌ Retrieved local content doesn't match: ${retrievedLocal}`);
        errors++;
      }
      
      const retrievedCloud = await storageManager.retrieveFile(cloudPath, {
        useCloud: true
      });
      
      if (retrievedCloud !== cloudContent) {
        console.error(`❌ Retrieved cloud content doesn't match: ${retrievedCloud}`);
        errors++;
      }
    } catch (error) {
      console.error(`❌ File retrieval failed: ${error.message}`);
      errors++;
    }
    
    // Test metadata statistics
    console.log(`📊 Testing metadata statistics...`);
    const stats = await metadataTracker.getStatistics();
    
    if (!stats || stats.fileCount < 2) {
      console.error(`❌ Metadata statistics failed or missing files: ${JSON.stringify(stats)}`);
      errors++;
    }
    
    // Cleanup
    await storageManager.deleteFile(localPath);
    await storageManager.deleteFile(cloudPath, { useCloud: true });
    await metadataTracker.deleteMetadata(localPath);
    await metadataTracker.deleteMetadata(cloudPath);
    
    if (errors === 0) {
      console.log('✅ All integration tests passed\n');
    } else {
      console.log(`❌ Integration tests completed with ${errors} errors\n`);
    }
  } catch (error) {
    console.error(`❌ Unexpected error in integration tests: ${error.message}`);
    errors++;
  }
  
  return errors;
}

// Run the tests
runStorageTests().catch(error => {
  console.error(`❌ Test execution failed: ${error.message}`);
});

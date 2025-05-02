/**
 * Test script for fs-helper.js
 */

const fsHelper = require('./fs-helper');

// Simple test function
async function runTests() {
  console.log('Testing fs-helper.js...');
  
  // Test 1: Generate ASCII tree
  console.log('\nTest 1: Generate ASCII tree');
  const tree = await fsHelper.generateAsciiTree();
  console.log(tree);
  
  // Test 2: Check if keystone directory exists
  console.log('\nTest 2: Check if keystone directory exists');
  const keystoneExists = await fsHelper.pathExists('/home/louthenw/Documents/teambadass_github/teambadass/keystone');
  console.log(`Keystone directory exists: ${keystoneExists}`);
  
  // Test 3: Write file with directory creation
  console.log('\nTest 3: Write file with directory creation');
  const testDir = '/home/louthenw/Documents/teambadass_github/teambadass/utils/test-dir';
  const testFile = `${testDir}/test-file.txt`;
  const writeResult = await fsHelper.writeFile(testFile, 'Test content');
  console.log(`Write file result: ${writeResult}`);
  
  console.log('\nAll tests complete!');
}

runTests().catch(console.error);

/**
 * Test script for gas-tracker.js
 */

const gasTracker = require('./gas-tracker');

// Simple test function
async function runTest() {
  console.log('Testing gas-tracker.js...');
  
  // Initialize gas tracker
  console.log('\nInitializing gas tracker...');
  const initResult = await gasTracker.initialize();
  console.log('Initialization result:', initResult);
  
  // Simulate context loading (80KB)
  console.log('\nSimulating context loading...');
  const contextResult = gasTracker.recordOperation('contextLoading', { kb: 80 });
  console.log(`Context loaded. Usage: ${contextResult.currentUsage.toFixed(1)}%`);
  
  // Simulate some discussion
  console.log('\nSimulating discussion...');
  const discussionResult = gasTracker.recordOperation('discussion', { size: 'medium' });
  console.log(`Discussion recorded. Usage: ${discussionResult.currentUsage.toFixed(1)}%`);
  
  // Simulate code generation
  console.log('\nSimulating code generation...');
  const codeResult = gasTracker.recordOperation('code', { size: 'large', complexity: 'high' });
  console.log(`Code generated. Usage: ${codeResult.currentUsage.toFixed(1)}%`);
  
  // Simulate artifact creation
  console.log('\nSimulating artifact creation...');
  const artifactResult = gasTracker.recordOperation('artifact', { size: 'medium', complexity: 'medium' });
  console.log(`Artifact created. Usage: ${artifactResult.currentUsage.toFixed(1)}%`);
  
  // Get status report
  console.log('\nGetting status report...');
  const report = gasTracker.getStatusReport();
  console.log('Status Report:');
  console.log(`- Session ID: ${report.sessionId}`);
  console.log(`- Current Usage: ${report.currentUsage.toFixed(1)}%`);
  console.log(`- Status: ${report.status}`);
  console.log(`- Duration: ${report.duration} minutes`);
  console.log(`- Operation Count: ${report.operationCount}`);
  console.log(`- Recommendation: ${report.recommendation}`);
  
  // Save metrics
  console.log('\nSaving metrics...');
  const saveResult = await gasTracker.saveMetrics();
  console.log('Save result:', saveResult);
  
  console.log('\nTest complete!');
}

runTest().catch(console.error);

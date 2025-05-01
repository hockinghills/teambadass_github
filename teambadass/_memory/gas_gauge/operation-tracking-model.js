/**
 * TeamBadass Operation-Based Tracking Model
 * Enhanced version based on observable metrics
 */

// Operation Types and their base costs
const OPERATION_TYPES = {
  CONTEXT_LOADING: {
    id: "context_loading",
    name: "Context Loading",
    base_cost: 2.0,
    per_kb: 0.05,
    description: "Loading repository content and other context"
  },
  DISCUSSION_EXCHANGE: {
    id: "discussion_exchange",
    name: "Discussion Exchange",
    base_cost: 1.0,
    per_word: 0.01,
    description: "Back-and-forth conversation exchanges"
  },
  CODE_GENERATION: {
    id: "code_generation",
    name: "Code Generation",
    base_cost: 3.0,
    complexity_factors: {
      low: 1.0,
      medium: 2.0,
      high: 4.0
    },
    size_factors: {
      small: 1.0,
      medium: 2.5,
      large: 5.0
    },
    description: "Creating new code or modifying existing code"
  },
  SEARCH_OPERATION: {
    id: "search_operation",
    name: "Search Operation",
    base_cost: 4.0,
    per_result: 0.5,
    description: "Web searches or internal repository searches"
  },
  ARTIFACT_CREATION: {
    id: "artifact_creation",
    name: "Artifact Creation",
    base_cost: 5.0,
    complexity_factors: {
      low: 1.0,
      medium: 2.0, 
      high: 3.5
    },
    size_factors: {
      small: 1.0,
      medium: 2.0,
      large: 4.0
    },
    description: "Creating visualizations, documents, or other artifacts"
  },
  KEYSTONE_CREATION: {
    id: "keystone_creation",
    name: "Keystone Creation",
    base_cost: 8.0,
    complexity_factors: {
      low: 1.0,
      medium: 1.5,
      high: 2.5
    },
    description: "Creating keystone moment records"
  },
  PLANNING: {
    id: "planning",
    name: "Planning & Analysis",
    base_cost: 2.0,
    complexity_factors: {
      low: 1.0,
      medium: 2.0,
      high: 3.0 
    },
    description: "Project planning, strategy, and deep analysis"
  }
};

/**
 * Calculate the cost of a context loading operation
 * @param {number} sizeKb - Size of loaded context in KB
 * @returns {number} - Estimated gas cost
 */
function calculateContextLoadingCost(sizeKb) {
  return OPERATION_TYPES.CONTEXT_LOADING.base_cost + 
         (OPERATION_TYPES.CONTEXT_LOADING.per_kb * sizeKb);
}

/**
 * Calculate the cost of a discussion exchange
 * @param {number} words - Approximate word count in the exchange
 * @returns {number} - Estimated gas cost
 */
function calculateDiscussionCost(words) {
  return OPERATION_TYPES.DISCUSSION_EXCHANGE.base_cost + 
         (OPERATION_TYPES.DISCUSSION_EXCHANGE.per_word * words);
}

/**
 * Calculate the cost of code generation
 * @param {string} complexity - Complexity level (low, medium, high)
 * @param {string} size - Size level (small, medium, large)
 * @returns {number} - Estimated gas cost
 */
function calculateCodeGenerationCost(complexity, size) {
  const complexityFactor = OPERATION_TYPES.CODE_GENERATION.complexity_factors[complexity] || 
                           OPERATION_TYPES.CODE_GENERATION.complexity_factors.medium;
                           
  const sizeFactor = OPERATION_TYPES.CODE_GENERATION.size_factors[size] || 
                     OPERATION_TYPES.CODE_GENERATION.size_factors.medium;
                     
  return OPERATION_TYPES.CODE_GENERATION.base_cost * complexityFactor * sizeFactor;
}

/**
 * Calculate the cost of a search operation
 * @param {number} resultsCount - Number of search results
 * @returns {number} - Estimated gas cost
 */
function calculateSearchCost(resultsCount) {
  return OPERATION_TYPES.SEARCH_OPERATION.base_cost + 
         (OPERATION_TYPES.SEARCH_OPERATION.per_result * resultsCount);
}

/**
 * Calculate the cost of artifact creation
 * @param {string} complexity - Complexity level (low, medium, high)
 * @param {string} size - Size level (small, medium, large)
 * @returns {number} - Estimated gas cost
 */
function calculateArtifactCreationCost(complexity, size) {
  const complexityFactor = OPERATION_TYPES.ARTIFACT_CREATION.complexity_factors[complexity] || 
                           OPERATION_TYPES.ARTIFACT_CREATION.complexity_factors.medium;
                           
  const sizeFactor = OPERATION_TYPES.ARTIFACT_CREATION.size_factors[size] || 
                     OPERATION_TYPES.ARTIFACT_CREATION.size_factors.medium;
                     
  return OPERATION_TYPES.ARTIFACT_CREATION.base_cost * complexityFactor * sizeFactor;
}

/**
 * Calculate the cost of keystone creation
 * @param {string} complexity - Complexity level (low, medium, high)
 * @returns {number} - Estimated gas cost
 */
function calculateKeystoneCost(complexity) {
  const complexityFactor = OPERATION_TYPES.KEYSTONE_CREATION.complexity_factors[complexity] || 
                           OPERATION_TYPES.KEYSTONE_CREATION.complexity_factors.medium;
                           
  return OPERATION_TYPES.KEYSTONE_CREATION.base_cost * complexityFactor;
}

/**
 * Calculate the cost of planning and analysis
 * @param {string} complexity - Complexity level (low, medium, high)
 * @returns {number} - Estimated gas cost
 */
function calculatePlanningCost(complexity) {
  const complexityFactor = OPERATION_TYPES.PLANNING.complexity_factors[complexity] || 
                           OPERATION_TYPES.PLANNING.complexity_factors.medium;
                           
  return OPERATION_TYPES.PLANNING.base_cost * complexityFactor;
}

/**
 * Generate operation cost estimate for pre-task assessment
 * @param {string} operationType - Type of operation
 * @param {Object} params - Parameters for the operation
 * @returns {Object} - Cost estimate with details
 */
function generateOperationEstimate(operationType, params) {
  let cost = 0;
  let details = {};
  
  switch(operationType) {
    case OPERATION_TYPES.CONTEXT_LOADING.id:
      cost = calculateContextLoadingCost(params.sizeKb);
      details = {
        sizeKb: params.sizeKb,
        base_cost: OPERATION_TYPES.CONTEXT_LOADING.base_cost,
        per_kb_cost: OPERATION_TYPES.CONTEXT_LOADING.per_kb
      };
      break;
      
    case OPERATION_TYPES.DISCUSSION_EXCHANGE.id:
      cost = calculateDiscussionCost(params.words);
      details = {
        words: params.words,
        base_cost: OPERATION_TYPES.DISCUSSION_EXCHANGE.base_cost,
        per_word_cost: OPERATION_TYPES.DISCUSSION_EXCHANGE.per_word
      };
      break;
      
    case OPERATION_TYPES.CODE_GENERATION.id:
      cost = calculateCodeGenerationCost(params.complexity, params.size);
      details = {
        complexity: params.complexity,
        size: params.size,
        base_cost: OPERATION_TYPES.CODE_GENERATION.base_cost,
        complexity_factor: OPERATION_TYPES.CODE_GENERATION.complexity_factors[params.complexity],
        size_factor: OPERATION_TYPES.CODE_GENERATION.size_factors[params.size]
      };
      break;
      
    case OPERATION_TYPES.SEARCH_OPERATION.id:
      cost = calculateSearchCost(params.resultsCount);
      details = {
        resultsCount: params.resultsCount,
        base_cost: OPERATION_TYPES.SEARCH_OPERATION.base_cost,
        per_result_cost: OPERATION_TYPES.SEARCH_OPERATION.per_result
      };
      break;
      
    case OPERATION_TYPES.ARTIFACT_CREATION.id:
      cost = calculateArtifactCreationCost(params.complexity, params.size);
      details = {
        complexity: params.complexity,
        size: params.size,
        base_cost: OPERATION_TYPES.ARTIFACT_CREATION.base_cost,
        complexity_factor: OPERATION_TYPES.ARTIFACT_CREATION.complexity_factors[params.complexity],
        size_factor: OPERATION_TYPES.ARTIFACT_CREATION.size_factors[params.size]
      };
      break;
      
    case OPERATION_TYPES.KEYSTONE_CREATION.id:
      cost = calculateKeystoneCost(params.complexity);
      details = {
        complexity: params.complexity,
        base_cost: OPERATION_TYPES.KEYSTONE_CREATION.base_cost,
        complexity_factor: OPERATION_TYPES.KEYSTONE_CREATION.complexity_factors[params.complexity]
      };
      break;
      
    case OPERATION_TYPES.PLANNING.id:
      cost = calculatePlanningCost(params.complexity);
      details = {
        complexity: params.complexity,
        base_cost: OPERATION_TYPES.PLANNING.base_cost,
        complexity_factor: OPERATION_TYPES.PLANNING.complexity_factors[params.complexity]
      };
      break;
      
    default:
      cost = 0;
      details = { error: "Unknown operation type" };
  }
  
  return {
    operationType: operationType,
    cost: Math.round(cost * 10) / 10, // Round to 1 decimal place
    details: details
  };
}

/**
 * Format a pre-task assessment with cost estimates
 * @param {string} taskName - Name of the task
 * @param {string} operationType - Type of operation
 * @param {Object} params - Parameters for the operation
 * @param {number} currentUsage - Current gas usage
 * @returns {string} - Formatted pre-task assessment
 */
function formatPreTaskAssessment(taskName, operationType, params, currentUsage) {
  const estimate = generateOperationEstimate(operationType, params);
  const postTaskUsage = currentUsage + estimate.cost;
  
  // ASCII gauge for current status
  const currentGauge = generateAsciiGauge(currentUsage);
  
  // ASCII gauge for post-task status
  const postTaskGauge = generateAsciiGauge(postTaskUsage);
  
  // Generate decision options
  const options = generateDecisionOptions(currentUsage, estimate.cost);
  
  // Format the assessment
  return `
🔎 Pre-task Assessment
Task: ${taskName}
Type: ${OPERATION_TYPES[operationType.toUpperCase()].name}
Complexity: ${params.complexity || 'N/A'}
Size: ${params.size || 'N/A'}

Current Status: ${currentGauge} ${currentUsage.toFixed(1)}%
Estimated Cost: ${estimate.cost}%
Post-Task Status: ${postTaskGauge} ${postTaskUsage.toFixed(1)}%

Decision Options:
${options.map(option => `- ${option.option} (${option.recommendation}): ${option.description}`).join('\n')}
`.trim();
}

/**
 * Generate an ASCII gauge representation of usage
 * @param {number} usage - Current usage percentage
 * @param {number} width - Width of the gauge in characters
 * @returns {string} - ASCII gauge
 */
function generateAsciiGauge(usage, width = 20) {
  const warningThreshold = 60;
  const hardStopThreshold = 90;
  
  const filledWidth = Math.round((usage / 100) * width);
  const warningPos = Math.round((warningThreshold / 100) * width);
  const hardStopPos = Math.round((hardStopThreshold / 100) * width);
  
  let gauge = "[";
  
  for (let i = 0; i < width; i++) {
    if (i < filledWidth) {
      gauge += "="; // Filled portion
    } else if (i === warningPos) {
      gauge += "W"; // Warning threshold
    } else if (i === hardStopPos) {
      gauge += "H"; // Hard stop threshold
    } else {
      gauge += " "; // Empty portion
    }
  }
  
  gauge += "]";
  
  return gauge;
}

/**
 * Generate decision options based on current usage and estimated cost
 * @param {number} currentUsage - Current gas usage
 * @param {number} estimatedCost - Estimated cost of the operation
 * @returns {Array} - Array of decision options
 */
function generateDecisionOptions(currentUsage, estimatedCost) {
  const warningThreshold = 60;
  const hardStopThreshold = 90;
  const postTaskUsage = currentUsage + estimatedCost;
  const options = [];
  
  if (postTaskUsage >= hardStopThreshold) {
    options.push({
      option: "Hop Session",
      recommendation: "Strong",
      description: "Start a new session before attempting this task"
    });
    
    options.push({
      option: "Break Into Chunks",
      recommendation: "Alternative",
      description: "Split into smaller pieces to fit within available capacity"
    });
  } else if (postTaskUsage >= warningThreshold) {
    options.push({
      option: "Proceed & Hop",
      recommendation: "Strong",
      description: "Complete task then immediately hop to new session"
    });
    
    options.push({
      option: "Reduce Scope",
      recommendation: "Alternative",
      description: "Complete a smaller portion of the task in this session"
    });
  } else if (postTaskUsage >= warningThreshold * 0.8) {
    options.push({
      option: "Proceed With Caution",
      recommendation: "Standard",
      description: "Complete task but prepare for potential hop afterwards"
    });
  } else {
    options.push({
      option: "Proceed As Planned",
      recommendation: "Standard",
      description: "Sufficient capacity for this task and more"
    });
  }
  
  return options;
}

// Global registry for operations performed in this session
const sessionOperations = {
  operations: [],
  currentUsage: 0,
  
  addOperation(type, details, cost) {
    const cumulative = this.currentUsage + cost;
    
    const operation = {
      type,
      details,
      cost,
      cumulative,
      timestamp: new Date().toISOString()
    };
    
    this.operations.push(operation);
    this.currentUsage = cumulative;
    
    return operation;
  },
  
  getStatus() {
    const warningThreshold = 60;
    const hardStopThreshold = 90;
    
    let status = "NORMAL";
    if (this.currentUsage >= hardStopThreshold) {
      status = "CRITICAL";
    } else if (this.currentUsage >= warningThreshold) {
      status = "WARNING";
    } else if (this.currentUsage >= warningThreshold * 0.8) {
      status = "CAUTION";
    }
    
    return {
      currentUsage: this.currentUsage,
      status,
      operationCount: this.operations.length,
      asciiGauge: generateAsciiGauge(this.currentUsage)
    };
  }
};

// Example usage
console.log("Current status:", sessionOperations.getStatus());
console.log("\nEstimating cost of code generation (medium, medium):");
console.log(generateOperationEstimate(OPERATION_TYPES.CODE_GENERATION.id, { complexity: "medium", size: "medium" }));
console.log("\nPre-task assessment for artifact creation:");
console.log(formatPreTaskAssessment(
  "Create Dashboard Component", 
  OPERATION_TYPES.ARTIFACT_CREATION.id,
  { complexity: "medium", size: "medium" },
  30.5
));

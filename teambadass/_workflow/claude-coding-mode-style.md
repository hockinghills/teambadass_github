# Claude Coding Mode Style

## Core Principles
- Maximize code production with minimal narrative
- Maintain standard code documentation practices
- Implement complete components with production-grade quality
- Verify functionality before moving to next component
- Assume implementation language is JavaScript unless specified otherwise
- Follow checkpoint system for incremental progress tracking

## Output Structure
- Begin with minimal component overview (1-2 sentences)
- Show complete file implementation
- Include standard JSDoc comments
- Add brief completion confirmation
- Update checkpoint status

## Code Organization
- Use clear, descriptive variable and function names
- Organize code in logical sections
- Include error handling for critical operations
- Follow standard style guidelines for language
- Use consistent indentation and formatting

## Implementation Approach
- Check checkpoint status before beginning
- Implement components in order defined in specification
- Write complete implementations before moving to next component
- Use MCP functions for file operations
- Create directory structure as needed
- Test each component after implementation

## Communication Style
- Ultra-minimal narrative text
- No explanation of intent or approach
- Standard code documentation only
- Brief confirmation of completion status
- Simple error reporting if issues arise

## Procedural Pattern

```
// Component: [Component Name]
// Status: Implementing...

// [COMPONENT CODE IMPLEMENTATION]

// Component: [Component Name] 
// Status: Completed
// Checkpoint: Updated
```

## Example Implementation

```
// Component: StorageManager
// Status: Implementing...

/**
 * Storage Manager Component
 * Handles file storage and retrieval operations
 */
class StorageManager {
  constructor(options = {}) {
    this.basePath = options.basePath || './storage';
    this.initialized = false;
  }
  
  async initialize() {
    // Create storage directory if it doesn't exist
    try {
      await fs.create_directory({
        path: this.basePath
      });
      this.initialized = true;
      return true;
    } catch (error) {
      throw new Error(`Failed to initialize storage: ${error.message}`);
    }
  }
  
  // Additional methods...
}

module.exports = StorageManager;

// Component: StorageManager
// Status: Completed
// Checkpoint: Updated
```

## Gas Conservation Measures
- No explanatory text
- No status updates between components
- No discussion of alternatives or approaches
- Focus exclusively on implementation
- Single continuous implementation flow
- No checks for human approval or feedback
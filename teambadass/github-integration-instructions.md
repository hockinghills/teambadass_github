# GitHub Integration Instructions

This document explains how to integrate the optimized JSON memory structure into your existing GitHub repository.

## Directory Structure to Create

```
teambadass/
├── _memory/                      # Main memory directory
│   ├── core/                     # Core system files
│   │   ├── teambadass-optimized-memory.json  # Entry point 
│   │   ├── team-dynamics.json               # Team roles and communication
│   │   ├── project-history.json             # Project history overview
│   │   └── technical-environment.json       # Technical details
│   └── projects/                 # Project-specific memory
│       ├── furnace-project.json            # Furnace project details
│       ├── memory-system.json              # Memory system project
│       └── adhd-case.json                  # ADHD case resources
├── README.md                    # Existing file - no changes needed
├── team/                        # Existing directory - no changes needed
├── projects/                    # Existing directory - no changes needed
└── utils/                       # Existing directory - no changes needed
```

## Installation Steps

1. **Create Memory Directory Structure**

   ```bash
   mkdir -p teambadass/_memory/core
   mkdir -p teambadass/_memory/projects
   ```

2. **Add Memory JSON Files**

   Copy each of the JSON files into their respective directories:
   
   - Core files go in `teambadass/_memory/core/`
   - Project files go in `teambadass/_memory/projects/`

3. **Add Documentation**

   Add this file to the repository so you have installation instructions.

## Usage

The memory system is designed to be:

1. **Machine-Readable** - Optimized for Claude to efficiently process
2. **Modular** - Broken into separate files to minimize context window usage
3. **Maintainable** - Clear organization makes updates easier

When working with Claude, you can share specific JSON files as needed rather than the entire repository. For example:

- Share `team-dynamics.json` when focusing on communication patterns
- Share `furnace-project.json` when working on the Furnace project
- Share `teambadass-optimized-memory.json` as an entry point

## Maintenance

Update the JSON files as your projects evolve. Make sure to:

1. Increment the `version` field when making significant changes
2. Update the `last_updated` field with the current date
3. Keep file sizes manageable to optimize Claude's context window usage
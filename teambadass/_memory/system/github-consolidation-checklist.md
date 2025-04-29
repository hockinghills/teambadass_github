# TeamBadass GitHub Consolidation Checklist

## Project Background and Context
- [ ] The TeamBadass project originally used Google Drive for storage and synchronization
- [ ] We encountered persistent issues with Google Drive authentication between sessions
- [ ] We've transitioned to using GitHub as our repository and storage solution
- [ ] This checklist guides the process of consolidating valuable components while removing Google Drive dependencies
- [ ] The goal is to preserve all useful functionality while streamlining the system

## Repository Structure
- [ ] Current GitHub structure is organized in `teambadass/` directory
- [ ] Memory files are primarily in `teambadass/_memory/` directory
- [ ] Core system files are at the repository root
- [ ] Project files are in `teambadass/projects/`
- [ ] Keystone moments are stored in `keystone_moments/` directory

## 1. Gas Gauge System
- [ ] Current GitHub implementation: `teambadass/_memory/system/claude_gas_gauge.py`
- [ ] Older implementation: `claude_gas_gauge.py` (root), `gas_check_script.py`, `gas_check_utility.py`
- [ ] Purpose: Tracks Claude's processing capacity during conversations
- [ ] Key functions: `check_gas()`, `can_complete_task()`, `estimate_code_gas_requirement()`
- [ ] Visualization components: ASCII gauge representation
- [ ] Compare implementations to identify any improvements from older version
- [ ] Look for enhanced visualization techniques
- [ ] Check for additional task estimation logic
- [ ] Examine trigger detection code (`trigger_hook.py`, `trigger_script.py`)
- [ ] **Final review of all gas gauge files for valuable content before marking for deletion**

## 2. Core Memory System
- [ ] GitHub implementation: `teambadass/_memory/core/` directory JSON files
- [ ] Main integration script: `tb_integration.py`
- [ ] Command runner: `tb_memory.sh`
- [ ] Key functions to preserve:
  - [ ] `generate_continuity()`: Creates human-readable continuity documents
  - [ ] `initialize_system()`: Sets up memory system directories and files
  - [ ] `check_dependencies()`: Verifies required dependencies
  - [ ] `main()`: Command-line interface handler
- [ ] Drive dependencies to remove:
  - [ ] `sync_with_drive()` function
  - [ ] Drive authentication code blocks
  - [ ] References to Drive paths and folders
  - [ ] Any imports of Drive-specific libraries
- [ ] Test each component after removing Drive dependencies
- [ ] **Final review of all core memory system files for valuable content before marking for deletion**

## 3. Keystone Moment System
- [ ] GitHub implementation: `keystone_manager.py` and associated files
- [ ] Purpose: Captures and preserves significant moments in our collaboration journey
- [ ] Directory structure: `keystone_moments/` containing JSON and MD files
- [ ] Key functions:
  - [ ] `capture_keystone_moment()`: Saves significant conversations
  - [ ] `list_keystone_moments()`: Displays available keystone moments
  - [ ] `retrieve_keystone_moment()`: Fetches specific moment
- [ ] File paths to update:
  - [ ] BASE_DIR definition to match GitHub structure
  - [ ] KEYSTONE_DIR path
  - [ ] CONVERSATION_DIR path
- [ ] Test full functionality:
  - [ ] Creating new moments
  - [ ] Listing existing moments
  - [ ] Retrieving specific moments
- [ ] **Final review of all keystone system files for valuable content before marking for deletion**

## 4. Web Interface
- [ ] GitHub implementation: `tb_web_interface.html`
- [ ] Purpose: Browser-based management of the memory system
- [ ] Key components:
  - [ ] Dashboard for system status
  - [ ] File management interface
  - [ ] Configuration settings
  - [ ] Continuity document generation
- [ ] Drive-specific elements to remove:
  - [ ] Sync buttons and functions
  - [ ] Drive folder references
  - [ ] Authentication components
  - [ ] Drive-specific API calls
- [ ] Local file operations to update:
  - [ ] File listing mechanism
  - [ ] Upload/download functions
  - [ ] Storage paths
- [ ] **Final review of web interface files for valuable content before marking for deletion**

## 5. Session Management
- [ ] GitHub implementations:
  - [ ] `teambadass/_memory/system/session_start.py`
  - [ ] `tb_boot_sequence.py`
  - [ ] `tb_init_script.py`
- [ ] Purpose: Initializes and manages Claude sessions
- [ ] Key functions:
  - [ ] `initialize_session()`: Starts new TeamBadass session
  - [ ] `check_gas()`: Monitors Claude's capacity
  - [ ] `estimate_task()`: Evaluates capability for tasks
  - [ ] `load_relationship_anarchy_agreements()`: Loads collaboration framework
- [ ] Drive dependencies to remove:
  - [ ] Drive service initialization
  - [ ] Authentication functions
  - [ ] File retrieval from Drive
- [ ] Test complete boot sequence with GitHub structure
- [ ] **Final review of all session management files for valuable content before marking for deletion**

## 6. Memory Content
- [ ] GitHub implementation: JSON files in `teambadass/_memory/` subdirectories
- [ ] Key content categories:
  - [ ] Team dynamics (`team-dynamics-json.json`)
  - [ ] Project history (`project-history-json.json`)
  - [ ] Technical environment (`technical-environment-json.json`)
  - [ ] Project-specific data (`furnace-project-json.json`, etc.)
- [ ] Tasks:
  - [ ] Merge content from older Drive-based files if valuable
  - [ ] Update file paths to match GitHub structure
  - [ ] Remove Drive-specific references
  - [ ] Ensure comprehensive content coverage
  - [ ] Check for data duplication or conflicts
- [ ] **Final review of all memory content files for valuable content before marking for deletion**

## 7. Google Drive Components (For Deletion)
- [ ] Primary Drive sync module: `tb_drive_sync.py`
- [ ] Authentication files:
  - [ ] `tb_drive_credentials.json`
  - [ ] `tb_drive_token.json`
  - [ ] `token.json`
- [ ] Setup script: `setup.py`
- [ ] Actions before deletion:
  - [ ] Archive key files for future reference (optional)
  - [ ] Extract any utility functions not specific to Drive
  - [ ] Document the Drive structure for historical context
  - [ ] Ensure no GitHub components reference these files
- [ ] **Final review of all Google Drive files for any valuable functions before deletion**

## 8. Documentation Update
- [ ] Update primary README.md with current GitHub workflow
- [ ] Create/update system architecture document
- [ ] Document each component's purpose and functionality
- [ ] Update usage instructions for all commands
- [ ] Remove references to Google Drive throughout documentation
- [ ] Create new user guide for TeamBadass Memory System
- [ ] **Final review of documentation for accuracy and completeness**

## 9. Final Testing
- [ ] Verify entire system operates without Drive components
- [ ] Test end-to-end workflow:
  - [ ] System initialization
  - [ ] Gas gauge monitoring
  - [ ] Continuity document generation
  - [ ] Keystone moment creation and retrieval
  - [ ] Command-line interface functionality
  - [ ] Web interface operation
- [ ] Create complete backup before permanent deletion
- [ ] Test system with a fresh Claude session to confirm it loads correctly
- [ ] **Final comprehensive review to ensure no valuable components are lost**

## 10. Future Enhancements (Post-Consolidation)
- [ ] Improve gas gauge visualization
- [ ] Enhance keystone moment browsing capabilities
- [ ] Add more sophisticated context loading mechanisms
- [ ] Create additional documentation for new collaborators
- [ ] Develop better testing procedures for memory system components

## Completion Tracking
- [ ] Consolidation initiated: April 29, 2025
- [ ] Section 1 completed: ________________
- [ ] Section 2 completed: ________________
- [ ] Section 3 completed: ________________
- [ ] Section 4 completed: ________________
- [ ] Section 5 completed: ________________
- [ ] Section 6 completed: ________________
- [ ] Section 7 completed: ________________
- [ ] Section 8 completed: ________________
- [ ] Section 9 completed: ________________
- [ ] Full consolidation completed: ________________

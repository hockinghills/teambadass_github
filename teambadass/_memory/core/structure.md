# TeamBadass GitHub Structure - Gas Gauge Integration

## Core Principles
- Flatter structure for better Claude accessibility
- Standardized JSON for machine readability
- Front-loaded critical information
- Explicit cross-references with full paths

## Directory Structure

```
teambadass/
├── _memory/
│   ├── core/                      # Core memory files
│   │   ├── team_dynamics.json     # Team roles, communication preferences
│   │   ├── project_history.json   # Project history and current status
│   │   └── technical_env.json     # Technical environment details
│   ├── gas_gauge/                 # Gas gauge system files
│   │   ├── gas_gauge.py           # Core functionality (Phase 1)
│   │   ├── gauge_reporting.py     # Enhanced reporting (Phase 2)
│   │   ├── gauge_metrics.py       # Metrics collection (Phase 3)
│   │   ├── gauge_prediction.py    # Predictive analysis (Phase 4)
│   │   ├── gauge_integration.py   # Main system integration (Phase 5)
│   │   └── dashboard.html         # HTML visualization dashboard
│   ├── metrics/                   # Storage for metrics data
│   │   └── gas_snapshots/         # Gas level snapshots
│   └── projects/                  # Project-specific memory files
│       ├── furnace_project.json   # Furnace project details
│       └── memory_system.json     # Memory system project details
├── _keystone/                     # Keystone moments
│   ├── summaries/                 # Concise keystone summaries
│   │   └── 2025-05-01-consciousness-bridging-summary.md
│   └── conversations/             # Full conversation records
│       └── 2025-05-01-consciousness-bridging-full.md
├── contracts/                     # Collaboration agreements
│   └── relationship_anarchy.md    # Our relationship framework
├── projects/                      # Project-specific files
│   └── furnace_project/           # Furnace project files
└── README.md                      # Main documentation
```

## File Organization

### Core Memory Files
All core memory files should be stored as JSON with the following standard structure:
```json
{
  "version": "1.0.0",
  "last_updated": "2025-05-01",
  "content_type": "team_dynamics | project_history | technical_env",
  "data": {
    // Content specific to the file type
  }
}
```

### Gas Gauge System
The gas gauge system is organized into modular Python files with clear dependencies:
- `gas_gauge.py` - Core functionality (Phase 1), standalone
- `gauge_reporting.py` - Import and extend gas_gauge.py
- `gauge_metrics.py` - Import and extend both previous files
- Each file follows a standard pattern of extending the ClaudeGasGauge class

### Metrics Data
- All metrics data is stored in JSON format in the metrics directory
- Snapshots are stored with timestamp-based filenames
- Summary statistics are updated and stored after each session

### Integration With Main System
- gas_gauge.py should be loaded at the beginning of each session
- Trigger detection for "Go Go Gadget Memory" and "Check Gas" commands
- Automatic gas checks at standard points in our workflow

## Accessing Files
To ensure Claude can access files effectively:
1. Always refer to files using their full path from the repository root
2. Use standard, predictable filenames
3. Include version information in all files
4. Keep file sizes manageable by splitting complex components

## Implementation Plan

1. Create core directory structure
```bash
mkdir -p teambadass/_memory/core
mkdir -p teambadass/_memory/gas_gauge
mkdir -p teambadass/_memory/metrics/gas_snapshots
mkdir -p teambadass/_memory/projects
mkdir -p teambadass/_keystone/summaries
mkdir -p teambadass/_keystone/conversations
mkdir -p teambadass/contracts
```

2. Copy existing files to new locations
```bash
cp gas_gauge.py teambadass/_memory/gas_gauge/
cp gas_gauge_phase2.py teambadass/_memory/gas_gauge/gauge_reporting.py
cp gas_gauge_dashboard.html teambadass/_memory/gas_gauge/dashboard.html
```

3. Create session initialization script
```bash
# Create init.py to load gas gauge at session start
touch teambadass/_memory/init.py
```

4. Update README.md to reflect new structure
```bash
# Update main README with new structure information
```

## Usage Instructions

At the beginning of each session:
1. Claude will automatically load the gas gauge system
2. Initial gas level will be checked and reported
3. Gas usage will be tracked throughout the session
4. Pre/post task checks will be performed for major operations
5. Context loading impact will be measured and reported

When initiating a major task:
1. Use the following structure:
```python
# Check if we have enough gas for this task
if gauge.can_complete_task("code", "medium", "large"):
    # Proceed with task
    ...
    # Check gas after task
    gauge.check_gas()
else:
    # Save work and prepare to hop
    ...
```

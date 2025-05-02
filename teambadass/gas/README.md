# MinimalTracker

Ultra-efficient session capacity tracking with background operation mode.

## Core Metrics
- Implementation cost: ~10% session
- Ongoing overhead: <0.5% per session
- Savings: ~29% per session vs dashboard approach
- Break-even: 1 session
- 5-session ROI: +145% capacity gain

## Key Features
- Silent background operation
- Threshold-only surfacing
- Consolidated metrics in single JSON
- Automated threshold adaptation
- Outlier detection

## Installation
Place `minimal_tracker.py` in:
```
teambadass/gas/minimal_tracker.py
```

## Usage Patterns

### Silent Initialization
```python
# Create instance
tracker = MinimalTracker()

# Initialize with context size (outputs nothing)
tracker.init_session(kb=80)
```

### Operation Registration (Silent)
```python
# Register operations (silent unless threshold)
result = tracker.register("code", complexity="high", size="large")
if result:  # Only outputs at thresholds
    print(result)
```

### Pre-task Assessment
```python
# Check before large operations
estimate = tracker.estimate("artifact", "high", "large")
print(f"Will use {estimate['cost']}%, {estimate['remaining']}% will remain")
if not estimate['proceed']:
    print(f"{estimate['status']}: {estimate['recommendation']}")
```

### Explicit Status Check
```python
# Only when explicitly requested
status = tracker.check()
print(f"{status['usage']}% used, {status['remaining']}% left")
```

### Session Transition
```python
# Prepare for hop and save metrics
hop = tracker.prepare_hop()
print(f"Session: {hop['usage']}% across {len(hop['ops'])} operations")
```

## Operation Types & Parameters

| Operation | Complexity | Size | Example |
|-----------|------------|------|---------|
| context | - | KB value | `register("context", size=80)` |
| code | low/med/high | small/med/large | `register("code", "high", "large")` |
| discuss | word count | - | `register("discuss", size=300)` |
| search | result count | - | `register("search", complexity=8)` |
| artifact | low/med/high | small/med/large | `register("artifact", "med", "large")` |
| plan | low/med/high | - | `register("plan", "high")` |

## Integration
Add to `init.py`:

```python
from teambadass.gas.minimal_tracker import MinimalTracker

# Create tracker in background
tracker = MinimalTracker()
tracker.init_session(kb=80)  # Register context size

# Register operations silently
def register_operation(op_type, **kwargs):
    result = tracker.register(op_type, **kwargs)
    if result:
        print(result)  # Only surface at thresholds
```

## Metrics Storage
Metrics are stored in `capacity_metrics.json` with:
- Last 10 sessions history
- Operation cost averages
- Threshold observations
- Significant outliers

## Advantages vs Dashboard
- <0.5% overhead vs ~30% for dashboard
- No visual code overhead
- Adapts based on actual observations
- Minimal impact on conversation
- Zero mention of gas/capacity unless needed
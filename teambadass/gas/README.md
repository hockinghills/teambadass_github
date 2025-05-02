# MinimalTracker

Ultra-efficient session capacity tracking with background operation mode.

## Key Metrics
- Implementation cost: ~5% session capacity
- Ongoing overhead: <0.5% per operation
- Savings: ~25% compared to previous implementations
- Break-even: Immediate (first session)

## Core Features
- Silent background operation
- Threshold-based notifications
- Consolidated metrics storage
- Operation cost estimation
- Adaptive thresholds

## Usage Patterns

### Silent Initialization
```python
# Create instance
tracker = MinimalTracker(silent=True)

# Initialize with context size (outputs nothing)
tracker.init_session(kb=80)
```

### Operation Registration
```python
# Register operations silently
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
print(f"Session: {hop['usage']}% across {hop['duration_mins']} minutes")
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

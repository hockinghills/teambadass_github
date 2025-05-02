#!/usr/bin/env python3
"""
Test script for minimal-tracker.py
"""

# Import the minimal tracker
from minimal_tracker import MinimalTracker

def run_test():
    print("Testing minimal-tracker.py...")
    
    # Create tracker in non-silent mode for testing
    tracker = MinimalTracker(silent=False)
    
    # Initialize with context loading
    print("\nInitializing with context loading...")
    tracker.init_session(kb=80)
    
    # Test various operations
    print("\nTesting operations...")
    
    # Code generation
    print("- Code generation (high, large):")
    result = tracker.register("code", "high", "large")
    
    # Discussion
    print("- Discussion (300 words):")
    tracker.register("discuss", size=300)
    
    # Artifact creation
    print("- Artifact creation (medium, medium):")
    tracker.register("artifact", "medium", "medium")
    
    # Check status
    print("\nCurrent status:")
    status = tracker.check()
    print(f"- Usage: {status['usage']}%")
    print(f"- Status: {status['status']}")
    print(f"- Operations: {status['op_count']}")
    print(f"- Duration: {status['mins']} minutes")
    
    # Try an estimation
    print("\nEstimating large artifact (high complexity):")
    estimate = tracker.estimate("artifact", "high", "large")
    print(f"- Cost: {estimate['cost']}%")
    print(f"- Post-task usage: {estimate['post']}%")
    print(f"- Recommendation: {estimate['recommendation']}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    run_test()

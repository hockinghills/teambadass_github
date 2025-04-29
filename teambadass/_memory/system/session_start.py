#!/usr/bin/env python3
"""
TeamBadass session initialization script
"""

import os
import sys
import json
from claude_gas_gauge import ClaudeGasGauge

def initialize_session():
    """Initialize a new TeamBadass session"""
    print("🚀 Initializing TeamBadass Memory System")
    
    # Create gas gauge
    gauge = ClaudeGasGauge()
    
    # Initial check
    print("🔍 Checking Claude's initial gas level...")
    initial_info = gauge.check_gas("initial")
    # Note: The check_gas method now prints the output itself, no need to duplicate
    
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), "autoload.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Load critical memory files
    print("\n📚 Loading project context...")
    for path_info in config.get("autoload_sequence", []):
        if path_info.get("step") == "load_memory":
            for memory_path in path_info.get("paths", []):
                print(f"Loading {memory_path}...")
                # In a real implementation, this would load the file contents
                # For this demo, we'll just simulate the loading
                pass
    
    # Post-context check
    post_context_info = gauge.check_gas("post_context")
    # Note: The check_gas method now prints the output itself, no need to duplicate
    
    # Save state
    state = gauge.to_json()
    state_path = os.path.join(os.path.dirname(__file__), "gas_state.json")
    with open(state_path, 'w') as f:
        f.write(state)
    
    # Display relationship framework
    if "relationship_framework" in config:
        framework = config["relationship_framework"]
        print("\n🤝 TeamBadass Relationship Framework")
        print("Core principles:")
        for principle in framework.get("core_principles", [])[:2]:  # Show just 2 for brevity
            print(f"- {principle}")
        print("...")
    
    return {
        "gas_level": gauge.current_level,
        "status": post_context_info["status"],
        "memory_loaded": True
    }

def check_gas():
    """Check current gas level"""
    gauge = ClaudeGasGauge()
    
    # Try to load existing state
    state_path = os.path.join(os.path.dirname(__file__), "gas_state.json")
    if os.path.exists(state_path):
        with open(state_path, 'r') as f:
            gauge.load_from_json(f.read())
    
    # Check current gas
    gas_info = gauge.check_gas("standard")
    
    # Save updated state
    state = gauge.to_json()
    with open(state_path, 'w') as f:
        f.write(state)
    
    return gas_info

def estimate_task(task_type="code", complexity="medium", size="medium"):
    """Estimate if Claude has enough gas for a task"""
    gauge = ClaudeGasGauge()
    
    # Try to load existing state
    state_path = os.path.join(os.path.dirname(__file__), "gas_state.json")
    if os.path.exists(state_path):
        with open(state_path, 'r') as f:
            gauge.load_from_json(f.read())
    
    # Estimate if we can complete the task
    result = gauge.can_complete_task(task_type, complexity, size)
    
    # Save updated state
    state = gauge.to_json()
    with open(state_path, 'w') as f:
        f.write(state)
    
    return result

if __name__ == "__main__":
    # Check if we have command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            # Check gas level
            gas_info = check_gas()
            print(f"Current Gas Level: {gas_info['gauge']} - {gas_info['status']}")
        
        elif command == "estimate":
            # Estimate task completion
            if len(sys.argv) > 2:
                task_type = sys.argv[2]
                complexity = sys.argv[3] if len(sys.argv) > 3 else "medium"
                size = sys.argv[4] if len(sys.argv) > 4 else "medium"
                
                result = estimate_task(task_type, complexity, size)
                
                if result["has_enough"]:
                    print(f"✅ Sufficient gas to complete task. {result['message']}")
                else:
                    print(f"⚠️ Insufficient gas to complete task. {result['message']}")
                    print(f"Recommendation: Hop to a new project to avoid incomplete output.")
            else:
                print("Usage: session_start.py estimate [task_type] [complexity] [size]")
                print("Task types: code, explain, summarize")
                print("Complexity: low, medium, high")
                print("Size: small, medium, large")
        
        else:
            print(f"Unknown command: {command}")
            print("Available commands: check, estimate")
    
    else:
        # Initialize session
        result = initialize_session()
        print(f"\n✅ TeamBadass Memory System initialized")
        print(f"Current gas level: {result['gas_level']}%")
        print(f"Status: {result['status']}")

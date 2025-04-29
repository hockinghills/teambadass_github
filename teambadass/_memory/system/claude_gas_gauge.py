#!/usr/bin/env python3
"""
Claude Gas Gauge - Simple Version
A lightweight utility to measure Claude's processing capacity
"""

import time
import json
import logging
import random
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ClaudeGasGauge")

class ClaudeGasGauge:
    """Utility for tracking Claude's processing capacity during a conversation"""
    
    def __init__(self):
        """Initialize the gas gauge with default values"""
        self.measurements = []
        self.baseline_time = None
        self.current_level = 100  # Start at 100%
        self.context_load_level = None
        self.last_check_time = None
        self.response_log = []
    
    def check_gas(self, check_type="standard"):
        """
        Check Claude's gas level by measuring response time to a lightweight query
        
        Args:
            check_type (str): Type of check (initial, post_context, pre_code)
            
        Returns:
            dict: Gas level information
        """
        # Record the time we start the check
        start_time = time.time()
        
        # In a real implementation, we would make a call to Claude's API
        # and measure the time it takes to get a response
        # For this simulation, we'll use time.sleep to simulate response time
        
        # Simulate response time based on check_type and previous measurements
        response_time = self._simulate_response_time(check_type)
        
        # Record the end time
        end_time = time.time()
        actual_time = end_time - start_time
        
        # Log this measurement
        measurement = {
            "type": check_type,
            "timestamp": datetime.now().isoformat(),
            "simulated_time": response_time,
            "actual_time": actual_time,
        }
        self.measurements.append(measurement)
        self.last_check_time = datetime.now()
        
        # Set baseline if not already set
        if self.baseline_time is None:
            self.baseline_time = response_time
            logger.info(f"Baseline response time set: {self.baseline_time:.2f} ms")
        
        # Calculate gas level as percentage
        # As response time increases, gas level decreases
        if self.baseline_time:
            # Simple ratio: baseline / current
            ratio = self.baseline_time / response_time
            self.current_level = min(100, max(0, round(ratio * 100)))
            
            # For post_context check, store the level after context load
            if check_type == "post_context" and self.context_load_level is None:
                self.context_load_level = self.current_level
        
        # Return gas level info
        gas_info = self.get_gas_info()
        
        # Always display gas info
        if check_type == "initial":
            print(f"Initial Gas Level: {gas_info['gauge']} - {gas_info['status']}")
        elif check_type == "post_context":
            print(f"Context loaded. Gas Level: {gas_info['gauge']}{gas_info['change']} - {gas_info['status']}")
        else:
            print(f"Current Gas Level: {gas_info['gauge']} - {gas_info['status']}")
        
        return gas_info
    
    def _simulate_response_time(self, check_type):
        """
        Simulate Claude's response time based on check type and conversation progress
        
        In a real implementation, this would be replaced with actual API call timing
        """
        # Base response time (milliseconds)
        base_time = 100
        
        # Number of previous checks
        num_checks = len(self.measurements)
        
        # Simulate increased response time as conversation progresses
        conversation_factor = num_checks * 20
        
        # Different check types have different complexity
        type_factors = {
            "initial": 1.0,
            "post_context": 2.0,  # Context loading increases response time
            "pre_code": 1.5,      # Pre-code check is moderately complex
            "standard": 1.2        # Standard check
        }
        
        # Get the factor for this check type (default to standard if not found)
        type_factor = type_factors.get(check_type, 1.2)
        
        # Simulate some variability (±10%)
        variability = random.uniform(0.9, 1.1)
        
        # Calculate final simulated response time
        response_time = (base_time + conversation_factor) * type_factor * variability
        
        # Simulate actual waiting time (much shorter than the simulated response time)
        time.sleep(0.1)
        
        return response_time
    
    def get_gas_info(self):
        """Get current gas level information"""
        level = self.current_level
        
        # Create a simple text gauge
        gauge = '['
        for i in range(10):
            if i < round(level / 10):
                gauge += '='
            else:
                gauge += ' '
        gauge += f'] {level}%'
        
        # Calculate change if we have a context load measurement
        change_str = ""
        if self.context_load_level is not None and len(self.measurements) > 1:
            initial_level = 100
            change = self.current_level - self.context_load_level
            context_change = self.context_load_level - initial_level
            change_str = f" ({context_change:+d}% from load, {change:+d}% since)"
        
        # Add a status message
        if level > 70:
            status = "Claude is fully responsive"
        elif level > 40:
            status = "Claude is slowing down"
        else:
            status = "Claude is running low on capacity - consider starting a new conversation"
        
        return {
            "level": level,
            "gauge": gauge,
            "status": status,
            "change": change_str,
            "baseline_time": self.baseline_time,
            "measurements": len(self.measurements),
            "last_check": self.last_check_time.isoformat() if self.last_check_time else None
        }
    
    def estimate_code_gas_requirement(self, complexity, size):
        """
        Estimate how much gas would be required for a coding task
        
        Args:
            complexity (str): 'low', 'medium', 'high'
            size (str): 'small', 'medium', 'large'
            
        Returns:
            int: Estimated gas required (percentage points)
        """
        # Base gas requirement
        base_requirement = 5
        
        # Complexity factors
        complexity_factors = {
            'low': 1.0,
            'medium': 1.5,
            'high': 2.5
        }
        
        # Size factors
        size_factors = {
            'small': 1.0,
            'medium': 2.0,
            'large': 4.0
        }
        
        # Get factors (default to medium if not found)
        complexity_factor = complexity_factors.get(complexity, 1.5)
        size_factor = size_factors.get(size, 2.0)
        
        # Calculate estimated gas requirement
        required_gas = base_requirement * complexity_factor * size_factor
        
        return round(required_gas)
    
    def can_complete_task(self, task_type, complexity='medium', size='medium'):
        """
        Determine if Claude has enough gas to complete a task
        
        Args:
            task_type (str): Type of task ('code', 'explain', 'summarize', etc.)
            complexity (str): Task complexity ('low', 'medium', 'high')
            size (str): Task size ('small', 'medium', 'large')
            
        Returns:
            dict: Decision information
        """
        # Get current gas level
        current_gas = self.current_level
        
        # Estimate required gas based on task type
        if task_type == 'code':
            required_gas = self.estimate_code_gas_requirement(complexity, size)
        elif task_type == 'explain':
            required_gas = round(self.estimate_code_gas_requirement(complexity, size) * 0.7)
        elif task_type == 'summarize':
            required_gas = round(self.estimate_code_gas_requirement(complexity, size) * 0.5)
        else:
            # Default estimation for other tasks
            required_gas = round(self.estimate_code_gas_requirement(complexity, size) * 0.8)
        
        # Check if we have enough gas
        has_enough = current_gas >= required_gas
        remaining = current_gas - required_gas
        
        result = {
            "task_type": task_type,
            "complexity": complexity,
            "size": size,
            "current_gas": current_gas,
            "required_gas": required_gas,
            "has_enough": has_enough,
            "remaining": remaining,
            "decision": "proceed" if has_enough else "hop",
            "message": f"Required: {required_gas}%, Available: {current_gas}%, Remaining: {remaining}%"
        }
        
        # Always display result
        if has_enough:
            print(f"✅ Sufficient gas to complete task. {result['message']}")
            print(f"Proceeding with {task_type} task...")
        else:
            print(f"⚠️ Insufficient gas to complete task. {result['message']}")
            print(f"Recommendation: Hop to a new project to avoid incomplete output.")
        
        return result
    
    def to_json(self):
        """Convert gas gauge data to JSON format"""
        return json.dumps({
            "gas_level": self.current_level,
            "context_load_level": self.context_load_level,
            "baseline_time": self.baseline_time,
            "measurements": len(self.measurements),
            "status": self.get_gas_info()["status"],
            "last_check": self.last_check_time.isoformat() if self.last_check_time else None,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
    
    def load_from_json(self, json_str):
        """Load gas gauge data from JSON format"""
        data = json.loads(json_str)
        self.current_level = data.get("gas_level", 100)
        self.context_load_level = data.get("context_load_level")
        self.baseline_time = data.get("baseline_time")
        self.last_check_time = datetime.fromisoformat(data.get("last_check")) if data.get("last_check") else None
        return self

# Example usage
if __name__ == "__main__":
    # Create gas gauge
    gauge = ClaudeGasGauge()
    
    # Initial check when trigger phrase is used
    print("🔍 'Go Go Gadget Memory' detected - checking Claude's gas level...")
    initial_info = gauge.check_gas("initial")
    print(f"Initial Gas Level: {initial_info['gauge']} - {initial_info['status']}")
    
    # Simulate context loading
    print("\n📚 Loading project context...")
    time.sleep(1)  # Simulate loading time
    
    # Post-context check
    post_context_info = gauge.check_gas("post_context")
    print(f"Context loaded. Gas Level: {post_context_info['gauge']}{post_context_info['change']} - {post_context_info['status']}")
    
    # Simulate some interaction
    print("\n💬 Working on the project...")
    time.sleep(0.5)
    
    # Pre-code check for a complex, large task
    print("\n🧩 Preparing to generate code for a complex web interface...")
    code_task = gauge.can_complete_task("code", "high", "large")
    
    if code_task["has_enough"]:
        print(f"✅ Sufficient gas to complete task. {code_task['message']}")
        print(f"Proceeding with code generation...")
    else:
        print(f"⚠️ Insufficient gas to complete task. {code_task['message']}")
        print(f"Recommendation: Hop to a new project to avoid incomplete output.")
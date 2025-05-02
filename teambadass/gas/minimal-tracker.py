#!/usr/bin/env python3
"""
FILE_OVERVIEW: minimal_tracker.py - Ultra-efficient session capacity tracker
VERSION: 2.0.0
LAST_UPDATED: 2025-05-02
DEPENDENCIES: None
IMPORTED_BY: init.py, auto_init.js

TABLE_OF_CONTENTS:
1. MinimalTracker Class - Core capacity tracking with silent operation
2. Operation Registration - Threshold-based operation tracking
3. Metrics Collection - Consolidated JSON metrics storage
4. Status Reporting - Minimal output with essential information
5. Command Integration - Direct integration with auto-init.js

SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
"""

import os
import json
import time
from datetime import datetime
import logging

# Configure minimal logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("MinimalTracker")

class MinimalTracker:
    """Ultra-minimal session capacity tracking with silent operation"""
    
    def __init__(self, silent=True):
        """Initialize tracker with optional silent mode"""
        self.usage = 0.0
        self.thresholds = {"warning": 60.0, "hard_stop": 90.0}
        self.operations = {}
        self.metrics_file = "capacity_metrics.json"
        self.start_time = datetime.now()
        self.session_id = f"session-{int(time.time())}"
        self.silent = silent
        
        # Observable indicators
        self.warning_observed = False
        self.warning_time = None
        self.hard_stop_observed = False
        self.hard_stop_time = None
        
        # Ensure metrics directory exists
        os.makedirs("metrics", exist_ok=True)
    
    def register(self, op_type, complexity=None, size=None):
        """Register operation with silent threshold detection"""
        cost = self._calculate_cost(op_type, complexity, size)
        pre_usage = self.usage
        self.usage += cost
        
        # Record operation
        if op_type not in self.operations:
            self.operations[op_type] = {"count": 0, "total_cost": 0}
        self.operations[op_type]["count"] += 1
        self.operations[op_type]["total_cost"] += cost
        
        # Check thresholds
        message = None
        if pre_usage < self.thresholds["warning"] and self.usage >= self.thresholds["warning"]:
            self.warning_observed = True
            self.warning_time = datetime.now()
            message = f"⚠️ Session at {self.usage:.1f}% capacity"
            
        elif pre_usage < self.thresholds["hard_stop"] and self.usage >= self.thresholds["hard_stop"]:
            self.hard_stop_observed = True
            self.hard_stop_time = datetime.now()
            message = f"🛑 Session at {self.usage:.1f}% capacity - critical"
        
        # Only output if not silent or threshold crossed
        if message and not self.silent:
            logger.info(message)
            
        return message
    
    def _calculate_cost(self, op_type, complexity=None, size=None):
        """Calculate operation cost with full operation matrix"""
        costs = {
            "context": {"base": 2.0, "per_kb": 0.05},
            "code": {"base": 3.0, "complexity": {"low": 1.0, "medium": 2.0, "high": 4.0}, 
                     "size": {"small": 1.0, "medium": 2.5, "large": 5.0}},
            "discuss": {"base": 1.0, "per_word": 0.01},
            "search": {"base": 4.0, "per_result": 0.5},
            "artifact": {"base": 5.0, "complexity": {"low": 1.0, "medium": 2.0, "high": 3.5}, 
                         "size": {"small": 1.0, "medium": 2.0, "large": 4.0}},
            "plan": {"base": 2.0, "complexity": {"low": 1.0, "medium": 2.0, "high": 3.0}}
        }
        
        complexity = complexity or "medium"
        size = size or "medium"
        
        if op_type == "context":
            kb = size if isinstance(size, (int, float)) else 50
            return costs["context"]["base"] + (costs["context"]["per_kb"] * kb)
            
        elif op_type in ["code", "artifact"]:
            c_factor = costs[op_type]["complexity"].get(complexity, costs[op_type]["complexity"]["medium"])
            s_factor = costs[op_type]["size"].get(size, costs[op_type]["size"]["medium"])
            return costs[op_type]["base"] * c_factor * s_factor
            
        elif op_type == "discuss":
            words = size if isinstance(size, (int, float)) else 200
            return costs["discuss"]["base"] + (costs["discuss"]["per_word"] * words)
            
        elif op_type == "search":
            results = complexity if isinstance(complexity, (int, float)) else 5
            return costs["search"]["base"] + (costs["search"]["per_result"] * results)
            
        elif op_type == "plan":
            c_factor = costs["plan"]["complexity"].get(complexity, costs["plan"]["complexity"]["medium"])
            return costs["plan"]["base"] * c_factor
            
        # Default fallback
        return 3.0
    
    def estimate(self, task, complexity="medium", size="medium"):
        """Estimate operation cost with decision support"""
        cost = self._calculate_cost(task, complexity, size)
        post_usage = self.usage + cost
        remaining = 100 - post_usage
        
        # Determine status and recommendation
        if post_usage >= self.thresholds["hard_stop"]:
            status = "CRITICAL"
            recommendation = "New session first"
            proceed = False
        elif post_usage >= self.thresholds["warning"]:
            status = "WARNING"
            recommendation = "Complete then hop"
            proceed = True
        elif post_usage >= self.thresholds["warning"] * 0.8:
            status = "CAUTION"
            recommendation = "Monitor capacity"
            proceed = True
        else:
            status = "NORMAL"
            recommendation = "Proceed"
            proceed = True
        
        # Return compact assessment
        return {
            "cost": round(cost, 1),
            "current": round(self.usage, 1),
            "post": round(post_usage, 1),
            "remaining": round(remaining, 1),
            "status": status,
            "recommendation": recommendation,
            "proceed": proceed
        }
    
    def check(self):
        """Explicit status check with minimal output"""
        status = "NORMAL"
        if self.usage >= self.thresholds["hard_stop"]: 
            status = "CRITICAL"
        elif self.usage >= self.thresholds["warning"]: 
            status = "WARNING"
        elif self.usage >= self.thresholds["warning"] * 0.8: 
            status = "CAUTION"
        
        # Return compact status report
        return {
            "usage": round(self.usage, 1),
            "remaining": round(100 - self.usage, 1),
            "status": status,
            "op_count": sum(op["count"] for op in self.operations.values()),
            "mins": round((datetime.now() - self.start_time).total_seconds() / 60, 1)
        }
    
    def save_metrics(self):
        """Save consolidated metrics to JSON file"""
        try:
            # Check for existing metrics file
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    metrics = json.load(f)
            else:
                metrics = {"sessions": [], "thresholds": [], "operations": {}}
            
            # Current session data
            session = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "session_id": self.session_id,
                "start": self.start_time.isoformat(),
                "end": datetime.now().isoformat(),
                "duration_mins": round((datetime.now() - self.start_time).total_seconds() / 60, 1),
                "operations": self.operations,
                "usage": round(self.usage, 1),
                "thresholds": self.thresholds,
                "warning_observed": self.warning_observed,
                "warning_time": self.warning_time.isoformat() if self.warning_time else None,
                "hard_stop_observed": self.hard_stop_observed,
                "hard_stop_time": self.hard_stop_time.isoformat() if self.hard_stop_time else None
            }
            
            # Add to sessions and keep only most recent 10
            metrics["sessions"].append(session)
            if len(metrics["sessions"]) > 10:
                metrics["sessions"] = metrics["sessions"][-10:]
            
            # Update operation metrics and threshold history
            for op_type, data in self.operations.items():
                if op_type not in metrics["operations"]:
                    metrics["operations"][op_type] = {"count": 0, "total_cost": 0}
                metrics["operations"][op_type]["count"] += data["count"]
                metrics["operations"][op_type]["total_cost"] += data["total_cost"]
            
            # Add thresholds to history
            metrics["thresholds"].append(self.thresholds)
            if len(metrics["thresholds"]) > 20:
                metrics["thresholds"] = metrics["thresholds"][-20:]
            
            # Calculate averages
            metrics["avg_warning"] = sum(t["warning"] for t in metrics["thresholds"]) / len(metrics["thresholds"])
            metrics["avg_hard_stop"] = sum(t["hard_stop"] for t in metrics["thresholds"]) / len(metrics["thresholds"])
            
            # Write to file
            with open(self.metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)
            
            return {"status": "success", "file": self.metrics_file}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def init_session(self, kb=0):
        """Initialize session with context loading"""
        if kb > 0:
            return self.register("context", size=kb)
        return None
    
    def prepare_hop(self):
        """Prepare for session hop with recommendations"""
        metrics = {
            "usage": round(self.usage, 1),
            "operations": self.operations,
            "duration_mins": round((datetime.now() - self.start_time).total_seconds() / 60, 1),
            "recommendation": self._get_hop_recommendation()
        }
        
        # Save metrics
        self.save_metrics()
        
        return metrics
    
    def _get_hop_recommendation(self):
        """Generate hop recommendation based on usage"""
        if self.usage >= 85: 
            return "Hop immediately"
        elif self.usage >= 70: 
            return "Hop recommended"
        else: 
            return "Hop optional"
    
    def register_threshold(self, threshold_type, value=None):
        """Register threshold observation with adaptation"""
        if threshold_type == "warning":
            self.thresholds["warning"] = value or self.usage
            return f"Warning updated: {self.thresholds['warning']}%"
        elif threshold_type == "hard_stop":
            self.thresholds["hard_stop"] = value or self.usage
            return f"Hard stop updated: {self.thresholds['hard_stop']}%"
        return f"Unknown threshold: {threshold_type}"
    
    def adapt_thresholds(self, warning=None, hard_stop=None):
        """Adapt thresholds with weighted average"""
        if warning:
            self.thresholds["warning"] = (warning * 0.7) + (self.thresholds["warning"] * 0.3)
            self.thresholds["warning"] = round(self.thresholds["warning"], 1)
        
        if hard_stop:
            self.thresholds["hard_stop"] = (hard_stop * 0.7) + (self.thresholds["hard_stop"] * 0.3)
            self.thresholds["hard_stop"] = round(self.thresholds["hard_stop"], 1)
        
        return self.thresholds
    
    def background_mode(self, enabled=True):
        """Toggle background operation (ultra-silent) mode"""
        self.silent = enabled
        return {"status": "success", "background_mode": enabled}


# Example usage
if __name__ == "__main__":
    # Create minimal tracker
    tracker = MinimalTracker(silent=False)
    
    # Initialize with context loading
    tracker.init_session(kb=80)
    
    # Register several operations
    operations = [
        ("code", "medium", "large"),
        ("discuss", None, 200),
        ("artifact", "high", "medium"),
        ("search", 5, None)
    ]
    
    for op in operations:
        if len(op) == 3:
            tracker.register(op[0], op[1], op[2])
        else:
            tracker.register(op[0])
    
    # Check status
    status = tracker.check()
    print(f"Session at {status['usage']}% capacity ({status['status']})")
    
    # Check specific operation estimate
    estimate = tracker.estimate("code", "high", "large")
    print(f"Large code estimate: {estimate['cost']}% cost, {estimate['recommendation']}")
    
    # Prepare for hop
    hop = tracker.prepare_hop()
    print(f"Session wrap-up: {hop['usage']}% used, {hop['recommendation']}")

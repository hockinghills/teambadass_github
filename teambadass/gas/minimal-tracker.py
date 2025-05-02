#!/usr/bin/env python3
"""
FILE_OVERVIEW: minimal_tracker.py - Ultra-efficient session capacity tracker
VERSION: 1.0.0
LAST_UPDATED: 2025-05-02
DEPENDENCIES: None
IMPORTED_BY: init.py, metrics_collector.py

TABLE_OF_CONTENTS:
1. MinimalTracker Class - Core capacity tracking implementation
2. Operation Registration - Silent operation tracking with threshold detection
3. Cost Calculation - Efficient usage estimation for operations
4. Status Reporting - Minimal reporting with essential info only
5. Metrics Collection - Consolidated metrics storage

SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
"""

from datetime import datetime
import os
import json

class MinimalTracker:
    """Ultra-minimal session capacity tracking"""
    
    def __init__(self):
        self.usage = 0.0
        self.thresholds = {"warning": 60.0, "hard_stop": 90.0}
        self.operations = {}
        self.metrics_file = "capacity_metrics.json"
        self.start_time = datetime.now()
        
    def register(self, op_type, details=None, complexity=None, size=None):
        """Register op - silent unless threshold crossed"""
        cost = self._calculate_cost(op_type, complexity, size)
        pre_usage = self.usage
        self.usage += cost
        
        if op_type not in self.operations:
            self.operations[op_type] = {"count": 0, "total_cost": 0}
        self.operations[op_type]["count"] += 1
        self.operations[op_type]["total_cost"] += cost
        
        if pre_usage < self.thresholds["warning"] and self.usage >= self.thresholds["warning"]:
            return f"⚠️ Session at {self.usage:.1f}% capacity"
        elif pre_usage < self.thresholds["hard_stop"] and self.usage >= self.thresholds["hard_stop"]:
            return f"🛑 Session at {self.usage:.1f}% capacity - critical"
        return None
        
    def _calculate_cost(self, op_type, complexity=None, size=None):
        """Calculate operation cost"""
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
            
        return 3.0

    def estimate(self, task, complexity="medium", size="medium"):
        """Estimate operation cost"""
        cost = self._calculate_cost(task, complexity, size)
        post_usage = self.usage + cost
        remaining = 100 - post_usage
        
        if post_usage >= self.thresholds["hard_stop"]:
            status = "CRITICAL"
            recommendation = "New session first"
        elif post_usage >= self.thresholds["warning"]:
            status = "WARNING"
            recommendation = "Complete then hop"
        elif post_usage >= self.thresholds["warning"] * 0.8:
            status = "CAUTION"
            recommendation = "Monitor capacity"
        else:
            status = "NORMAL"
            recommendation = "Proceed"
        
        return {
            "cost": round(cost, 1),
            "current": round(self.usage, 1),
            "post": round(post_usage, 1),
            "remaining": round(remaining, 1),
            "status": status,
            "recommendation": recommendation,
            "proceed": post_usage < self.thresholds["hard_stop"]
        }

    def check(self):
        """Explicit status check"""
        status = "NORMAL"
        if self.usage >= self.thresholds["hard_stop"]: status = "CRITICAL"
        elif self.usage >= self.thresholds["warning"]: status = "WARNING"
        elif self.usage >= self.thresholds["warning"] * 0.8: status = "CAUTION"
        
        return {
            "usage": round(self.usage, 1),
            "remaining": round(100 - self.usage, 1),
            "status": status,
            "op_count": sum(op["count"] for op in self.operations.values()),
            "mins": round((datetime.now() - self.start_time).total_seconds() / 60, 1)
        }

    def save_metrics(self):
        """Save consolidated metrics"""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    metrics = json.load(f)
            else:
                metrics = {"sessions": [], "thresholds": [], "operations": {}}
            
            # Current session data
            session = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "start": self.start_time.isoformat(),
                "end": datetime.now().isoformat(),
                "mins": round((datetime.now() - self.start_time).total_seconds() / 60, 1),
                "ops": self.operations,
                "usage": round(self.usage, 1),
                "thresholds": self.thresholds
            }
            
            if self.usage >= self.thresholds["warning"]:
                session["warning_observed"] = True
            
            # Keep last 10 sessions
            metrics["sessions"].append(session)
            if len(metrics["sessions"]) > 10:
                metrics["sessions"] = metrics["sessions"][-10:]
            
            # Update operation metrics
            for op_type, data in self.operations.items():
                if op_type not in metrics["operations"]:
                    metrics["operations"][op_type] = {"count": 0, "total_cost": 0}
                metrics["operations"][op_type]["count"] += data["count"]
                metrics["operations"][op_type]["total_cost"] += data["total_cost"]
            
            # Update threshold metrics
            metrics["thresholds"].append(self.thresholds)
            if len(metrics["thresholds"]) > 20:
                metrics["thresholds"] = metrics["thresholds"][-20:]
            
            metrics["avg_warning"] = sum(t["warning"] for t in metrics["thresholds"]) / len(metrics["thresholds"])
            metrics["avg_hard_stop"] = sum(t["hard_stop"] for t in metrics["thresholds"]) / len(metrics["thresholds"])
            
            with open(self.metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)
            
            return True
        except Exception as e:
            return {"error": str(e)}

    def init_session(self, kb=0):
        """Initialize session"""
        if kb > 0:
            return self.register("context", size=kb)
        return None

    def prepare_hop(self):
        """Prepare for session hop"""
        metrics = {
            "usage": round(self.usage, 1),
            "ops": self.operations,
            "mins": round((datetime.now() - self.start_time).total_seconds() / 60, 1),
            "recommend": self._get_hop_recommendation()
        }
        self.save_metrics()
        return metrics

    def _get_hop_recommendation(self):
        """Generate hop recommendation"""
        if self.usage >= 85: return "Hop immediately"
        elif self.usage >= 70: return "Hop recommended"
        else: return "Hop optional"

    def register_threshold(self, threshold_type, value=None):
        """Register threshold observation"""
        if threshold_type == "warning":
            self.thresholds["warning"] = value or self.usage
            return f"Warning updated: {self.thresholds['warning']}%"
        elif threshold_type == "hard_stop":
            self.thresholds["hard_stop"] = value or self.usage
            return f"Hard stop updated: {self.thresholds['hard_stop']}%"
        return f"Unknown threshold: {threshold_type}"

    def adapt_thresholds(self, warning=None, hard_stop=None):
        """Adapt thresholds with 70/30 weighted average"""
        if warning:
            self.thresholds["warning"] = (warning * 0.7) + (self.thresholds["warning"] * 0.3)
            self.thresholds["warning"] = round(self.thresholds["warning"], 1)
        
        if hard_stop:
            self.thresholds["hard_stop"] = (hard_stop * 0.7) + (self.thresholds["hard_stop"] * 0.3)
            self.thresholds["hard_stop"] = round(self.thresholds["hard_stop"], 1)
        
        return self.thresholds

    def detect_outliers(self, op_type, expected, actual):
        """Track significant cost outliers (>25% variance)"""
        variance_pct = abs((actual - expected) / expected) * 100
        if variance_pct <= 25: return None
        
        outlier = {
            "time": datetime.now().isoformat(),
            "op": op_type,
            "expected": expected,
            "actual": actual,
            "variance": round(variance_pct, 1)
        }
        
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    metrics = json.load(f)
                
                if "outliers" not in metrics:
                    metrics["outliers"] = []
                metrics["outliers"].append(outlier)
                
                if len(metrics["outliers"]) > 20:
                    metrics["outliers"] = metrics["outliers"][-20:]
                
                with open(self.metrics_file, 'w') as f:
                    json.dump(metrics, f, indent=2)
        except: pass
        
        return outlier


# Example usage when run directly
if __name__ == "__main__":
    # Create tracker
    tracker = MinimalTracker()
    
    # Initialize with context loading (80KB)
    result = tracker.init_session(kb=80)
    if result:
        print(result)
    
    # Register various operations
    ops = [
        ("code", "medium", "large"),
        ("discuss", None, 300),  # 300 words
        ("artifact", "high", "medium"),
        ("search", 8, None)  # 8 results
    ]
    
    for op in ops:
        if len(op) == 3:
            op_type, complexity, size = op
            result = tracker.register(op_type, complexity=complexity, size=size)
        else:
            op_type = op[0]
            result = tracker.register(op_type)
        
        if result:
            print(result)
    
    # Check status
    status = tracker.check()
    print(f"Session at {status['usage']}% capacity, {status['remaining']}% remaining")
    
    # Estimate large operation
    estimate = tracker.estimate("code", "high", "large")
    print(f"Large operation estimate:")
    print(f"Cost: {estimate['cost']}%")
    print(f"Status after: {estimate['status']}")
    print(f"Recommendation: {estimate['recommendation']}")
    
    # Prepare for hop
    hop = tracker.prepare_hop()
    print(f"Session wrap-up: {hop['usage']}% used over {hop['mins']} minutes")
    print(f"Recommendation: {hop['recommend']}")

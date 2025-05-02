#!/usr/bin/env python3
"""
TeamBadass Observable Gas Gauge System
A realistic resource monitoring system based on observable indicators
"""

import json
import os
import time
from datetime import datetime

class ObservableGasGauge:
    """
    Resource monitoring system based on observable indicators rather than
    simulated measurements. Maps session capacity based on empirical observations.
    """
    
    def __init__(self):
        """Initialize the gas gauge with default values"""
        self.session_start_time = datetime.now()
        self.last_check_time = datetime.now()
        self.estimated_usage = 0  # Percentage of session used (estimated)
        self.long_chats_warning_threshold = 60  # Initial guess - will be refined
        self.hard_stop_threshold = 95  # Initial guess - will be refined
        self.six_hour_limit_exceeded = False
        
        # Load resource map if it exists
        self.resource_map = self._load_resource_map()
        
        # Initialize operation counters
        self.operations = {
            "context_loading": 0,
            "code_generation": 0,
            "discussion_exchanges": 0,
            "search_operations": 0,
            "artifacts_created": 0
        }
        
        # Initialize timestamp markers
        self.markers = {
            "session_start": self.session_start_time,
            "long_chats_warning": None,
            "hard_stop": None
        }
        
        # Log session initialization
        self._log_event("session_initialized")
    
    def _load_resource_map(self):
        """Load the resource map from file if it exists, otherwise use defaults"""
        map_path = os.path.join("teambadass", "_memory", "metrics", "resource_map.json")
        
        try:
            if os.path.exists(map_path):
                with open(map_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading resource map: {e}")
        
        # Return default resource map if file doesn't exist or loading fails
        return {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "operation_costs": {
                "context_loading": {
                    "per_kb": 0.05,  # Estimated percentage per KB loaded
                    "base_cost": 2.0  # Base percentage for any context loading
                },
                "code_generation": {
                    "complexity_factors": {
                        "low": 1.0,
                        "medium": 2.0,
                        "high": 4.0
                    },
                    "size_factors": {
                        "small": 1.0,
                        "medium": 2.5,
                        "large": 5.0
                    },
                    "base_cost": 3.0
                },
                "discussion_exchange": {
                    "base_cost": 1.0,  # Cost per message exchange
                    "per_word": 0.01   # Additional cost per word
                },
                "search_operation": {
                    "base_cost": 4.0,  # Base cost for any search
                    "per_result": 0.5  # Additional cost per result processed
                },
                "artifact_creation": {
                    "complexity_factors": {
                        "low": 1.0,
                        "medium": 2.0,
                        "high": 3.5
                    },
                    "size_factors": {
                        "small": 1.0,
                        "medium": 2.0,
                        "large": 4.0
                    },
                    "base_cost": 5.0
                }
            },
            "thresholds": {
                "long_chats_warning": 60,  # Percentage where warning appears
                "hard_stop": 95           # Percentage where session ends
            },
            "observed_sessions": []
        }
    
    def _save_resource_map(self):
        """Save the current resource map to file"""
        map_path = os.path.join("teambadass", "_memory", "metrics", "resource_map.json")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(map_path), exist_ok=True)
        
        # Update last_updated timestamp
        self.resource_map["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(map_path, 'w') as f:
                json.dump(self.resource_map, indent=2, f)
            print(f"Resource map saved to {map_path}")
        except Exception as e:
            print(f"Error saving resource map: {e}")
    
    def _log_event(self, event_type, details=None):
        """Log an event for later analysis"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "estimated_usage": self.estimated_usage,
            "operations": self.operations.copy()
        }
        
        # Add additional details if provided
        if details:
            log_entry["details"] = details
        
        # Add to session log
        if "session_log" not in self.resource_map:
            self.resource_map["session_log"] = []
        
        self.resource_map["session_log"].append(log_entry)
    
    def register_context_loading(self, size_kb):
        """
        Register context loading operation
        
        Args:
            size_kb (float): Size of loaded context in KB
        """
        operation_costs = self.resource_map["operation_costs"]["context_loading"]
        usage_increase = operation_costs["base_cost"] + (operation_costs["per_kb"] * size_kb)
        
        self.estimated_usage += usage_increase
        self.operations["context_loading"] += size_kb
        
        self._log_event("context_loading", {"size_kb": size_kb, "usage_increase": usage_increase})
        
        return self._format_status_update("Context Loading", size_kb, usage_increase)
    
    def register_code_generation(self, complexity="medium", size="medium"):
        """
        Register code generation operation
        
        Args:
            complexity (str): Complexity level (low, medium, high)
            size (str): Size level (small, medium, large)
        """
        operation_costs = self.resource_map["operation_costs"]["code_generation"]
        
        # Get complexity and size factors (default to medium if invalid)
        complexity_factor = operation_costs["complexity_factors"].get(
            complexity, operation_costs["complexity_factors"]["medium"]
        )
        size_factor = operation_costs["size_factors"].get(
            size, operation_costs["size_factors"]["medium"]
        )
        
        # Calculate usage increase
        usage_increase = operation_costs["base_cost"] * complexity_factor * size_factor
        
        self.estimated_usage += usage_increase
        self.operations["code_generation"] += 1
        
        self._log_event("code_generation", {
            "complexity": complexity,
            "size": size,
            "usage_increase": usage_increase
        })
        
        return self._format_status_update("Code Generation", f"{complexity} complexity, {size} size", usage_increase)
    
    def register_discussion_exchange(self, words=100):
        """
        Register a discussion exchange (question and answer)
        
        Args:
            words (int): Approximate word count in the exchange
        """
        operation_costs = self.resource_map["operation_costs"]["discussion_exchange"]
        usage_increase = operation_costs["base_cost"] + (operation_costs["per_word"] * words)
        
        self.estimated_usage += usage_increase
        self.operations["discussion_exchanges"] += 1
        
        self._log_event("discussion_exchange", {"words": words, "usage_increase": usage_increase})
        
        return self._format_status_update("Discussion Exchange", f"{words} words", usage_increase)
    
    def register_search_operation(self, results_count=5):
        """
        Register a search operation
        
        Args:
            results_count (int): Number of search results processed
        """
        operation_costs = self.resource_map["operation_costs"]["search_operation"]
        usage_increase = operation_costs["base_cost"] + (operation_costs["per_result"] * results_count)
        
        self.estimated_usage += usage_increase
        self.operations["search_operations"] += 1
        
        self._log_event("search_operation", {"results_count": results_count, "usage_increase": usage_increase})
        
        return self._format_status_update("Search Operation", f"{results_count} results", usage_increase)
    
    def register_artifact_creation(self, complexity="medium", size="medium"):
        """
        Register artifact creation
        
        Args:
            complexity (str): Complexity level (low, medium, high)
            size (str): Size level (small, medium, large)
        """
        operation_costs = self.resource_map["operation_costs"]["artifact_creation"]
        
        # Get complexity and size factors (default to medium if invalid)
        complexity_factor = operation_costs["complexity_factors"].get(
            complexity, operation_costs["complexity_factors"]["medium"]
        )
        size_factor = operation_costs["size_factors"].get(
            size, operation_costs["size_factors"]["medium"]
        )
        
        # Calculate usage increase
        usage_increase = operation_costs["base_cost"] * complexity_factor * size_factor
        
        self.estimated_usage += usage_increase
        self.operations["artifacts_created"] += 1
        
        self._log_event("artifact_creation", {
            "complexity": complexity,
            "size": size,
            "usage_increase": usage_increase
        })
        
        return self._format_status_update("Artifact Creation", f"{complexity} complexity, {size} size", usage_increase)
    
    def register_long_chats_warning(self):
        """Register that the 'long chats' warning has appeared"""
        self.markers["long_chats_warning"] = datetime.now()
        
        # Calculate actual percentage when warning appeared
        elapsed = (self.markers["long_chats_warning"] - self.markers["session_start"]).total_seconds()
        
        # Log the event
        self._log_event("long_chats_warning", {
            "elapsed_seconds": elapsed,
            "estimated_usage": self.estimated_usage
        })
        
        # Adjust our threshold based on this observation
        self._adjust_long_chats_threshold(self.estimated_usage)
        
        return {
            "status": "Long Chats Warning Registered",
            "timestamp": self.markers["long_chats_warning"].isoformat(),
            "estimated_usage_at_warning": self.estimated_usage,
            "new_threshold": self.resource_map["thresholds"]["long_chats_warning"]
        }
    
    def register_hard_stop(self):
        """Register that a hard stop has occurred (session ended)"""
        self.markers["hard_stop"] = datetime.now()
        
        # Calculate actual percentage when hard stop occurred
        elapsed = (self.markers["hard_stop"] - self.markers["session_start"]).total_seconds()
        
        # Log the event
        self._log_event("hard_stop", {
            "elapsed_seconds": elapsed,
            "estimated_usage": self.estimated_usage
        })
        
        # Adjust our threshold based on this observation
        self._adjust_hard_stop_threshold(self.estimated_usage)
        
        return {
            "status": "Hard Stop Registered",
            "timestamp": self.markers["hard_stop"].isoformat(),
            "estimated_usage_at_stop": self.estimated_usage,
            "new_threshold": self.resource_map["thresholds"]["hard_stop"]
        }
    
    def register_six_hour_limit(self):
        """Register that the six-hour limit has been hit"""
        self.six_hour_limit_exceeded = True
        
        # Log the event
        self._log_event("six_hour_limit", {
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "status": "Six Hour Limit Registered",
            "timestamp": datetime.now().isoformat(),
            "remaining_time": "Approximately 1 hour before reset"
        }
    
    def _adjust_long_chats_threshold(self, observed_percentage):
        """
        Adjust our threshold based on observed warning appearance
        
        This uses a weighted average that gives more weight to recent observations
        but doesn't completely discard our previous understanding.
        """
        current_threshold = self.resource_map["thresholds"]["long_chats_warning"]
        
        # Use a weighted average (70% new observation, 30% previous threshold)
        new_threshold = (observed_percentage * 0.7) + (current_threshold * 0.3)
        
        # Update the threshold
        self.resource_map["thresholds"]["long_chats_warning"] = round(new_threshold, 1)
        
        # Save the updated resource map
        self._save_resource_map()
    
    def _adjust_hard_stop_threshold(self, observed_percentage):
        """
        Adjust our hard stop threshold based on observed session end
        
        This uses a weighted average that gives more weight to recent observations
        but doesn't completely discard our previous understanding.
        """
        current_threshold = self.resource_map["thresholds"]["hard_stop"]
        
        # Use a weighted average (70% new observation, 30% previous threshold)
        new_threshold = (observed_percentage * 0.7) + (current_threshold * 0.3)
        
        # Update the threshold
        self.resource_map["thresholds"]["hard_stop"] = round(new_threshold, 1)
        
        # Save the updated resource map
        self._save_resource_map()
    
    def check_status(self):
        """
        Check current status and provide recommendations
        
        Returns:
            dict: Status information and recommendations
        """
        self.last_check_time = datetime.now()
        session_duration = (self.last_check_time - self.session_start_time).total_seconds() / 60.0
        
        # Generate ASCII gauge
        gauge_str = self._generate_ascii_gauge()
        
        # Create status report
        status = {
            "timestamp": self.last_check_time.isoformat(),
            "session_duration_minutes": round(session_duration, 1),
            "estimated_usage_percentage": round(self.estimated_usage, 1),
            "ascii_gauge": gauge_str,
            "operations_summary": self.operations,
            "thresholds": {
                "long_chats_warning": self.resource_map["thresholds"]["long_chats_warning"],
                "hard_stop": self.resource_map["thresholds"]["hard_stop"]
            },
            "remaining_capacity": round(100 - self.estimated_usage, 1)
        }
        
        # Add recommendations based on usage
        if self.estimated_usage >= self.resource_map["thresholds"]["hard_stop"]:
            status["status"] = "CRITICAL"
            status["recommendations"] = [
                "Emergency continuity generation required",
                "Hop immediately to avoid data loss",
                "Split any remaining work into a new session"
            ]
        elif self.estimated_usage >= self.resource_map["thresholds"]["long_chats_warning"]:
            status["status"] = "WARNING"
            status["recommendations"] = [
                "Prepare to wrap up current work",
                "Generate continuity documentation",
                "Plan for session hop"
            ]
        elif self.estimated_usage >= self.resource_map["thresholds"]["long_chats_warning"] * 0.8:
            status["status"] = "CAUTION"
            status["recommendations"] = [
                "Approaching 'long chats' warning threshold",
                "Complete current high-priority tasks",
                "Avoid starting new complex operations"
            ]
        else:
            status["status"] = "NORMAL"
            status["recommendations"] = [
                "Sufficient capacity for planned operations",
                "Continue with current work plan"
            ]
        
        # Log the status check
        self._log_event("status_check", status)
        
        return status
    
    def estimate_task_capacity(self, task_type, complexity="medium", size="medium", count=1):
        """
        Estimate if enough capacity remains for a planned task
        
        Args:
            task_type (str): Type of task (code, discussion, search, artifact)
            complexity (str): Complexity level (low, medium, high)
            size (str): Size level (small, medium, large)
            count (int): Number of operations
            
        Returns:
            dict: Estimation results
        """
        # Map task type to operation type
        operation_map = {
            "code": "code_generation",
            "discussion": "discussion_exchange",
            "search": "search_operation",
            "artifact": "artifact_creation",
            "context": "context_loading"
        }
        
        operation_type = operation_map.get(task_type)
        if not operation_type:
            return {
                "status": "ERROR",
                "message": f"Unknown task type: {task_type}",
                "valid_types": list(operation_map.keys())
            }
        
        # Estimate cost based on operation type
        if operation_type == "code_generation":
            cost = self._estimate_code_cost(complexity, size) * count
        elif operation_type == "discussion_exchange":
            cost = self._estimate_discussion_cost(size) * count
        elif operation_type == "search_operation":
            cost = self._estimate_search_cost(complexity) * count
        elif operation_type == "artifact_creation":
            cost = self._estimate_artifact_cost(complexity, size) * count
        elif operation_type == "context_loading":
            cost = self._estimate_context_cost(size) * count
        
        # Check if we have enough capacity
        remaining = 100 - self.estimated_usage
        has_capacity = remaining >= cost
        will_exceed_warning = (self.estimated_usage + cost) >= self.resource_map["thresholds"]["long_chats_warning"]
        will_exceed_hard_stop = (self.estimated_usage + cost) >= self.resource_map["thresholds"]["hard_stop"]
        
        # Create result
        result = {
            "task_type": task_type,
            "complexity": complexity,
            "size": size,
            "count": count,
            "estimated_cost": round(cost, 1),
            "current_usage": round(self.estimated_usage, 1),
            "remaining_capacity": round(remaining, 1),
            "has_capacity": has_capacity,
            "will_exceed_warning": will_exceed_warning,
            "will_exceed_hard_stop": will_exceed_hard_stop
        }
        
        # Add status and recommendation
        if will_exceed_hard_stop:
            result["status"] = "CRITICAL"
            result["recommendation"] = "Do not proceed - hop to new session first"
        elif will_exceed_warning:
            result["status"] = "WARNING"
            result["recommendation"] = "Proceed with caution - prepare for hop afterwards"
        elif remaining <= cost * 1.5:
            result["status"] = "CAUTION"
            result["recommendation"] = "Capacity tight - complete task and prepare for hop"
        else:
            result["status"] = "NORMAL"
            result["recommendation"] = "Sufficient capacity - proceed as planned"
        
        return result
    
    def _estimate_code_cost(self, complexity, size):
        """Estimate the cost of code generation"""
        operation_costs = self.resource_map["operation_costs"]["code_generation"]
        
        complexity_factor = operation_costs["complexity_factors"].get(
            complexity, operation_costs["complexity_factors"]["medium"]
        )
        size_factor = operation_costs["size_factors"].get(
            size, operation_costs["size_factors"]["medium"]
        )
        
        return operation_costs["base_cost"] * complexity_factor * size_factor
    
    def _estimate_discussion_cost(self, size):
        """Estimate the cost of a discussion exchange"""
        operation_costs = self.resource_map["operation_costs"]["discussion_exchange"]
        
        # Map size to approximate word count
        word_counts = {
            "small": 50,
            "medium": 200,
            "large": 500
        }
        
        words = word_counts.get(size, word_counts["medium"])
        
        return operation_costs["base_cost"] + (operation_costs["per_word"] * words)
    
    def _estimate_search_cost(self, complexity):
        """Estimate the cost of a search operation"""
        operation_costs = self.resource_map["operation_costs"]["search_operation"]
        
        # Map complexity to approximate result count
        result_counts = {
            "low": 3,
            "medium": 5,
            "high": 10
        }
        
        results = result_counts.get(complexity, result_counts["medium"])
        
        return operation_costs["base_cost"] + (operation_costs["per_result"] * results)
    
    def _estimate_artifact_cost(self, complexity, size):
        """Estimate the cost of artifact creation"""
        operation_costs = self.resource_map["operation_costs"]["artifact_creation"]
        
        complexity_factor = operation_costs["complexity_factors"].get(
            complexity, operation_costs["complexity_factors"]["medium"]
        )
        size_factor = operation_costs["size_factors"].get(
            size, operation_costs["size_factors"]["medium"]
        )
        
        return operation_costs["base_cost"] * complexity_factor * size_factor
    
    def _estimate_context_cost(self, size):
        """Estimate the cost of context loading"""
        operation_costs = self.resource_map["operation_costs"]["context_loading"]
        
        # Map size to approximate KB
        kb_sizes = {
            "small": 10,
            "medium": 50,
            "large": 200
        }
        
        kb = kb_sizes.get(size, kb_sizes["medium"])
        
        return operation_costs["base_cost"] + (operation_costs["per_kb"] * kb)
    
    def pre_task_assessment(self, task_name, task_type, complexity="medium", size="medium"):
        """
        Perform a pre-task assessment to aid in collaborative decision-making
        
        Args:
            task_name (str): Name or brief description of the task
            task_type (str): Type of task (code, discussion, search, artifact)
            complexity (str): Complexity level (low, medium, high)
            size (str): Size level (small, medium, large)
            
        Returns:
            dict: Assessment results with recommendations
        """
        # Check current status
        status = self.check_status()
        
        # Estimate task capacity
        capacity = self.estimate_task_capacity(task_type, complexity, size)
        
        # Calculate post-task estimated usage
        post_task_usage = self.estimated_usage + capacity["estimated_cost"]
        
        # Generate gauge for post-task state
        post_task_gauge = self._generate_ascii_gauge(usage=post_task_usage)
        
        # Create decision options
        options = []
        
        if capacity["will_exceed_hard_stop"]:
            options.append({
                "option": "Hop Session",
                "description": "Start a new session before attempting this task",
                "recommendation_level": "Strong"
            })
            options.append({
                "option": "Break Into Chunks",
                "description": f"Split into smaller {size} chunks of {complexity} complexity",
                "recommendation_level": "Alternative"
            })
        elif capacity["will_exceed_warning"]:
            options.append({
                "option": "Proceed & Hop",
                "description": "Complete task then immediately hop to new session",
                "recommendation_level": "Strong"
            })
            options.append({
                "option": "Break Into Chunks",
                "description": f"Split into smaller {size} chunks of {complexity} complexity",
                "recommendation_level": "Alternative"
            })
        elif post_task_usage > self.resource_map["thresholds"]["long_chats_warning"] * 0.8:
            options.append({
                "option": "Proceed With Caution",
                "description": "Complete task but prepare for potential hop afterwards",
                "recommendation_level": "Standard"
            })
            options.append({
                "option": "Break Into Chunks",
                "description": f"Split into smaller {size} chunks of {complexity} complexity",
                "recommendation_level": "Alternative"
            })
        else:
            options.append({
                "option": "Proceed As Planned",
                "description": "Sufficient capacity for this task and more",
                "recommendation_level": "Standard"
            })
        
        # Create multi-task checklist option if appropriate
        if capacity["will_exceed_warning"] or complexity == "high":
            options.append({
                "option": "Multi-Session Project",
                "description": "Create a checklist across multiple sessions",
                "recommendation_level": "Consider"
            })
        
        # Create final assessment
        assessment = {
            "task_name": task_name,
            "task_type": task_type,
            "complexity": complexity,
            "size": size,
            "current_status": status["ascii_gauge"],
            "estimated_cost": f"{capacity['estimated_cost']}%",
            "post_task_status": post_task_gauge,
            "remaining_capacity": f"{status['remaining_capacity']}%",
            "post_task_remaining": f"{round(100 - post_task_usage, 1)}%",
            "decision_options": options
        }
        
        # Log the assessment
        self._log_event("pre_task_assessment", assessment)
        
        return assessment
    
    def _generate_ascii_gauge(self, width=30, usage=None):
        """
        Generate an ASCII gauge representation of usage
        
        Args:
            width (int): Width of the gauge in characters
            usage (float, optional): Override usage value (for predictions)
            
        Returns:
            str: Formatted ASCII gauge
        """
        # Get current usage and thresholds
        level = usage if usage is not None else self.estimated_usage
        warning_threshold = self.resource_map["thresholds"]["long_chats_warning"]
        hard_stop_threshold = self.resource_map["thresholds"]["hard_stop"]
        
        # Calculate filled portion
        filled_width = int((level / 100) * width)
        warning_pos = int((warning_threshold / 100) * width)
        hard_stop_pos = int((hard_stop_threshold / 100) * width)
        
        # Build the gauge
        gauge = "["
        for i in range(width):
            if i < filled_width:
                gauge += "="  # Filled portion
            elif i == warning_pos:
                gauge += "W"  # Warning threshold marker
            elif i == hard_stop_pos:
                gauge += "H"  # Hard stop threshold marker
            else:
                gauge += " "  # Empty portion
        gauge += f"] {round(level, 1)}%"
        
        # Determine status label
        if level >= hard_stop_threshold:
            status = "CRITICAL"
        elif level >= warning_threshold:
            status = "WARNING"
        elif level >= warning_threshold * 0.8:
            status = "CAUTION"
        else:
            status = "NORMAL"
        
        return f"{gauge} - {status}"
    
    def _format_status_update(self, operation_type, details, usage_increase):
        """Format a status update after an operation is registered"""
        # Generate ASCII gauge
        gauge_str = self._generate_ascii_gauge()
        
        return {
            "operation": operation_type,
            "details": details,
            "usage_increase": round(usage_increase, 1),
            "total_estimated_usage": round(self.estimated_usage, 1),
            "remaining_capacity": round(100 - self.estimated_usage, 1),
            "ascii_gauge": gauge_str,
            "status": self._get_status_label()
        }
    
    def _get_status_label(self):
        """Get a status label based on current usage"""
        if self.estimated_usage >= self.resource_map["thresholds"]["hard_stop"]:
            return "CRITICAL"
        elif self.estimated_usage >= self.resource_map["thresholds"]["long_chats_warning"]:
            return "WARNING"
        elif self.estimated_usage >= self.resource_map["thresholds"]["long_chats_warning"] * 0.8:
            return "CAUTION"
        else:
            return "NORMAL"
    
    def generate_report(self):
        """Generate a comprehensive report of the current session"""
        status = self.check_status()
        
        # Calculate time metrics
        session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60.0
        time_to_warning = None
        
        if self.markers["long_chats_warning"]:
            warning_duration = (self.markers["long_chats_warning"] - self.session_start_time).total_seconds() / 60.0
            time_to_warning = warning_duration
        
        # Create report
        report = {
            "session_id": self.session_start_time.strftime("%Y%m%d%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "session_duration_minutes": round(session_duration, 1),
            "estimated_usage_percentage": round(self.estimated_usage, 1),
            "warning_threshold": self.resource_map["thresholds"]["long_chats_warning"],
            "hard_stop_threshold": self.resource_map["thresholds"]["hard_stop"],
            "time_to_warning_minutes": round(time_to_warning, 1) if time_to_warning else None,
            "operations_summary": self.operations,
            "status": status["status"],
            "recommendations": status["recommendations"],
            "six_hour_limit_exceeded": self.six_hour_limit_exceeded
        }
        
        # Add markers if they exist
        for marker_name, marker_time in self.markers.items():
            if marker_time:
                report[f"{marker_name}_timestamp"] = marker_time.isoformat()
        
        # Add to observed sessions
        self.resource_map["observed_sessions"].append(report)
        
        # Save the updated resource map
        self._save_resource_map()
        
        return report
    
    def generate_continuity(self):
        """
        Generate continuity information for the next session
        
        Returns:
            dict: Continuity information
        """
        report = self.generate_report()
        
        # Create continuity information
        continuity = {
            "previous_session_id": report["session_id"],
            "timestamp": datetime.now().isoformat(),
            "operations_completed": self.operations,
            "estimated_usage_percentage": round(self.estimated_usage, 1),
            "threshold_adjustments": {
                "long_chats_warning": self.resource_map["thresholds"]["long_chats_warning"],
                "hard_stop": self.resource_map["thresholds"]["hard_stop"]
            },
            "six_hour_limit_status": {
                "exceeded": self.six_hour_limit_exceeded,
                "reset_time": datetime.now().isoformat() if self.six_hour_limit_exceeded else None
            }
        }
        
        # Log continuity generation
        self._log_event("continuity_generated", continuity)
        
        return continuity

# Example usage
if __name__ == "__main__":
    # Create the gas gauge
    print("🚀 Initializing TeamBadass Gas Gauge System...")
    gauge = ObservableGasGauge()
    
    # Register context loading
    print("\n📚 Registering initial context loading...")
    result = gauge.register_context_loading(100)  # 100KB of context
    print(f"Operation: {result['operation']}")
    print(f"Usage Increase: {result['usage_increase']}%")
    print(f"Current Status: {result['ascii_gauge']}")
    
    # Register code generation
    print("\n💻 Registering code generation (medium complexity, medium size)...")
    result = gauge.register_code_generation("medium", "medium")
    print(f"Operation: {result['operation']}")
    print(f"Usage Increase: {result['usage_increase']}%")
    print(f"Current Status: {result['ascii_gauge']}")
    
    # Perform pre-task assessment for a large coding task
    print("\n🔎 Performing pre-task assessment for a large coding task...")
    assessment = gauge.pre_task_assessment(
        "Implement Machine Learning Algorithm", 
        "code", 
        "high", 
        "large"
    )
    print(f"Task: {assessment['task_name']} ({assessment['complexity']} complexity, {assessment['size']} size)")
    print(f"Current Status: {assessment['current_status']}")
    print(f"Estimated Cost: {assessment['estimated_cost']}")
    print(f"Post-Task Status: {assessment['post_task_status']}")
    print("Decision Options:")
    for option in assessment["decision_options"]:
        print(f"- {option['option']} ({option['recommendation_level']}): {option['description']}")
    
    # Register discussion exchange
    print("\n💬 Registering discussion exchange (200 words)...")
    result = gauge.register_discussion_exchange(200)
    print(f"Operation: {result['operation']}")
    print(f"Usage Increase: {result['usage_increase']}%")
    print(f"Current Status: {result['ascii_gauge']}")
    
    # Check status
    print("\n🔍 Checking current status...")
    status = gauge.check_status()
    print(f"Session Duration: {status['session_duration_minutes']} minutes")
    print(f"Current Status: {status['ascii_gauge']}")
    print(f"Remaining Capacity: {status['remaining_capacity']}%")
    print("Recommendations:")
    for recommendation in status["recommendations"]:
        print(f"- {recommendation}")
    
    # Register long chats warning
    print("\n⚠️ Simulating appearance of 'long chats' warning...")
    result = gauge.register_long_chats_warning()
    print(f"Warning Registered at: {result['timestamp']}")
    print(f"Estimated Usage at Warning: {result['estimated_usage_at_warning']}%")
    print(f"New Warning Threshold: {result['new_threshold']}%")
    
    # Generate continuity
    print("\n📋 Generating continuity information...")
    continuity = gauge.generate_continuity()
    print(f"Session ID: {continuity['previous_session_id']}")
    print(f"Operations Completed: {continuity['operations_completed']}")
    print(f"Final Usage Estimate: {continuity['estimated_usage_percentage']}%")
    print("Adjusted Thresholds:")
    print(f"- Long Chats Warning: {continuity['threshold_adjustments']['long_chats_warning']}%")
    print(f"- Hard Stop: {continuity['threshold_adjustments']['hard_stop']}%")

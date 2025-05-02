#!/usr/bin/env python3
"""
FILE_OVERVIEW: consolidated_gas_gauge.py - Optimized gas measurement using observable indicators
VERSION: 2.0.0
LAST_UPDATED: 2025-05-02
DEPENDENCIES: None
IMPORTED_BY: init.py, metrics_collector.py, dashboard.tsx

TABLE_OF_CONTENTS:
1. ConsolidatedGasGauge Class - Core gas measurement implementation
2. Observable Indicators - Usage estimation based on actual behavior
3. Status Reporting - Usage visualization and recommendations
4. Checkpoint Verification - Progress validation against thresholds
5. Task Estimation - Capacity planning for operations
6. JSON Serialization - Persistence and metrics collection

SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
"""

import os
import json
import time
import logging
import re
from datetime import datetime
from typing import Dict, List, Union, Optional, Any, Tuple

class ConsolidatedGasGauge:
    """Optimized gas measurement system using observable indicators"""
    
    def __init__(self, metrics_dir: str = None):
        """Initialize the gas gauge with streamlined defaults"""
        # Core tracking attributes
        self.operations = {
            "context_loading": 0,
            "discussion_exchanges": 0,
            "code_generation": 0,
            "search_operations": 0,
            "artifact_creation": 0,
            "planning": 0
        }
        self.start_time = datetime.now()
        self.last_check_time = self.start_time
        self.estimated_usage = 0.0  # Percentage of session used
        
        # Thresholds (based on observed data)
        self.warning_threshold = 60.0  # "Long chats" warning appears here
        self.hard_stop_threshold = 90.0  # Session terminates here
        
        # Observable indicators
        self.long_chats_warning_observed = False
        self.long_chats_warning_time = None
        self.hard_stop_observed = False
        self.hard_stop_time = None
        
        # Checkpoints definition (mapped to gas levels)
        self.checkpoints = {
            "context_loaded": {"minimum_gas": 75, "description": "After loading project context"},
            "planning_complete": {"minimum_gas": 60, "description": "After project planning phase"},
            "implementation_start": {"minimum_gas": 50, "description": "Before starting implementation"},
            "continuity_generation": {"minimum_gas": 30, "description": "Before generating continuity"},
            "wrap_up": {"minimum_gas": 20, "description": "Project wrap-up and final tasks"}
        }
        
        # Cost reference table (percentage points)
        self.operation_costs = {
            "context_loading": {
                "base_cost": 2.0,
                "per_kb": 0.05
            },
            "code_generation": {
                "base_cost": 3.0,
                "complexity_factors": {"low": 1.0, "medium": 2.0, "high": 4.0},
                "size_factors": {"small": 1.0, "medium": 2.5, "large": 5.0}
            },
            "discussion_exchange": {
                "base_cost": 1.0,
                "per_word": 0.01
            },
            "search_operation": {
                "base_cost": 4.0,
                "per_result": 0.5
            },
            "artifact_creation": {
                "base_cost": 5.0,
                "complexity_factors": {"low": 1.0, "medium": 2.0, "high": 3.5},
                "size_factors": {"small": 1.0, "medium": 2.0, "large": 4.0}
            },
            "planning": {
                "base_cost": 2.0,
                "complexity_factors": {"low": 1.0, "medium": 2.0, "high": 3.0}
            }
        }
        
        # Setup metrics directory
        self.metrics_dir = metrics_dir or os.path.join("teambadass", "metrics")
        os.makedirs(self.metrics_dir, exist_ok=True)
        
        # Setup logging (minimal)
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger("ConsolidatedGasGauge")

    def register_context_loading(self, size_kb: float) -> Dict[str, Any]:
        """Register context loading with size in KB"""
        cost = self.operation_costs["context_loading"]["base_cost"] + (self.operation_costs["context_loading"]["per_kb"] * size_kb)
        
        self.estimated_usage += cost
        self.operations["context_loading"] += size_kb
        self.last_check_time = datetime.now()
        
        return {
            "operation": "Context Loading",
            "details": f"{size_kb}KB",
            "cost": cost,
            "cumulative": self.estimated_usage,
            "status": self._get_status()
        }

    def register_code_generation(self, complexity: str = "medium", size: str = "medium") -> Dict[str, Any]:
        """Register code generation with complexity and size"""
        complexity_factor = self.operation_costs["code_generation"]["complexity_factors"].get(complexity, 
                                                                                            self.operation_costs["code_generation"]["complexity_factors"]["medium"])
        size_factor = self.operation_costs["code_generation"]["size_factors"].get(size, 
                                                                                self.operation_costs["code_generation"]["size_factors"]["medium"])
        
        cost = self.operation_costs["code_generation"]["base_cost"] * complexity_factor * size_factor
        
        self.estimated_usage += cost
        self.operations["code_generation"] += 1
        self.last_check_time = datetime.now()
        
        return {
            "operation": "Code Generation",
            "details": f"{complexity} complexity, {size} size",
            "cost": cost,
            "cumulative": self.estimated_usage,
            "status": self._get_status()
        }

    def register_discussion_exchange(self, words: int = 100) -> Dict[str, Any]:
        """Register discussion exchange with word count"""
        cost = self.operation_costs["discussion_exchange"]["base_cost"] + (self.operation_costs["discussion_exchange"]["per_word"] * words)
        
        self.estimated_usage += cost
        self.operations["discussion_exchanges"] += 1
        self.last_check_time = datetime.now()
        
        return {
            "operation": "Discussion Exchange",
            "details": f"{words} words",
            "cost": cost,
            "cumulative": self.estimated_usage,
            "status": self._get_status()
        }

    def register_search_operation(self, results: int = 5) -> Dict[str, Any]:
        """Register search operation with results count"""
        cost = self.operation_costs["search_operation"]["base_cost"] + (self.operation_costs["search_operation"]["per_result"] * results)
        
        self.estimated_usage += cost
        self.operations["search_operations"] += 1
        self.last_check_time = datetime.now()
        
        return {
            "operation": "Search Operation",
            "details": f"{results} results",
            "cost": cost,
            "cumulative": self.estimated_usage,
            "status": self._get_status()
        }

    def register_artifact_creation(self, complexity: str = "medium", size: str = "medium") -> Dict[str, Any]:
        """Register artifact creation with complexity and size"""
        complexity_factor = self.operation_costs["artifact_creation"]["complexity_factors"].get(complexity, 
                                                                                              self.operation_costs["artifact_creation"]["complexity_factors"]["medium"])
        size_factor = self.operation_costs["artifact_creation"]["size_factors"].get(size, 
                                                                                  self.operation_costs["artifact_creation"]["size_factors"]["medium"])
        
        cost = self.operation_costs["artifact_creation"]["base_cost"] * complexity_factor * size_factor
        
        self.estimated_usage += cost
        self.operations["artifact_creation"] += 1
        self.last_check_time = datetime.now()
        
        return {
            "operation": "Artifact Creation",
            "details": f"{complexity} complexity, {size} size",
            "cost": cost,
            "cumulative": self.estimated_usage,
            "status": self._get_status()
        }

    def register_planning(self, complexity: str = "medium") -> Dict[str, Any]:
        """Register planning with complexity level"""
        complexity_factor = self.operation_costs["planning"]["complexity_factors"].get(complexity, 
                                                                                     self.operation_costs["planning"]["complexity_factors"]["medium"])
        
        cost = self.operation_costs["planning"]["base_cost"] * complexity_factor
        
        self.estimated_usage += cost
        self.operations["planning"] += 1
        self.last_check_time = datetime.now()
        
        return {
            "operation": "Planning",
            "details": f"{complexity} complexity",
            "cost": cost,
            "cumulative": self.estimated_usage,
            "status": self._get_status()
        }

    def _get_status(self) -> str:
        """Get status based on current estimated usage"""
        if self.estimated_usage >= self.hard_stop_threshold:
            return "CRITICAL"
        elif self.estimated_usage >= self.warning_threshold:
            return "WARNING"
        elif self.estimated_usage >= self.warning_threshold * 0.8:
            return "CAUTION"
        else:
            return "NORMAL"

    def register_long_chats_warning(self) -> Dict[str, Any]:
        """Register observation of 'long chats' warning"""
        self.long_chats_warning_observed = True
        self.long_chats_warning_time = datetime.now()
        
        # Adjust threshold based on observation (weighted average)
        if self.warning_threshold != self.estimated_usage:
            self.warning_threshold = (self.estimated_usage * 0.7) + (self.warning_threshold * 0.3)
            self.warning_threshold = round(self.warning_threshold, 1)
        
        return {
            "event": "Long Chats Warning",
            "usage_at_warning": self.estimated_usage,
            "timestamp": self.long_chats_warning_time.isoformat(),
            "updated_threshold": self.warning_threshold
        }

    def register_hard_stop(self) -> Dict[str, Any]:
        """Register observation of hard stop (session termination)"""
        self.hard_stop_observed = True
        self.hard_stop_time = datetime.now()
        
        # Adjust threshold based on observation (weighted average)
        if self.hard_stop_threshold != self.estimated_usage:
            self.hard_stop_threshold = (self.estimated_usage * 0.7) + (self.hard_stop_threshold * 0.3)
            self.hard_stop_threshold = round(self.hard_stop_threshold, 1)
        
        return {
            "event": "Hard Stop",
            "usage_at_stop": self.estimated_usage,
            "timestamp": self.hard_stop_time.isoformat(),
            "updated_threshold": self.hard_stop_threshold
        }

    def check_status(self) -> Dict[str, Any]:
        """Complete status check with recommendations"""
        self.last_check_time = datetime.now()
        session_duration = (self.last_check_time - self.start_time).total_seconds() / 60.0
        
        status = {
            "timestamp": self.last_check_time.isoformat(),
            "session_duration_minutes": round(session_duration, 1),
            "estimated_usage": round(self.estimated_usage, 1),
            "ascii_gauge": self._generate_ascii_gauge(),
            "operations": self.operations,
            "status": self._get_status(),
            "warning_threshold": self.warning_threshold,
            "hard_stop_threshold": self.hard_stop_threshold,
            "remaining_capacity": round(100 - self.estimated_usage, 1)
        }
        
        # Add recommendations based on status
        if status["status"] == "CRITICAL":
            status["recommendations"] = [
                "Emergency continuity generation required",
                "Hop immediately to avoid data loss",
                "Split any remaining work into a new session"
            ]
        elif status["status"] == "WARNING":
            status["recommendations"] = [
                "Prepare to wrap up current work",
                "Generate continuity documentation",
                "Plan for session hop"
            ]
        elif status["status"] == "CAUTION":
            status["recommendations"] = [
                "Approaching warning threshold",
                "Complete current high-priority tasks",
                "Avoid starting new complex operations"
            ]
        else:
            status["recommendations"] = [
                "Sufficient capacity for planned operations",
                "Continue with current work plan"
            ]
        
        return status

    def _generate_ascii_gauge(self, width: int = 20) -> str:
        """Generate ASCII gauge showing usage and thresholds"""
        # Calculate positions
        usage_width = int((self.estimated_usage / 100) * width)
        warning_pos = int((self.warning_threshold / 100) * width)
        hard_stop_pos = int((self.hard_stop_threshold / 100) * width)
        
        # Generate gauge
        gauge = "["
        for i in range(width):
            if i < usage_width:
                gauge += "="  # Filled portion
            elif i == warning_pos:
                gauge += "W"  # Warning marker
            elif i == hard_stop_pos:
                gauge += "H"  # Hard stop marker
            else:
                gauge += " "  # Empty portion
        gauge += f"] {round(self.estimated_usage, 1)}%"
        
        # Add status label
        gauge += f" - {self._get_status()}"
        
        return gauge

    def format_status_report(self) -> str:
        """Generate comprehensive status report with visualization"""
        status = self.check_status()
        
        # Create report
        report = []
        report.append("="*50)
        report.append("📊 GAS GAUGE STATUS REPORT")
        report.append("="*50)
        report.append("")
        
        # Add gauge
        report.append(f"Gas Level:\n{status['ascii_gauge']}")
        report.append("")
        
        # Add usage details
        report.append(f"Session Duration: {status['session_duration_minutes']} minutes")
        report.append(f"Estimated Usage: {status['estimated_usage']}%")
        report.append(f"Remaining Capacity: {status['remaining_capacity']}%")
        report.append(f"Warning Threshold: {self.warning_threshold}%")
        report.append(f"Hard Stop Threshold: {self.hard_stop_threshold}%")
        report.append("")
        
        # Add operations summary
        report.append("Operations Summary:")
        for op_type, count in self.operations.items():
            if count > 0:
                report.append(f"- {op_type}: {count}")
        report.append("")
        
        # Add observable indicators
        report.append("Observable Indicators:")
        if self.long_chats_warning_observed:
            warning_time = self.long_chats_warning_time.strftime("%H:%M:%S")
            report.append(f"- Long Chats Warning: Observed at {warning_time} ({round(self.estimated_usage, 1)}% usage)")
        else:
            report.append(f"- Long Chats Warning: Not observed")
            
        if self.hard_stop_observed:
            stop_time = self.hard_stop_time.strftime("%H:%M:%S")
            report.append(f"- Hard Stop: Observed at {stop_time} ({round(self.estimated_usage, 1)}% usage)")
        else:
            report.append(f"- Hard Stop: Not observed")
        report.append("")
        
        # Add recommendations
        report.append("Recommendations:")
        for rec in status["recommendations"]:
            report.append(f"- {rec}")
        
        report.append("="*50)
        
        return "\n".join(report)

    def display_current_gas(self) -> None:
        """Display current gas level to console"""
        print(self._generate_ascii_gauge())

    def check_checkpoint(self, name: str) -> Dict[str, Any]:
        """Verify if gas level meets checkpoint requirement"""
        checkpoint = self.checkpoints.get(name)
        if not checkpoint:
            return {"valid": False, "error": f"Unknown checkpoint: {name}"}
        
        remaining = 100 - self.estimated_usage
        minimum = checkpoint["minimum_gas"]
        meets_requirement = remaining >= minimum
        
        result = {
            "checkpoint": name,
            "description": checkpoint["description"],
            "minimum_gas": minimum,
            "current_remaining": remaining,
            "valid": meets_requirement,
            "status": "PASS" if meets_requirement else "FAIL",
            "margin": remaining - minimum if meets_requirement else minimum - remaining
        }
        
        # Log result
        status_str = "✅ PASS" if meets_requirement else "❌ FAIL"
        self.logger.info(f"{status_str} | Checkpoint '{name}': {remaining}% remaining, {minimum}% required")
        
        return result

    def estimate_task(self, task_type: str, complexity: str = "medium", size: str = "medium") -> Dict[str, Any]:
        """Estimate if task can be completed with remaining capacity"""
        # Map task type to operation
        type_mapping = {
            "code": "code_generation",
            "discussion": "discussion_exchange",
            "search": "search_operation",
            "artifact": "artifact_creation",
            "planning": "planning",
            "context": "context_loading"
        }
        
        operation = type_mapping.get(task_type)
        if not operation:
            return {
                "error": f"Unknown task type: {task_type}",
                "valid_types": list(type_mapping.keys())
            }
        
        # Calculate cost based on operation type
        cost = 0
        details = {}
        
        if operation == "code_generation":
            complexity_factor = self.operation_costs["code_generation"]["complexity_factors"].get(
                complexity, self.operation_costs["code_generation"]["complexity_factors"]["medium"])
            size_factor = self.operation_costs["code_generation"]["size_factors"].get(
                size, self.operation_costs["code_generation"]["size_factors"]["medium"])
            cost = self.operation_costs["code_generation"]["base_cost"] * complexity_factor * size_factor
            details = {"complexity_factor": complexity_factor, "size_factor": size_factor}
            
        elif operation == "discussion_exchange":
            # Map size to word count
            word_counts = {"small": 50, "medium": 200, "large": 500}
            words = word_counts.get(size, word_counts["medium"])
            cost = self.operation_costs["discussion_exchange"]["base_cost"] + (self.operation_costs["discussion_exchange"]["per_word"] * words)
            details = {"words": words}
            
        elif operation == "search_operation":
            # Map complexity to result count
            result_counts = {"low": 3, "medium": 5, "high": 10}
            results = result_counts.get(complexity, result_counts["medium"])
            cost = self.operation_costs["search_operation"]["base_cost"] + (self.operation_costs["search_operation"]["per_result"] * results)
            details = {"results": results}
            
        elif operation == "artifact_creation":
            complexity_factor = self.operation_costs["artifact_creation"]["complexity_factors"].get(
                complexity, self.operation_costs["artifact_creation"]["complexity_factors"]["medium"])
            size_factor = self.operation_costs["artifact_creation"]["size_factors"].get(
                size, self.operation_costs["artifact_creation"]["size_factors"]["medium"])
            cost = self.operation_costs["artifact_creation"]["base_cost"] * complexity_factor * size_factor
            details = {"complexity_factor": complexity_factor, "size_factor": size_factor}
            
        elif operation == "planning":
            complexity_factor = self.operation_costs["planning"]["complexity_factors"].get(
                complexity, self.operation_costs["planning"]["complexity_factors"]["medium"])
            cost = self.operation_costs["planning"]["base_cost"] * complexity_factor
            details = {"complexity_factor": complexity_factor}
            
        elif operation == "context_loading":
            # Map size to KB
            kb_sizes = {"small": 10, "medium": 50, "large": 200}
            kb = kb_sizes.get(size, kb_sizes["medium"])
            cost = self.operation_costs["context_loading"]["base_cost"] + (self.operation_costs["context_loading"]["per_kb"] * kb)
            details = {"size_kb": kb}
        
        # Check if we have enough capacity
        remaining = 100 - self.estimated_usage
        has_capacity = remaining >= cost
        will_exceed_warning = (self.estimated_usage + cost) >= self.warning_threshold
        will_exceed_hard_stop = (self.estimated_usage + cost) >= self.hard_stop_threshold
        
        # Generate result
        result = {
            "task_type": task_type,
            "complexity": complexity,
            "size": size,
            "cost": round(cost, 1),
            "current_usage": round(self.estimated_usage, 1),
            "remaining": round(remaining, 1),
            "has_capacity": has_capacity,
            "will_exceed_warning": will_exceed_warning,
            "will_exceed_hard_stop": will_exceed_hard_stop,
            "details": details
        }
        
        # Add recommendation
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

    def pre_task_assessment(self, task_name: str, task_type: str, complexity: str = "medium", size: str = "medium") -> Dict[str, Any]:
        """Comprehensive pre-task assessment with decision support"""
        # Check status first
        status = self.check_status()
        
        # Estimate task
        estimate = self.estimate_task(task_type, complexity, size)
        if "error" in estimate:
            return estimate
        
        # Calculate post-task usage
        post_task_usage = self.estimated_usage + estimate["cost"]
        
        # Generate decision options
        options = []
        
        if estimate["will_exceed_hard_stop"]:
            options.append({
                "option": "Hop Session",
                "recommendation": "Strong",
                "description": "Start a new session before attempting this task",
                "impact": f"Preserves continuity, avoids data loss"
            })
            options.append({
                "option": "Break Into Chunks",
                "recommendation": "Alternative",
                "description": f"Split into smaller {size} chunks of {complexity} complexity",
                "impact": f"Allows partial progress, but increases overhead"
            })
        elif estimate["will_exceed_warning"]:
            options.append({
                "option": "Proceed & Hop",
                "recommendation": "Strong",
                "description": "Complete task then immediately hop to new session",
                "impact": f"Maximizes current session, but risks interruption"
            })
            options.append({
                "option": "Break Into Chunks",
                "recommendation": "Alternative",
                "description": f"Split into smaller {size} chunks of {complexity} complexity",
                "impact": f"More predictable, but increases overhead"
            })
        elif post_task_usage > self.warning_threshold * 0.8:
            options.append({
                "option": "Proceed With Caution",
                "recommendation": "Standard",
                "description": "Complete task but prepare for potential hop afterwards",
                "impact": f"Balanced approach with moderate risk"
            })
            options.append({
                "option": "Optimize First",
                "recommendation": "Alternative",
                "description": f"Reduce scope or complexity before proceeding",
                "impact": f"Slower but safer approach"
            })
        else:
            options.append({
                "option": "Proceed As Planned",
                "recommendation": "Standard",
                "description": "Sufficient capacity for this task and more",
                "impact": f"No special measures needed"
            })
        
        # Create comprehensive assessment
        assessment = {
            "task_name": task_name,
            "task_type": task_type,
            "complexity": complexity,
            "size": size,
            "current_usage": round(self.estimated_usage, 1),
            "estimated_cost": round(estimate["cost"], 1),
            "post_task_usage": round(post_task_usage, 1),
            "remaining_after": round(100 - post_task_usage, 1),
            "status": estimate["status"],
            "decision_options": options,
            "ascii_gauge_current": self._generate_ascii_gauge(),
            "ascii_gauge_post_task": self._generate_post_task_gauge(estimate["cost"])
        }
        
        return assessment

    def _generate_post_task_gauge(self, cost: float) -> str:
        """Generate ASCII gauge showing post-task status"""
        post_usage = self.estimated_usage + cost
        
        # Calculate positions for width=20
        width = 20
        usage_width = int((post_usage / 100) * width)
        warning_pos = int((self.warning_threshold / 100) * width)
        hard_stop_pos = int((self.hard_stop_threshold / 100) * width)
        
        # Generate gauge
        gauge = "["
        for i in range(width):
            if i < usage_width:
                gauge += "="  # Filled portion
            elif i == warning_pos:
                gauge += "W"  # Warning marker
            elif i == hard_stop_pos:
                gauge += "H"  # Hard stop marker
            else:
                gauge += " "  # Empty portion
        gauge += f"] {round(post_usage, 1)}%"
        
        # Add status
        if post_usage >= self.hard_stop_threshold:
            status = "CRITICAL"
        elif post_usage >= self.warning_threshold:
            status = "WARNING"
        elif post_usage >= self.warning_threshold * 0.8:
            status = "CAUTION"
        else:
            status = "NORMAL"
        
        gauge += f" - {status}"
        
        return gauge

    def save_metrics(self, filename: str = None) -> str:
        """Save current metrics to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
            filename = f"gas-metrics-{timestamp}.json"
        
        # Create full path
        filepath = os.path.join(self.metrics_dir, filename)
        
        # Prepare data structure
        metrics = {
            "version": "2.0.0",
            "session_id": f"{datetime.now().strftime('%Y-%m-%d')}-gas-metrics",
            "timestamp": datetime.now().isoformat(),
            "operations": [self._format_operation_record(op_type, count) for op_type, count in self.operations.items() if count > 0],
            "operations_by_type": {
                op_type: {
                    "count": count if isinstance(count, int) else 1, 
                    "total_usage": self._calculate_operation_usage(op_type, count)
                } 
                for op_type, count in self.operations.items()
            },
            "thresholds": {
                "warning": self.warning_threshold,
                "hard_stop": self.hard_stop_threshold
            },
            "final_status": {
                "usage": round(self.estimated_usage, 1),
                "status": self._get_status(),
                "remaining": round(100 - self.estimated_usage, 1),
                "usage_percentage_of_warning": round((self.estimated_usage / self.warning_threshold) * 100, 1),
                "timestamp": datetime.now().isoformat()
            },
            "warnings_observed": {
                "long_chats_warning": {
                    "occurred": self.long_chats_warning_observed,
                    "timestamp": self.long_chats_warning_time.isoformat() if self.long_chats_warning_time else None,
                    "usage_at_warning": round(self.estimated_usage, 1) if self.long_chats_warning_observed else None
                },
                "hard_stop": {
                    "occurred": self.hard_stop_observed,
                    "timestamp": self.hard_stop_time.isoformat() if self.hard_stop_time else None,
                    "usage_at_stop": round(self.estimated_usage, 1) if self.hard_stop_observed else None
                }
            }
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        return filepath

    def _format_operation_record(self, op_type: str, count) -> Dict[str, Any]:
        """Format operation record for metrics"""
        # Special handling for context loading which stores KB not count
        if op_type == "context_loading":
            return {
                "type": op_type,
                "details": f"Repository files ({count}KB)",
                "usage": self._calculate_operation_usage(op_type, count),
                "cumulative": round(self.estimated_usage, 1),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "type": op_type,
                "details": f"{count} operations",
                "usage": self._calculate_operation_usage(op_type, count),
                "cumulative": round(self.estimated_usage, 1),
                "timestamp": datetime.now().isoformat()
            }

    def _calculate_operation_usage(self, op_type: str, count) -> float:
        """Calculate usage for an operation type"""
        # This is an approximation since we don't track individual operation details
        if op_type == "context_loading":
            # For context loading, count is KB
            return round(self.operation_costs["context_loading"]["base_cost"] + 
                        (self.operation_costs["context_loading"]["per_kb"] * count), 1)
        
        elif op_type == "code_generation":
            # Assume medium complexity and size for simplicity
            return round(count * self.operation_costs["code_generation"]["base_cost"] * 
                        self.operation_costs["code_generation"]["complexity_factors"]["medium"] * 
                        self.operation_costs["code_generation"]["size_factors"]["medium"], 1)
        
        elif op_type == "discussion_exchanges":
            # Assume 100 words per exchange for simplicity
            return round(count * (self.operation_costs["discussion_exchange"]["base_cost"] + 
                                 (self.operation_costs["discussion_exchange"]["per_word"] * 100)), 1)
        
        elif op_type == "search_operations":
            # Assume 5 results per search for simplicity
            return round(count * (self.operation_costs["search_operation"]["base_cost"] + 
                                 (self.operation_costs["search_operation"]["per_result"] * 5)), 1)
        
        elif op_type == "artifact_creation":
            # Assume medium complexity and size for simplicity
            return round(count * self.operation_costs["artifact_creation"]["base_cost"] * 
                        self.operation_costs["artifact_creation"]["complexity_factors"]["medium"] * 
                        self.operation_costs["artifact_creation"]["size_factors"]["medium"], 1)
        
        elif op_type == "planning":
            # Assume medium complexity for simplicity
            return round(count * self.operation_costs["planning"]["base_cost"] * 
                        self.operation_costs["planning"]["complexity_factors"]["medium"], 1)
        
        return 0.0

    def to_json(self) -> str:
        """Convert gas gauge to JSON string"""
        data = {
            "estimated_usage": round(self.estimated_usage, 1),
            "status": self._get_status(),
            "warning_threshold": self.warning_threshold,
            "hard_stop_threshold": self.hard_stop_threshold,
            "operations": self.operations,
            "long_chats_warning_observed": self.long_chats_warning_observed,
            "hard_stop_observed": self.hard_stop_observed,
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(data, indent=2)

    def from_json(self, json_str: str) -> 'ConsolidatedGasGauge':
        """Load gas gauge from JSON string"""
        data = json.loads(json_str)
        self.estimated_usage = data.get("estimated_usage", 0.0)
        self.warning_threshold = data.get("warning_threshold", 60.0)
        self.hard_stop_threshold = data.get("hard_stop_threshold", 90.0)
        self.operations = data.get("operations", self.operations)
        self.long_chats_warning_observed = data.get("long_chats_warning_observed", False)
        self.hard_stop_observed = data.get("hard_stop_observed", False)
        return self

    def load_previous_metrics(self, filename: str) -> Dict[str, Any]:
        """Load previous metrics from file"""
        filepath = os.path.join(self.metrics_dir, filename)
        if not os.path.exists(filepath):
            return {"error": f"File not found: {filepath}"}
        
        with open(filepath, 'r') as f:
            return json.load(f)


# Example usage - simple test
if __name__ == "__main__":
    # Create gas gauge
    gauge = ConsolidatedGasGauge()
    
    # Register context loading
    print("\n🔍 Registering initial context loading...")
    result = gauge.register_context_loading(80) # 80KB
    print(f"Operation: {result['operation']}")
    print(f"Usage: {result['cost']}%")
    print(f"Status: {result['status']}")
    
    # Check status
    print("\n📊 Current gas status:")
    gauge.display_current_gas()
    
    # Run pre-task assessment for a medium code task
    print("\n🧩 Pre-task assessment for code generation:")
    assessment = gauge.pre_task_assessment("Implement Dashboard", "code", "medium", "medium")
    print(f"Task: {assessment['task_name']}")
    print(f"Current usage: {assessment['current_usage']}%")
    print(f"Estimated cost: {assessment['estimated_cost']}%")
    print(f"Post-task usage: {assessment['post_task_usage']}%")
    print(f"Status: {assessment['status']}")
    print("Decision options:")
    for option in assessment['decision_options']:
        print(f"- {option['option']} ({option['recommendation']}): {option['description']}")
    
    # Generate status report
    print("\n📜 Full status report:")
    print(gauge.format_status_report())
    
    # Save metrics
    metrics_file = gauge.save_metrics()
    print(f"\n💾 Metrics saved to: {metrics_file}")

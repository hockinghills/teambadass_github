#!/usr/bin/env python3
"""
FILE_OVERVIEW: mobile_integration.py - TeamBadass Mobile Session Handler
VERSION: 1.0.0
LAST_UPDATED: 2025-05-01
DEPENDENCIES: auto_init.py
IMPORTED_BY: session_start.py

TABLE_OF_CONTENTS:
1. Mobile Detection - Methods to detect mobile environment
2. Session Optimization - Streamlined session handling for mobile
3. Command Processing - Shorthand command processing for mobile

SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
"""

import os
import sys
import re
import json
import logging
from datetime import datetime

# Import auto initialization system
from auto_init import AutoInit

# Configure minimal logging for mobile
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Simplified format for mobile
)
logger = logging.getLogger("TeamBadass")

class MobileSession:
    """TeamBadass mobile session handler with optimizations"""
    
    def __init__(self):
        """Initialize mobile session handler"""
        self.is_mobile = self._detect_mobile()
        self.auto_init = AutoInit(mobile_optimized=self.is_mobile)
        self.initialized = False
        self.gas_gauge = None
        self.commands = {
            "/g": self._cmd_check_gas,
            "/i": self._cmd_initialize,
            "/s": self._cmd_status,
            "/p": self._cmd_pre_task,
            "/h": self._cmd_help
        }
    
    def _detect_mobile(self):
        """
        Detect if session is running on a mobile device
        
        This is a simplified detection that can be enhanced based on your needs.
        
        Returns:
            bool: True if likely on mobile, False otherwise
        """
        # Check for mobile flag in command line args
        if "--mobile" in sys.argv:
            return True
        
        # Check for environment variable
        if os.environ.get("TEAMBADASS_MOBILE") == "1":
            return True
        
        # Default to desktop mode
        return False
    
    def initialize(self, context_files=None):
        """
        Initialize TeamBadass session for mobile use
        
        Args:
            context_files (list): List of file paths from context
            
        Returns:
            dict: Initialization status
        """
        # Detect repository
        repo_detected = self.auto_init.detect_repository(context_files)
        
        if not repo_detected:
            return {
                "status": "error",
                "message": "TeamBadass repository not detected. Please share the repository."
            }
        
        # Initialize gas gauge with minimal output
        gas_result = self.auto_init.initialize_gas_gauge()
        if gas_result["status"] == "success":
            self.gas_gauge = gas_result["gauge"]
        
        # Load minimal memory files
        memory_result = self.auto_init.load_memory(min_files=True)
        
        # Mark as initialized
        self.initialized = (
            repo_detected and 
            gas_result["status"] == "success" and 
            memory_result["status"] == "success"
        )
        
        # Generate very minimal report for mobile
        if self.is_mobile:
            status_message = "🚀 TeamBadass Mobile Ready"
            if gas_result["status"] == "success":
                status_message += f" | 🔋 {gas_result['gas_level']}%"
        else:
            status_message = self.auto_init.get_initialization_report()
        
        return {
            "status": "success" if self.initialized else "partial",
            "message": status_message,
            "gas_level": gas_result.get("gas_level") if gas_result["status"] == "success" else None,
            "initialized": self.initialized
        }
    
    def process_command(self, text):
        """
        Process potential shorthand commands in user input
        
        Args:
            text (str): User input text
            
        Returns:
            tuple: (was_command, result)
                was_command (bool): True if text was a command, False otherwise
                result (str): Command result or None if not a command
        """
        if not text or not text.startswith("/"):
            return False, None
        
        # Extract command and arguments
        parts = text.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Check if command exists
        if command in self.commands:
            # Execute command
            result = self.commands[command](args)
            return True, result
        
        return False, None
    
    def _cmd_check_gas(self, args):
        """Check gas level command"""
        if not self.initialized or not self.gas_gauge:
            return "⚠️ Gas gauge not initialized. Run /i first."
        
        # Check gas level
        gas_info = self.gas_gauge.check_gas()
        
        # Format minimal output for mobile
        if self.is_mobile:
            return f"🔋 Gas: {gas_info['level']}% - {gas_info['status']}"
        else:
            return f"Gas Level: {gas_info['gauge']} - {gas_info['status']}"
    
    def _cmd_initialize(self, args):
        """Initialize or reinitialize command"""
        result = self.initialize()
        return result["message"]
    
    def _cmd_status(self, args):
        """Show full status command"""
        if not self.initialized or not self.gas_gauge:
            return "⚠️ TeamBadass not initialized. Run /i first."
        
        # Get current status
        try:
            from teambadass._memory.gas_gauge.gauge_reporting import ClaudeGasGauge
            status = self.gas_gauge.format_status_report()
            
            # For mobile, create a more compact version
            if self.is_mobile:
                # Extract key information
                level = self.gas_gauge.current_level
                buffer_status = self.gas_gauge.check_buffers()
                
                # Create compact report
                report = []
                report.append(f"🔋 Gas: {level}% - {buffer_status['status']}")
                report.append(f"⚠️ Warning at: {self.gas_gauge.resource_map['thresholds']['long_chats_warning']}%")
                report.append(f"⛔ Hard Stop at: {self.gas_gauge.resource_map['thresholds']['hard_stop']}%")
                report.append(f"💪 Available: {buffer_status['available_for_work']}%")
                
                return "\n".join(report)
            else:
                return status
        except Exception as e:
            # Fallback to basic status
            return self._cmd_check_gas(args)
    
    def _cmd_pre_task(self, args):
        """Perform pre-task assessment command"""
        if not self.initialized or not self.gas_gauge:
            return "⚠️ TeamBadass not initialized. Run /i first."
        
        # Parse arguments
        args_pattern = r"(\w+)\s+(\w+)\s+(\w+)"
        match = re.match(args_pattern, args)
        
        if not match:
            return "Usage: /p task_type complexity size\nExample: /p code medium large"
        
        task_type, complexity, size = match.groups()
        
        # Perform assessment
        try:
            assessment = self.gas_gauge.pre_task_assessment(
                f"User requested {task_type}", task_type, complexity, size
            )
            
            # For mobile, create a more compact version
            if self.is_mobile:
                report = []
                report.append(f"🔍 Task: {task_type} ({complexity}/{size})")
                report.append(f"💰 Cost: {assessment['estimated_cost']}")
                report.append(f"🔄 After: {assessment['post_task_remaining']}")
                
                # Add primary recommendation
                primary_option = assessment['decision_options'][0]
                report.append(f"👉 {primary_option['option']}: {primary_option['description']}")
                
                return "\n".join(report)
            else:
                return f"Pre-Task Assessment:\n{assessment}"
        except Exception as e:
            return f"Error performing assessment: {e}"
    
    def _cmd_help(self, args):
        """Show help command"""
        help_text = [
            "📱 TeamBadass Mobile Commands:",
            "/g - Check gas level",
            "/i - Initialize or reinitialize",
            "/s - Show detailed status",
            "/p [task] [complexity] [size] - Pre-task assessment",
            "/h - Show this help"
        ]
        return "\n".join(help_text)

# Main execution - this can be used for testing
if __name__ == "__main__":
    # Create mobile session handler
    session = MobileSession()
    
    # Initialize
    print("🚀 Initializing TeamBadass Mobile...")
    init_result = session.initialize()
    print(init_result["message"])
    
    # Test command processing
    test_commands = ["/g", "/s", "/p code medium large", "/h"]
    for cmd in test_commands:
        print(f"\nTesting command: {cmd}")
        was_cmd, result = session.process_command(cmd)
        if was_cmd:
            print(result)
        else:
            print("Not a command")

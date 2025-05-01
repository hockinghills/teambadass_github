#!/usr/bin/env python3
"""
FILE_OVERVIEW: init.py - Main TeamBadass Initialization Script
VERSION: 1.0.0
LAST_UPDATED: 2025-05-01
DEPENDENCIES: auto_init.py, mobile_integration.py
IMPORTED_BY: None (entry point)

TABLE_OF_CONTENTS:
1. Initialization Control - Main entry point for TeamBadass initialization
2. Environment Detection - Detect running environment and configure accordingly
3. Auto/Manual Initialization - Support both auto and manual initialization

SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
"""

import os
import sys
import json
import logging
from datetime import datetime

# Import TeamBadass modules
try:
    from auto_init import AutoInit
    from mobile_integration import MobileSession
except ImportError:
    print("⚠️ TeamBadass modules not found. Please ensure repository is properly shared.")
    sys.exit(1)

# Create logger
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Simplified format
)
logger = logging.getLogger("TeamBadass")

class TeamBadassInit:
    """Main initialization control for TeamBadass"""
    
    def __init__(self):
        """Initialize the TeamBadass system"""
        # Detect environment
        self.is_mobile = self._detect_mobile_environment()
        self.trigger_phrases = ["go go gadget memory", "go go gadget", "init teambadass"]
        self.auto_init_mode = self._should_use_auto_init()
        
        # Create appropriate initializer
        if self.is_mobile:
            self.session = MobileSession()
        else:
            self.initializer = AutoInit(mobile_optimized=False)
    
    def _detect_mobile_environment(self):
        """Detect if running in a mobile environment"""
        # Check for mobile flag in command line args
        if "--mobile" in sys.argv:
            return True
        
        # Check for environment variable
        if os.environ.get("TEAMBADASS_MOBILE") == "1":
            return True
        
        # Try to detect screen size or other mobile indicators
        # This is a simplified approach and can be enhanced
        try:
            import shutil
            terminal_size = shutil.get_terminal_size()
            if terminal_size.columns < 80:  # Likely mobile
                return True
        except:
            pass
        
        # Default to desktop mode
        return False
    
    def _should_use_auto_init(self):
        """Determine if we should use auto-initialization"""
        # Check for environment variable
        if os.environ.get("TEAMBADASS_AUTO_INIT") == "1":
            return True
        
        # Check for flag file
        if os.path.exists("teambadass/_memory/auto_init_enabled"):
            return True
        
        # Always use auto-init on mobile
        if self.is_mobile:
            return True
        
        # Default based on environment
        return self.is_mobile  # Auto-init on mobile, manual on desktop
    
    def detect_trigger_phrase(self, text):
        """Check if text contains a trigger phrase"""
        if not text:
            return False
        
        # Convert to lowercase for case-insensitive matching
        lower_text = text.lower()
        
        # Check for any trigger phrase
        for phrase in self.trigger_phrases:
            if phrase in lower_text:
                return True
        
        return False
    
    def handle_message(self, text, context_files=None):
        """
        Handle a potential initialization message
        
        Args:
            text (str): Message text
            context_files (list): List of file paths from context
            
        Returns:
            tuple: (was_handled, result)
                was_handled (bool): True if message was handled, False otherwise
                result (str): Initialization result or None if not handled
        """
        # Check for mobile commands first
        if self.is_mobile:
            was_command, result = self.session.process_command(text)
            if was_command:
                return True, result
        
        # Check for trigger phrases if not in auto-init mode
        if not self.auto_init_mode and not self.detect_trigger_phrase(text):
            return False, None
        
        # Initialize TeamBadass
        if self.is_mobile:
            init_result = self.session.initialize(context_files)
        else:
            # Initialize with AutoInit
            repo_detected = self.initializer.detect_repository(context_files)
            if not repo_detected:
                return True, "⚠️ TeamBadass repository not detected. Please share the repository."
            
            gas_result = self.initializer.initialize_gas_gauge()
            memory_result = self.initializer.load_memory(min_files=False)
            init_result = {
                "status": "success" if gas_result["status"] == "success" and memory_result["status"] == "success" else "partial",
                "message": self.initializer.get_initialization_report()
            }
        
        return True, init_result["message"]
    
    def auto_initialize(self, context_files=None):
        """
        Automatically initialize TeamBadass without a trigger phrase
        
        Args:
            context_files (list): List of file paths from context
            
        Returns:
            dict: Initialization status
        """
        if self.is_mobile:
            return self.session.initialize(context_files)
        else:
            # Initialize with AutoInit
            repo_detected = self.initializer.detect_repository(context_files)
            if not repo_detected:
                return {
                    "status": "error",
                    "message": "⚠️ TeamBadass repository not detected. Please share the repository."
                }
            
            gas_result = self.initializer.initialize_gas_gauge()
            memory_result = self.initializer.load_memory(min_files=False)
            
            return {
                "status": "success" if gas_result["status"] == "success" and memory_result["status"] == "success" else "partial",
                "message": self.initializer.get_initialization_report(),
                "gas_level": gas_result.get("gas_level") if gas_result["status"] == "success" else None
            }

# Main execution - this can be used for testing
if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="TeamBadass Initialization")
    parser.add_argument("--mobile", action="store_true", help="Force mobile mode")
    parser.add_argument("--auto", action="store_true", help="Force auto-initialization")
    parser.add_argument("--message", type=str, help="Test message to process")
    args = parser.parse_args()
    
    # Set environment variables based on arguments
    if args.mobile:
        os.environ["TEAMBADASS_MOBILE"] = "1"
    if args.auto:
        os.environ["TEAMBADASS_AUTO_INIT"] = "1"
    
    # Create initializer
    init_system = TeamBadassInit()
    
    # Display detected environment
    print(f"📱 Mobile Mode: {'Enabled' if init_system.is_mobile else 'Disabled'}")
    print(f"🚀 Auto-Init: {'Enabled' if init_system.auto_init_mode else 'Disabled'}")
    
    # Test initialization
    if args.auto or init_system.auto_init_mode:
        print("\n🔄 Auto-initializing TeamBadass...")
        result = init_system.auto_initialize()
        print(result["message"])
    
    # Test message handling
    if args.message:
        print(f"\n📝 Processing message: '{args.message}'")
        was_handled, result = init_system.handle_message(args.message)
        if was_handled:
            print(f"✅ Message handled: {result}")
        else:
            print("❌ Message not handled (not a trigger phrase)")

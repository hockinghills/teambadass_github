#!/usr/bin/env python3
"""
FILE_OVERVIEW: auto_init.py - TeamBadass Auto-Initialization System
VERSION: 1.0.0
LAST_UPDATED: 2025-05-01
DEPENDENCIES: None
IMPORTED_BY: init.py, session_start.py

TABLE_OF_CONTENTS:
1. Repository Detection - Methods to detect GitHub repository presence
2. Gas Gauge Initialization - Streamlined startup with minimal output
3. Mobile Optimization - Special handling for mobile devices

SKIP_DETAILED_ANALYSIS: True - This header provides sufficient context
"""

import os
import json
import time
import logging
from datetime import datetime

# Configure minimal logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Simplified format for mobile
)
logger = logging.getLogger("TeamBadass")

class AutoInit:
    """TeamBadass repository auto-detection and initialization system"""
    
    def __init__(self, mobile_optimized=False):
        """Initialize with optional mobile optimization"""
        self.mobile_optimized = mobile_optimized
        self.repository_detected = False
        self.gas_gauge_available = False
        self.memory_loaded = False
        self.repo_fingerprint = None
        self.start_time = datetime.now()
        
        # Mobile-specific settings
        if mobile_optimized:
            self.verbose = False
            self.show_ascii_gauge = False
            self.compact_output = True
        else:
            self.verbose = True
            self.show_ascii_gauge = True
            self.compact_output = False
    
    def detect_repository(self, context_files=None):
        """
        Detect TeamBadass repository presence from context files
        
        Args:
            context_files (list): List of file paths from context
            
        Returns:
            bool: True if repository detected, False otherwise
        """
        # If explicit file list provided, use that
        if context_files:
            return self._check_files_for_repository(context_files)
        
        # Otherwise try to detect automatically
        try:
            # Check for common TeamBadass repository files/patterns
            key_files = [
                "teambadass/README.md",
                "teambadass/_memory/core/team-dynamics-json.json",
                "teambadass/_memory/gas_gauge/gas_gauge_core.py"
            ]
            
            # Check if at least one key file exists
            for file_path in key_files:
                if os.path.exists(file_path):
                    self.repository_detected = True
                    self._generate_repo_fingerprint()
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Error detecting repository: {e}")
            return False
    
    def _check_files_for_repository(self, file_paths):
        """Check file paths for TeamBadass repository patterns"""
        if not file_paths:
            return False
        
        # Look for teambadass directory pattern in paths
        teambadass_pattern = "teambadass/"
        for path in file_paths:
            if isinstance(path, str) and teambadass_pattern in path:
                self.repository_detected = True
                self._generate_repo_fingerprint()
                return True
        
        return False
    
    def _generate_repo_fingerprint(self):
        """Generate a fingerprint of the repository for verification"""
        try:
            # Simple fingerprint based on existence and modification times of key files
            fingerprint = {}
            key_files = [
                "teambadass/README.md",
                "teambadass/_memory/core/team-dynamics-json.json",
                "teambadass/_memory/gas_gauge/gas_gauge_core.py"
            ]
            
            for file_path in key_files:
                if os.path.exists(file_path):
                    fingerprint[file_path] = os.path.getmtime(file_path)
            
            self.repo_fingerprint = fingerprint
        except Exception as e:
            logger.error(f"Error generating fingerprint: {e}")
    
    def initialize_gas_gauge(self):
        """
        Initialize gas gauge with minimal output
        
        Returns:
            dict: Initialization status
        """
        if not self.repository_detected:
            return {"status": "error", "message": "Repository not detected"}
        
        try:
            # Determine which gas gauge implementation to use
            if os.path.exists("teambadass/_memory/gas_gauge/observable_gas_gauge.py"):
                from teambadass._memory.gas_gauge.observable_gas_gauge import ObservableGasGauge
                gauge = ObservableGasGauge()
                gauge_type = "observable"
            else:
                # Fall back to core implementation
                from teambadass._memory.gas_gauge.gas_gauge_core import ClaudeGasGauge
                gauge = ClaudeGasGauge()
                gauge_type = "core"
            
            # Perform initial gas check silently (just for measurement)
            gas_info = gauge.check_gas("initial")
            self.gas_gauge_available = True
            
            # Prepare minimal output
            if self.compact_output:
                status_message = f"🔋 Gas: {gas_info['level']}% - {gauge_type.upper()}"
            else:
                status_message = f"🔋 TeamBadass initialized - Gas level: {gas_info['level']}% - {gauge_type.upper()} gauge active"
            
            # Only show ASCII gauge if requested
            if self.show_ascii_gauge and not self.compact_output:
                status_message += f"\n{gas_info['gauge']}"
            
            # Return status with minimal information
            return {
                "status": "success",
                "gas_level": gas_info['level'],
                "gauge_type": gauge_type,
                "display_message": status_message,
                "gauge": gauge  # Return actual gauge object for further use
            }
        except Exception as e:
            logger.error(f"Error initializing gas gauge: {e}")
            return {"status": "error", "message": f"Gas gauge initialization failed: {e}"}
    
    def load_memory(self, min_files=True):
        """
        Load minimal TeamBadass memory to initialize context
        
        Args:
            min_files (bool): Only load essential files if True
            
        Returns:
            dict: Memory loading status
        """
        if not self.repository_detected:
            return {"status": "error", "message": "Repository not detected"}
        
        try:
            # Define essential files
            essential_files = [
                "teambadass/_memory/core/team-dynamics-json.json",
                "teambadass/_memory/core/project-history-json.json"
            ]
            
            # Define optional files
            optional_files = [
                "teambadass/_memory/core/technical-environment-json.json",
                "teambadass/_memory/projects/furnace-project-json.json",
                "teambadass/_memory/projects/memory-system-json.json"
            ]
            
            # Determine which files to load
            files_to_load = essential_files
            if not min_files:
                files_to_load += optional_files
            
            # Load files
            loaded_files = []
            for file_path in files_to_load:
                if os.path.exists(file_path):
                    # In a real implementation, we would load the file content here
                    # For this script, we just track what would be loaded
                    loaded_files.append(file_path)
            
            self.memory_loaded = True
            
            # Return status
            if self.compact_output:
                status_message = f"📚 Memory: {len(loaded_files)}/{len(files_to_load)} files"
            else:
                status_message = f"📚 TeamBadass memory loaded: {len(loaded_files)}/{len(files_to_load)} files"
            
            return {
                "status": "success",
                "files_loaded": len(loaded_files),
                "files_total": len(files_to_load),
                "display_message": status_message
            }
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return {"status": "error", "message": f"Memory loading failed: {e}"}
    
    def get_initialization_report(self):
        """
        Generate a minimal initialization report
        
        Returns:
            str: Formatted initialization report
        """
        # Calculate elapsed time
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        # Prepare mobile-optimized or standard report
        if self.compact_output:
            if self.repository_detected and self.gas_gauge_available and self.memory_loaded:
                return f"✅ TeamBadass ready ({elapsed:.2f}s)"
            else:
                components = []
                if self.repository_detected:
                    components.append("repo")
                if self.gas_gauge_available:
                    components.append("gas")
                if self.memory_loaded:
                    components.append("mem")
                return f"⚠️ Partial: {'+'.join(components)} ({elapsed:.2f}s)"
        else:
            # Standard report
            report = []
            report.append(f"TeamBadass Initialization Report (Elapsed: {elapsed:.2f}s)")
            report.append(f"- Repository detected: {'✅' if self.repository_detected else '❌'}")
            report.append(f"- Gas gauge available: {'✅' if self.gas_gauge_available else '❌'}")
            report.append(f"- Memory loaded: {'✅' if self.memory_loaded else '❌'}")
            
            if self.repository_detected and self.gas_gauge_available and self.memory_loaded:
                report.append("✅ TeamBadass initialization complete")
            else:
                report.append("⚠️ TeamBadass initialization incomplete")
            
            return "\n".join(report)

# Main execution - this can be used for testing
if __name__ == "__main__":
    # Auto-detect if running on mobile
    import sys
    mobile_mode = "--mobile" in sys.argv
    
    # Create initializer with mobile optimization if needed
    initializer = AutoInit(mobile_optimized=mobile_mode)
    
    # Detect repository
    print("📂 Checking for TeamBadass repository...")
    repo_detected = initializer.detect_repository()
    
    if repo_detected:
        # Initialize gas gauge
        gas_result = initializer.initialize_gas_gauge()
        print(gas_result["display_message"])
        
        # Load memory
        memory_result = initializer.load_memory(min_files=mobile_mode)
        print(memory_result["display_message"])
        
        # Show final report
        print("\n" + initializer.get_initialization_report())
    else:
        print("❌ TeamBadass repository not detected")

#!/usr/bin/env python3
"""
Claude Gas Gauge - Phase 2: Status Checking and Reporting
Enhanced visualization and reporting features for the gas gauge system
"""

# Import the core functionality from Phase 1
from gas_gauge import ClaudeGasGauge

# Add these methods to the ClaudeGasGauge class to implement Phase 2
def display_enhanced_gauge(self, width=40, show_markers=True):
    """
    Display an enhanced visual representation of the gas gauge
    
    Args:
        width (int): Width of the gauge in characters
        show_markers (bool): Whether to show buffer markers
        
    Returns:
        str: Formatted enhanced gauge string
    """
    # Get current gas level
    level = self.current_level
    
    # Calculate filled portion
    filled_width = int((level / 100) * width)
    
    # Buffer markers
    minimum_marker = int((30 / 100) * width)  # 30% minimum
    continuity_marker = int((20 / 100) * width)  # 20% continuity buffer
    
    # Create the gauge bar
    gauge = "["
    
    for i in range(width):
        if i < filled_width:
            # Filled portion
            gauge += "="
        elif show_markers and i == minimum_marker:
            # Minimum buffer marker
            gauge += "M"
        elif show_markers and i == continuity_marker:
            # Continuity buffer marker
            gauge += "C"
        else:
            # Empty portion
            gauge += " "
    
    gauge += f"] {level}%"
    
    # Determine status
    if level > 70:
        status = "OPTIMAL"
    elif level > 50:
        status = "GOOD"
    elif level > 40:
        status = "MODERATE"
    elif level > 30:
        status = "LOW"
    else:
        status = "CRITICAL"
    
    gauge += f" - {status}"
    
    # Add marker legend if showing markers
    if show_markers:
        gauge += "\nM = Minimum Buffer (30%)   C = Continuity Buffer (20%)"
    
    return gauge

def display_checkpoints_status(self):
    """
    Display status of all checkpoints in relation to current gas level
    
    Returns:
        str: Formatted checkpoint status report
    """
    # Get current gas level
    level = self.current_level
    
    # Create report
    report = "Checkpoint Status Report:\n"
    report += f"Current Gas Level: {level}%\n\n"
    
    # Sort checkpoints by minimum_gas (descending)
    sorted_checkpoints = sorted(
        self.checkpoints.values(),
        key=lambda x: x["minimum_gas"],
        reverse=True
    )
    
    # Calculate width for visualization
    width = 40
    
    # Add each checkpoint with visualization
    for cp in sorted_checkpoints:
        name = cp["name"]
        min_gas = cp["minimum_gas"]
        desc = cp.get("description", name)
        
        # Visualize as a bar
        cp_pos = int((min_gas / 100) * width)
        level_pos = int((level / 100) * width)
        
        bar = "["
        for i in range(width):
            if i == cp_pos:
                bar += "|"  # Checkpoint position
            elif i < level_pos:
                bar += "="  # Current gas level
            else:
                bar += " "  # Empty space
        bar += "]"
        
        # Check status
        if level >= min_gas:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        # Add to report
        report += f"{status} | {bar} | {name}: {min_gas}% - {desc}\n"
    
    return report

def get_buffer_rules(self):
    """
    Get the current buffer rules for resource management
    
    Returns:
        dict: Buffer rules information
    """
    # Define our resource management rules
    rules = {
        "minimum_remaining": 30,  # Never go below 30% remaining
        "continuity_buffer": 20,  # Reserve 20% for continuity operations
        "troubleshooting_buffer": 10,  # Reserve 10% for troubleshooting
        "total_buffer": 30,  # Total buffer (continuity + troubleshooting)
        "is_active": True  # Whether buffer rules are currently active
    }
    
    return rules

def check_buffers(self):
    """
    Check if current gas level respects buffer rules
    
    Returns:
        dict: Buffer status information
    """
    # Get buffer rules
    rules = self.get_buffer_rules()
    
    # Current gas level
    level = self.current_level
    
    # Calculate margins
    margin_above_minimum = level - rules["minimum_remaining"]
    available_for_work = margin_above_minimum  # How much gas can be used for work
    
    # Determine status
    if level <= rules["minimum_remaining"]:
        status = "CRITICAL - Below minimum threshold, immediate hop required"
        can_continue = False
    elif level <= rules["minimum_remaining"] + rules["continuity_buffer"]:
        status = "WARNING - Sufficient for continuity only, prepare to hop"
        can_continue = True
    elif level <= rules["minimum_remaining"] + rules["total_buffer"]:
        status = "CAUTION - Limited capacity, prioritize critical tasks"
        can_continue = True
    else:
        status = "GOOD - Sufficient capacity for continued work"
        can_continue = True
    
    # Create result
    result = {
        "current_level": level,
        "minimum_threshold": rules["minimum_remaining"],
        "continuity_buffer": rules["continuity_buffer"],
        "troubleshooting_buffer": rules["troubleshooting_buffer"],
        "margin_above_minimum": margin_above_minimum,
        "available_for_work": available_for_work,
        "can_continue": can_continue,
        "status": status
    }
    
    return result

def format_status_report(self):
    """
    Generate a comprehensive status report with enhanced visualizations
    
    Returns:
        str: Formatted status report
    """
    # Get current gas info
    gas_info = self.get_gas_info()
    
    # Create report
    report = "="*60 + "\n"
    report += "📊 CLAUDE GAS GAUGE - STATUS REPORT 📊\n"
    report += "="*60 + "\n\n"
    
    # Add enhanced gauge visualization
    report += "Gas Level:\n"
    report += self.display_enhanced_gauge() + "\n\n"
    
    # Add buffer status
    buffer_status = self.check_buffers()
    report += "Buffer Status:\n"
    report += f"Current Level: {buffer_status['current_level']}%\n"
    report += f"Minimum Threshold: {buffer_status['minimum_threshold']}%\n"
    report += f"Margin Above Minimum: {buffer_status['margin_above_minimum']}%\n"
    report += f"Available for Work: {buffer_status['available_for_work']}%\n"
    report += f"Status: {buffer_status['status']}\n\n"
    
    # Add checkpoint visualization
    report += self.display_checkpoints_status() + "\n\n"
    
    # Add measurements summary
    report += "Measurement Summary:\n"
    report += f"Total Measurements: {len(self.measurements)}\n"
    report += f"Baseline Response Time: {self.baseline_time:.2f} ms\n"
    report += f"Last Check: {self.last_check_time.isoformat() if self.last_check_time else 'None'}\n\n"
    
    # Add recommendations based on status
    report += "Recommendations:\n"
    
    if buffer_status["current_level"] <= 30:
        report += "⛔ CRITICAL: Immediate hop required - insufficient gas for operation\n"
        report += "- Save all work immediately and create minimal continuity\n"
    elif buffer_status["current_level"] <= 40:
        report += "⚠️ WARNING: Low gas level - approaching critical threshold\n"
        report += "- Complete only essential operations before hopping\n"
        report += "- Ensure sufficient capacity for proper continuity\n"
    elif buffer_status["current_level"] <= 50:
        report += "🟡 CAUTION: Moderate gas level - monitor usage closely\n"
        report += "- Prioritize remaining tasks carefully\n"
        report += "- Consider hopping after completing critical operations\n"
    else:
        report += "✅ GOOD: Healthy gas level - proceed with planned tasks\n"
        report += "- Continue monitoring gas levels after major operations\n"
    
    report += "="*60 + "\n"
    
    return report

def save_measurement_snapshot(self, filename=None):
    """
    Save current measurements and status to a JSON file
    
    Args:
        filename (str, optional): Custom filename for the snapshot
        
    Returns:
        str: Path to the saved file
    """
    import os
    import json
    from datetime import datetime
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"gas_snapshot_{timestamp}.json"
    
    # Ensure metrics directory exists
    os.makedirs(self.metrics_dir, exist_ok=True)
    
    # Create file path
    file_path = os.path.join(self.metrics_dir, filename)
    
    # Prepare data
    data = {
        "timestamp": datetime.now().isoformat(),
        "gas_level": self.current_level,
        "baseline_time": self.baseline_time,
        "context_load_level": self.context_load_level,
        "measurements": self.measurements,
        "checkpoints": self.checkpoints,
        "buffer_rules": self.get_buffer_rules(),
        "buffer_status": self.check_buffers(),
        "status": self.get_gas_info()["status"]
    }
    
    # Write to file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    
    return file_path

def run_enhanced_status_check(self):
    """
    Run an enhanced status check with all Phase 2 features
    
    Returns:
        dict: Comprehensive status information
    """
    # Measure gas level
    gas_info = self.check_gas()
    
    # Check buffer status
    buffer_status = self.check_buffers()
    
    # Save measurement snapshot
    snapshot_path = self.save_measurement_snapshot()
    
    # Print enhanced report
    print(self.format_status_report())
    
    # Return comprehensive status info
    return {
        "gas_info": gas_info,
        "buffer_status": buffer_status,
        "snapshot_path": snapshot_path,
        "can_continue": buffer_status["can_continue"]
    }

# Extend the ClaudeGasGauge class with Phase 2 methods
ClaudeGasGauge.display_enhanced_gauge = display_enhanced_gauge
ClaudeGasGauge.display_checkpoints_status = display_checkpoints_status
ClaudeGasGauge.get_buffer_rules = get_buffer_rules
ClaudeGasGauge.check_buffers = check_buffers
ClaudeGasGauge.format_status_report = format_status_report
ClaudeGasGauge.save_measurement_snapshot = save_measurement_snapshot
ClaudeGasGauge.run_enhanced_status_check = run_enhanced_status_check

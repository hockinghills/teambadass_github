class GasGauge:
    """
    A minimal utility to silently track Claude's processing capacity
    """
    
    def __init__(self):
        self.current_level = 100
        self.context_load_level = None
        self.initial_level = 100
        
    def check(self, check_type="standard", silent=True):
        """
        Check Claude's gas level
        
        Args:
            check_type: Type of check ("initial", "post_context", "task")
            silent: Whether to return info without displaying
            
        Returns:
            dict: Gas level information
        """
        # In a real implementation, we'd mea
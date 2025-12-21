"""
PixARR Agent for managing design files.
"""

from pixarr_design.core.integrity import IntegrityAuditor


class PixARRAgent:
    """Main agent for PixARR Design system."""
    
    def __init__(self):
        self.active = False
        self.auditor = IntegrityAuditor()
    
    def activate(self):
        """Activate the agent."""
        self.active = True
        print("✅ PixARR Agent activated")
    
    def audit_integrity(self):
        """
        Run integrity audit on all monitored files.
        
        Returns:
            Dictionary with audit results
        """
        if not self.active:
            raise RuntimeError("Agent must be activated before running audit")
        
        return self.auditor.audit_all()

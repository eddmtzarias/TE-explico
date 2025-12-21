"""
Settings and configuration for PixARR Design system.
"""

import os
from pathlib import Path


class Settings:
    """Configuration settings for PixARR Design system."""
    
    # Supervisor/system identity
    SUPERVISOR_NAME = os.environ.get("PIXARR_SUPERVISOR", "PixARR-System")
    
    # Directory structure
    BASE_DIR = Path(__file__).parent.parent.parent
    DESIGN_DIR = BASE_DIR / "designs"
    METADATA_DIR = BASE_DIR / ".pixarr_metadata"
    
    # File extensions to monitor
    MONITORED_EXTENSIONS = [".svg", ".png", ".jpg", ".jpeg", ".pdf", ".ai", ".psd"]
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        cls.DESIGN_DIR.mkdir(exist_ok=True)
        cls.METADATA_DIR.mkdir(exist_ok=True)

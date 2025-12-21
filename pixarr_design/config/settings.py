"""
Configuration settings for PixARR Design system.
"""

import os
from pathlib import Path
from typing import List


class Settings:
    """Global configuration for PixARR Design system."""

    # Supervisor Information
    SUPERVISOR_NAME: str = "Melampe001"
    SUPERVISOR_EMAIL: str = "tokraagcorp@gmail.com"

    # Project Root
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent.resolve()

    # Directory Structure
    DESIGNS_DIR: Path = PROJECT_ROOT / "designs"
    ACTIVE_DIR: Path = DESIGNS_DIR / "active"
    ARCHIVE_DIR: Path = DESIGNS_DIR / "archive"
    QUARANTINE_DIR: Path = DESIGNS_DIR / "quarantine"

    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    REPORTS_DIR: Path = PROJECT_ROOT / "reports"

    # Log Files
    AUDIT_LOG: Path = LOGS_DIR / "audit_log.json"
    INCIDENT_LOG: Path = LOGS_DIR / "incident_log.json"

    # Monitored Extensions
    MONITORED_EXTENSIONS: List[str] = [
        ".psd",
        ".ai",
        ".xd",
        ".fig",
        ".sketch",
        ".png",
        ".jpg",
        ".jpeg",
        ".svg",
        ".webp",
        ".md",
        ".txt",
    ]

    # Hash Algorithm
    HASH_ALGORITHM: str = "sha256"
    HASH_BLOCK_SIZE: int = 8192  # 8KB blocks for efficient reading

    # Alert Levels
    ALERT_LEVELS = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }

    @classmethod
    def ensure_directories(cls) -> None:
        """Create all required directories if they don't exist."""
        directories = [
            cls.DESIGNS_DIR,
            cls.ACTIVE_DIR,
            cls.ARCHIVE_DIR,
            cls.QUARANTINE_DIR,
            cls.LOGS_DIR,
            cls.REPORTS_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def is_monitored_file(cls, filename: str) -> bool:
        """
        Check if a file should be monitored based on its extension.

        Args:
            filename: Name of the file to check

        Returns:
            True if file extension is in monitored list
        """
        return any(filename.lower().endswith(ext) for ext in cls.MONITORED_EXTENSIONS)

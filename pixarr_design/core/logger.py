"""
Audit logging system for PixARR Design.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from ..config.settings import Settings


class AuditLogger:
    """Immutable audit logger for tracking all system events."""

    def __init__(self):
        """Initialize the audit logger."""
        Settings.ensure_directories()
        self.audit_log_path = Settings.AUDIT_LOG
        self.incident_log_path = Settings.INCIDENT_LOG

        # Initialize log files if they don't exist
        self._ensure_log_files()

    def _ensure_log_files(self) -> None:
        """Ensure log files exist and are properly formatted."""
        for log_path in [self.audit_log_path, self.incident_log_path]:
            if not log_path.exists():
                log_path.write_text("[]")

    def _read_log(self, log_path: Path) -> List[Dict[str, Any]]:
        """
        Read a log file.

        Args:
            log_path: Path to the log file

        Returns:
            List of log entries
        """
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_log(self, log_path: Path, entries: List[Dict[str, Any]]) -> None:
        """
        Write entries to a log file.

        Args:
            log_path: Path to the log file
            entries: List of log entries
        """
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)

    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Log a generic event to the audit log.

        Args:
            event_type: Type of event
            data: Event data
        """
        entries = self._read_log(self.audit_log_path)
        entry = {
            "type": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **data,
        }
        entries.append(entry)
        self._write_log(self.audit_log_path, entries)

    def log_artifact_creation(
        self,
        filename: str,
        file_hash: str,
        creator: str,
        version: int = 1,
        status: str = "active",
    ) -> None:
        """
        Log the creation of a new artifact.

        Args:
            filename: Name of the artifact
            file_hash: SHA-256 hash of the file
            creator: Creator of the artifact
            version: Version number (default: 1)
            status: Status of the artifact (default: "active")
        """
        data = {
            "filename": filename,
            "hash": file_hash,
            "creator": creator,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "version": version,
            "status": status,
            "supervisor": Settings.SUPERVISOR_NAME,
        }
        self.log_event("artifact_created", data)

    def log_artifact_modification(
        self,
        filename: str,
        file_hash: str,
        modifier: str,
        description: str,
        previous_hash: str,
        version: int,
    ) -> None:
        """
        Log a modification to an existing artifact.

        Args:
            filename: Name of the artifact
            file_hash: New SHA-256 hash
            modifier: Who modified the artifact
            description: Description of the modification
            previous_hash: Previous hash value
            version: New version number
        """
        data = {
            "filename": filename,
            "hash": file_hash,
            "modifier": modifier,
            "modified_at": datetime.utcnow().isoformat() + "Z",
            "description": description,
            "previous_hash": previous_hash,
            "version": version,
            "supervisor": Settings.SUPERVISOR_NAME,
        }
        self.log_event("artifact_modified", data)

    def log_incident(
        self,
        incident_type: str,
        filename: str,
        suspicious_actor: str,
        description: str,
        severity: str = "HIGH",
    ) -> None:
        """
        Log a security incident to the incident log.

        Args:
            incident_type: Type of incident
            filename: File involved in the incident
            suspicious_actor: Actor involved
            description: Description of the incident
            severity: Severity level (default: "HIGH")
        """
        entries = self._read_log(self.incident_log_path)
        entry = {
            "type": incident_type,
            "filename": filename,
            "suspicious_actor": suspicious_actor,
            "description": description,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "supervisor": Settings.SUPERVISOR_NAME,
        }
        entries.append(entry)
        self._write_log(self.incident_log_path, entries)

    def log_audit(self, files_verified: int, anomalies: int, details: str) -> None:
        """
        Log an integrity audit.

        Args:
            files_verified: Number of files verified
            anomalies: Number of anomalies detected
            details: Detailed audit information
        """
        data = {
            "files_verified": files_verified,
            "anomalies": anomalies,
            "details": details,
            "supervisor": Settings.SUPERVISOR_NAME,
        }
        self.log_event("integrity_audit", data)

    def get_audit_history(self) -> List[Dict[str, Any]]:
        """
        Get the complete audit history.

        Returns:
            List of all audit log entries
        """
        return self._read_log(self.audit_log_path)

    def get_incident_history(self) -> List[Dict[str, Any]]:
        """
        Get the complete incident history.

        Returns:
            List of all incident log entries
        """
        return self._read_log(self.incident_log_path)

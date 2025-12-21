"""
Alert system for PixARR Design.
"""

from datetime import datetime
from typing import List, Dict, Any
from enum import Enum
from ..config.settings import Settings


class AlertLevel(Enum):
    """Alert severity levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AlertSystem:
    """Alert system for notifying supervisors of important events."""

    def __init__(self):
        """Initialize the alert system."""
        self.alert_history: List[Dict[str, Any]] = []

    def send_alert(
        self,
        level: AlertLevel,
        message: str,
        filename: str = None,
        actor: str = None,
    ) -> None:
        """
        Send an alert to the supervisor.

        Args:
            level: Severity level of the alert
            message: Alert message
            filename: Optional filename related to the alert
            actor: Optional actor related to the alert
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        alert = {
            "level": level.name,
            "severity": level.value,
            "message": message,
            "timestamp": timestamp,
            "supervisor": Settings.SUPERVISOR_NAME,
            "email": Settings.SUPERVISOR_EMAIL,
        }

        if filename:
            alert["filename"] = filename
        if actor:
            alert["actor"] = actor

        # Store in history
        self.alert_history.append(alert)

        # Simulate notification (in production, this would send actual notifications)
        self._simulate_notification(alert)

    def _simulate_notification(self, alert: Dict[str, Any]) -> None:
        """
        Simulate sending a notification to the supervisor.

        Args:
            alert: Alert data
        """
        level_icon = {
            "LOW": "ℹ️",
            "MEDIUM": "⚡",
            "HIGH": "⚠️",
            "CRITICAL": "🚨",
        }

        icon = level_icon.get(alert["level"], "📢")
        print(f"\n{icon} ALERTA [{alert['level']}] enviada a {alert['email']}")
        print(f"   Mensaje: {alert['message']}")
        print(f"   Timestamp: {alert['timestamp']}")

    def get_alert_history(self) -> List[Dict[str, Any]]:
        """
        Get the complete alert history.

        Returns:
            List of all alerts sent
        """
        return self.alert_history

    def get_alerts_by_level(self, level: AlertLevel) -> List[Dict[str, Any]]:
        """
        Get alerts filtered by severity level.

        Args:
            level: Alert level to filter by

        Returns:
            List of alerts matching the specified level
        """
        return [
            alert for alert in self.alert_history if alert["level"] == level.name
        ]

    def clear_history(self) -> None:
        """Clear the alert history."""
        self.alert_history.clear()

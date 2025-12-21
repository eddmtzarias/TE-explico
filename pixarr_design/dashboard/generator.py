"""
Report generator for PixARR Design system.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from ..config.settings import Settings
from ..core.logger import AuditLogger
from ..core.alerts import AlertSystem
from ..core.integrity import IntegrityValidator


class ReportGenerator:
    """Generator for markdown audit reports."""

    def __init__(
        self,
        audit_logger: AuditLogger,
        alert_system: AlertSystem,
        integrity_validator: IntegrityValidator,
    ):
        """
        Initialize the report generator.

        Args:
            audit_logger: Audit logger instance
            alert_system: Alert system instance
            integrity_validator: Integrity validator instance
        """
        self.audit_logger = audit_logger
        self.alert_system = alert_system
        self.integrity_validator = integrity_validator

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate a comprehensive markdown report.

        Args:
            output_path: Optional custom output path

        Returns:
            Path to the generated report
        """
        # Generate filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        if output_path:
            report_path = Path(output_path)
        else:
            report_path = Settings.REPORTS_DIR / f"dashboard_{timestamp}.md"

        # Ensure reports directory exists
        report_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate report content
        content = self._generate_content()

        # Write report
        report_path.write_text(content, encoding="utf-8")

        return str(report_path)

    def _generate_content(self) -> str:
        """
        Generate the markdown content for the report.

        Returns:
            Markdown formatted report
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        # Build report sections
        sections = [
            self._generate_header(timestamp),
            self._generate_statistics(),
            self._generate_artifacts_table(),
            self._generate_incidents_section(),
            self._generate_alerts_section(),
            self._generate_footer(),
        ]

        return "\n\n".join(sections)

    def _generate_header(self, timestamp: str) -> str:
        """Generate report header."""
        return f"""# 🎨 PixARR Design - Reporte de Auditoría

**Fecha de Generación:** {timestamp}  
**Supervisor:** {Settings.SUPERVISOR_NAME}  
**Contacto:** {Settings.SUPERVISOR_EMAIL}

---"""

    def _generate_statistics(self) -> str:
        """Generate statistics section."""
        # Get audit history
        audit_history = self.audit_logger.get_audit_history()
        incident_history = self.audit_logger.get_incident_history()

        # Count artifacts by status
        artifacts = [e for e in audit_history if e.get("type") == "artifact_created"]
        modifications = [e for e in audit_history if e.get("type") == "artifact_modified"]

        # Count by status (simplified for now)
        total_artifacts = len(artifacts)
        active_artifacts = total_artifacts  # Would need to track status changes
        quarantine_files = len(incident_history)

        return f"""## 📊 Estadísticas Generales

| Métrica | Valor |
|---------|-------|
| **Total de Artefactos** | {total_artifacts} |
| **Artefactos Activos** | {active_artifacts} |
| **Archivos en Cuarentena** | {quarantine_files} |
| **Modificaciones Totales** | {len(modifications)} |
| **Incidentes Detectados** | {len(incident_history)} |"""

    def _generate_artifacts_table(self) -> str:
        """Generate artifacts table."""
        audit_history = self.audit_logger.get_audit_history()

        # Collect all artifact events
        events = []
        for entry in audit_history:
            event_type = entry.get("type", "")
            if event_type == "artifact_created":
                events.append(
                    {
                        "archivo": entry.get("filename", "N/A"),
                        "fecha": entry.get("created_at", "N/A")[:19].replace("T", " "),
                        "cambio": "Creación",
                        "responsable": entry.get("creator", "N/A"),
                        "hash": entry.get("hash", "N/A")[:8] + "...",
                        "estado": "OK",
                    }
                )
            elif event_type == "artifact_modified":
                events.append(
                    {
                        "archivo": entry.get("filename", "N/A"),
                        "fecha": entry.get("modified_at", "N/A")[:19].replace("T", " "),
                        "cambio": f"Edición: {entry.get('description', 'N/A')}",
                        "responsable": entry.get("modifier", "N/A"),
                        "hash": entry.get("hash", "N/A")[:8] + "...",
                        "estado": "OK",
                    }
                )

        # Add incidents
        incident_history = self.audit_logger.get_incident_history()
        for incident in incident_history:
            events.append(
                {
                    "archivo": incident.get("filename", "N/A"),
                    "fecha": incident.get("timestamp", "N/A")[:19].replace("T", " "),
                    "cambio": f"Incidente: {incident.get('type', 'N/A')}",
                    "responsable": incident.get("suspicious_actor", "N/A"),
                    "hash": "N/A",
                    "estado": "⚠️ ALERTA",
                }
            )

        # Build table
        table = """## 📋 Tabla de Artefactos

| Archivo | Fecha | Cambio | Responsable | Hash | Estado |
|---------|-------|--------|-------------|------|--------|"""

        if not events:
            table += "\n| *Sin eventos registrados* | - | - | - | - | - |"
        else:
            for event in events:
                table += f"\n| {event['archivo']} | {event['fecha']} | {event['cambio']} | {event['responsable']} | {event['hash']} | {event['estado']} |"

        return table

    def _generate_incidents_section(self) -> str:
        """Generate incidents section."""
        incidents = self.audit_logger.get_incident_history()

        section = "## 🚨 Incidentes de Seguridad\n\n"

        if not incidents:
            section += "*No se han detectado incidentes de seguridad.*"
        else:
            for i, incident in enumerate(incidents, 1):
                section += f"""### Incidente #{i}

- **Tipo:** {incident.get('type', 'N/A')}
- **Archivo:** {incident.get('filename', 'N/A')}
- **Actor Sospechoso:** {incident.get('suspicious_actor', 'N/A')}
- **Severidad:** {incident.get('severity', 'N/A')}
- **Descripción:** {incident.get('description', 'N/A')}
- **Timestamp:** {incident.get('timestamp', 'N/A')}

"""

        return section.rstrip()

    def _generate_alerts_section(self) -> str:
        """Generate alerts section."""
        alerts = self.alert_system.get_alert_history()

        section = "## 📧 Alertas Enviadas\n\n"

        if not alerts:
            section += "*No se han enviado alertas.*"
        else:
            for i, alert in enumerate(alerts, 1):
                section += f"""### Alerta #{i}

- **Nivel:** {alert.get('level', 'N/A')}
- **Mensaje:** {alert.get('message', 'N/A')}
- **Destinatario:** {alert.get('email', 'N/A')}
- **Timestamp:** {alert.get('timestamp', 'N/A')}

"""

        return section.rstrip()

    def _generate_footer(self) -> str:
        """Generate report footer."""
        return f"""---

## 🔒 Información de Sistema

**Sistema:** PixARR Design v1.0  
**Supervisor Asignado:** {Settings.SUPERVISOR_NAME}  
**Email de Contacto:** {Settings.SUPERVISOR_EMAIL}  
**Workspace:** {Settings.PROJECT_ROOT}

---

*Reporte generado automáticamente por PixARR Design System*"""

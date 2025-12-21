"""
PixARR Design Agent - Main autonomous agent for design artifact supervision.
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from ..config.settings import Settings
from ..utils.hash_utils import calculate_file_hash
from ..utils.metadata import inject_metadata, validate_metadata
from .logger import AuditLogger
from .alerts import AlertSystem, AlertLevel
from .integrity import IntegrityValidator


class PixARRAgent:
    """
    Autonomous agent for supervising design artifacts.

    The PixARR agent monitors, validates, and protects design files
    with comprehensive audit trails and automated incident response.
    """

    def __init__(self, workspace: Optional[str] = None):
        """
        Initialize the PixARR agent.

        Args:
            workspace: Optional workspace path (defaults to project root)
        """
        self.workspace = Path(workspace) if workspace else Settings.PROJECT_ROOT
        self.logger = AuditLogger()
        self.alert_system = AlertSystem()
        self.integrity_validator = IntegrityValidator()
        self.active = False

        # Ensure all directories exist
        Settings.ensure_directories()

    def activate(self) -> None:
        """Activate the PixARR agent and log the activation."""
        self.active = True
        self.logger.log_event(
            "agent_activated",
            {
                "workspace": str(self.workspace),
                "supervisor": Settings.SUPERVISOR_NAME,
                "activated_at": datetime.utcnow().isoformat() + "Z",
            },
        )
        print(f"✅ Agente PixARR Design activado")
        print(f"   Supervisor: {Settings.SUPERVISOR_NAME}")
        print(f"   Workspace: {self.workspace}")

    def create_artifact(self, file_path: str, creator: str) -> Dict[str, Any]:
        """
        Create and register a new design artifact.

        Args:
            file_path: Path to the artifact file
            creator: Name of the creator

        Returns:
            Dictionary containing artifact information

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        if not self.active:
            raise RuntimeError("Agent must be activated before use")

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Calculate hash
        file_hash = calculate_file_hash(str(path))

        # Create metadata
        metadata = {
            "filename": path.name,
            "hash": file_hash,
            "creator": creator,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "version": 1,
            "status": "active",
            "supervisor": Settings.SUPERVISOR_NAME,
        }

        # Inject metadata
        inject_metadata(str(path), metadata)

        # Log creation
        self.logger.log_artifact_creation(
            filename=path.name,
            file_hash=file_hash,
            creator=creator,
            version=1,
            status="active",
        )

        print(f"✅ Artefacto creado: {path.name}")
        print(f"   Hash: {file_hash[:16]}...")
        print(f"   Creador: {creator}")

        return metadata

    def modify_artifact(
        self, file_path: str, modifier: str, description: str
    ) -> Dict[str, Any]:
        """
        Register a modification to an existing artifact.

        Args:
            file_path: Path to the artifact file
            modifier: Name of the modifier
            description: Description of the modification

        Returns:
            Dictionary containing updated artifact information

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        if not self.active:
            raise RuntimeError("Agent must be activated before use")

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Get existing metadata
        old_metadata = validate_metadata(str(path))
        previous_hash = old_metadata.get("hash", "") if old_metadata else ""
        previous_version = old_metadata.get("version", 0) if old_metadata else 0

        # Calculate new hash
        new_hash = calculate_file_hash(str(path))

        # Create updated metadata
        new_version = previous_version + 1
        metadata = {
            "filename": path.name,
            "hash": new_hash,
            "creator": old_metadata.get("creator", "Unknown") if old_metadata else "Unknown",
            "created_at": old_metadata.get("created_at", datetime.utcnow().isoformat() + "Z") if old_metadata else datetime.utcnow().isoformat() + "Z",
            "version": new_version,
            "status": "active",
            "supervisor": Settings.SUPERVISOR_NAME,
            "last_modified_by": modifier,
            "last_modified_at": datetime.utcnow().isoformat() + "Z",
            "modification_description": description,
            "previous_hash": previous_hash,
        }

        # Inject updated metadata
        inject_metadata(str(path), metadata)

        # Log modification
        self.logger.log_artifact_modification(
            filename=path.name,
            file_hash=new_hash,
            modifier=modifier,
            description=description,
            previous_hash=previous_hash,
            version=new_version,
        )

        print(f"✅ Modificación registrada: {path.name}")
        print(f"   Versión: {new_version}")
        print(f"   Modificador: {modifier}")
        print(f"   Cambio: {description}")

        return metadata

    def detect_unauthorized_access(
        self, file_path: str, suspicious_actor: str
    ) -> None:
        """
        Detect and respond to unauthorized access attempts.

        Args:
            file_path: Path to the compromised file
            suspicious_actor: Name of the suspicious actor

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        if not self.active:
            raise RuntimeError("Agent must be activated before use")

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Move file to quarantine
        quarantine_path = Settings.QUARANTINE_DIR / path.name
        shutil.move(str(path), str(quarantine_path))

        # Log incident
        self.logger.log_incident(
            incident_type="unauthorized_access",
            filename=path.name,
            suspicious_actor=suspicious_actor,
            description=f"Acceso no autorizado detectado. Archivo movido a cuarentena.",
            severity="HIGH",
        )

        # Send alert
        self.alert_system.send_alert(
            level=AlertLevel.HIGH,
            message=f"⚠️ ACCESO NO AUTORIZADO detectado en {path.name}",
            filename=path.name,
            actor=suspicious_actor,
        )

        print(f"🚨 ALERTA: Acceso no autorizado detectado")
        print(f"   Archivo: {path.name}")
        print(f"   Actor sospechoso: {suspicious_actor}")
        print(f"   Acción: Movido a cuarentena")
        print(f"   Supervisor notificado: {Settings.SUPERVISOR_NAME}")

    def audit_integrity(self, directory: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform an integrity audit on all monitored files.

        Args:
            directory: Optional directory to audit (defaults to active directory)

        Returns:
            Dictionary containing audit results
        """
        if not self.active:
            raise RuntimeError("Agent must be activated before use")

        # Use active directory if not specified
        audit_dir = directory if directory else str(Settings.ACTIVE_DIR)

        # Clear previous results
        self.integrity_validator.clear_results()

        # Verify all files
        results = self.integrity_validator.verify_directory(audit_dir)
        summary = self.integrity_validator.get_summary()
        anomalies = self.integrity_validator.get_anomalies()

        # Log audit
        self.logger.log_audit(
            files_verified=summary["total_files"],
            anomalies=summary["anomalies"],
            details=f"Verified {summary['total_files']} files in {audit_dir}",
        )

        print(f"📊 AUDITORÍA DE INTEGRIDAD")
        print(f"   Archivos verificados: {summary['total_files']}")
        print(f"   Anomalías detectadas: {summary['anomalies']}")

        if summary["anomalies"] == 0:
            print(f"   ✅ Todos los archivos pasaron la auditoría")
        else:
            print(f"   ⚠️ Se detectaron {summary['anomalies']} anomalías")

        return {
            "summary": summary,
            "results": results,
            "anomalies": anomalies,
        }

    def generate_report(self) -> str:
        """
        Generate a comprehensive audit report.

        Returns:
            Path to the generated report file
        """
        if not self.active:
            raise RuntimeError("Agent must be activated before use")

        from ..dashboard.generator import ReportGenerator

        generator = ReportGenerator(
            audit_logger=self.logger,
            alert_system=self.alert_system,
            integrity_validator=self.integrity_validator,
        )

        report_path = generator.generate_report()
        print(f"✅ Reporte generado: {report_path}")

        return report_path

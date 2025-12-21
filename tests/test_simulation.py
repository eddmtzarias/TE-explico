"""
Tests for the complete simulation workflow.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from PIL import Image
from pixarr_design.core.agent import PixARRAgent
from pixarr_design.config.settings import Settings


@pytest.fixture
def setup_environment():
    """Setup test environment."""
    Settings.ensure_directories()


def test_complete_simulation_workflow(setup_environment, tmp_path):
    """Test the complete simulation workflow."""
    # Step 1: Initialize and activate agent
    agent = PixARRAgent()
    agent.activate()
    assert agent.active is True
    
    # Step 2: Create artifacts
    img1_path = Settings.ACTIVE_DIR / "test_artifact_1.png"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img1_path)
    
    metadata1 = agent.create_artifact(str(img1_path), "TestCreator")
    assert metadata1["version"] == 1
    
    # Step 3: Modify artifact
    img2_path = Settings.ACTIVE_DIR / "test_artifact_2.png"
    img2 = Image.new("RGB", (100, 100), color="blue")
    img2.save(img2_path)
    
    agent.create_artifact(str(img2_path), "TestCreator")
    metadata2 = agent.modify_artifact(str(img2_path), "TestModifier", "Changed color")
    assert metadata2["version"] == 2
    
    # Step 4: Audit integrity
    audit_results = agent.audit_integrity()
    assert "summary" in audit_results
    assert audit_results["summary"]["total_files"] >= 2
    
    # Step 5: Simulate incident (skip as it moves file)
    # Would need to recreate file after quarantine
    
    # Step 6: Generate report
    report_path = agent.generate_report()
    assert Path(report_path).exists()
    
    # Verify report content
    content = Path(report_path).read_text()
    assert "PixARR Design" in content
    assert "Estadísticas Generales" in content
    assert "Tabla de Artefactos" in content


def test_simulation_with_incidents(setup_environment):
    """Test simulation with incident detection."""
    agent = PixARRAgent()
    agent.activate()
    
    # Create artifact
    img_path = Settings.ACTIVE_DIR / "incident_test.png"
    img = Image.new("RGB", (50, 50), color="yellow")
    img.save(img_path)
    
    agent.create_artifact(str(img_path), "TestCreator")
    
    # Simulate unauthorized access
    agent.detect_unauthorized_access(str(img_path), "MaliciousActor")
    
    # Verify incident was logged
    incidents = agent.logger.get_incident_history()
    assert len(incidents) > 0
    assert incidents[-1]["suspicious_actor"] == "MaliciousActor"
    
    # Verify alert was sent
    alerts = agent.alert_system.get_alert_history()
    assert len(alerts) > 0
    
    # Verify file was moved to quarantine
    quarantine_file = Settings.QUARANTINE_DIR / "incident_test.png"
    assert quarantine_file.exists()


def test_multiple_artifact_versions(setup_environment):
    """Test creating multiple versions of an artifact."""
    agent = PixARRAgent()
    agent.activate()
    
    # Create initial artifact
    img_path = Settings.ACTIVE_DIR / "versioned_artifact.png"
    img = Image.new("RGB", (100, 100), color="green")
    img.save(img_path)
    
    metadata1 = agent.create_artifact(str(img_path), "Designer1")
    assert metadata1["version"] == 1
    
    # Modify multiple times
    for i in range(3):
        metadata = agent.modify_artifact(
            str(img_path),
            f"Designer{i+2}",
            f"Modification {i+1}"
        )
        assert metadata["version"] == i + 2
    
    # Check audit log
    audit_history = agent.logger.get_audit_history()
    modifications = [e for e in audit_history if e.get("type") == "artifact_modified"]
    assert len(modifications) >= 3


def test_report_generation_without_artifacts(setup_environment):
    """Test report generation when no artifacts exist."""
    agent = PixARRAgent()
    agent.activate()
    
    # Generate report immediately
    report_path = agent.generate_report()
    
    assert Path(report_path).exists()
    content = Path(report_path).read_text()
    assert "PixARR Design" in content

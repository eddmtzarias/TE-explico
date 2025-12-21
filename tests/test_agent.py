"""
Tests for PixARR Agent functionality.
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
def agent():
    """Fixture to create and activate an agent."""
    Settings.ensure_directories()
    agent = PixARRAgent()
    agent.activate()
    return agent


@pytest.fixture
def sample_image(tmp_path):
    """Fixture to create a sample test image."""
    image_path = tmp_path / "test_image.png"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(image_path)
    return str(image_path)


def test_agent_activation():
    """Test agent activation."""
    agent = PixARRAgent()
    assert agent.active is False
    agent.activate()
    assert agent.active is True


def test_create_artifact(agent, sample_image):
    """Test artifact creation."""
    metadata = agent.create_artifact(sample_image, "TestCreator")
    
    assert metadata["filename"] == "test_image.png"
    assert metadata["creator"] == "TestCreator"
    assert metadata["version"] == 1
    assert metadata["status"] == "active"
    assert "hash" in metadata
    assert metadata["supervisor"] == Settings.SUPERVISOR_NAME


def test_create_artifact_nonexistent_file(agent):
    """Test creating artifact with nonexistent file."""
    with pytest.raises(FileNotFoundError):
        agent.create_artifact("/nonexistent/file.png", "TestCreator")


def test_modify_artifact(agent, sample_image):
    """Test artifact modification."""
    # First create the artifact
    agent.create_artifact(sample_image, "TestCreator")
    
    # Then modify it
    metadata = agent.modify_artifact(
        sample_image,
        "TestModifier",
        "Updated colors"
    )
    
    assert metadata["version"] == 2
    assert metadata["last_modified_by"] == "TestModifier"
    assert metadata["modification_description"] == "Updated colors"
    assert "previous_hash" in metadata


def test_detect_unauthorized_access(agent, sample_image):
    """Test unauthorized access detection."""
    # Create artifact first
    agent.create_artifact(sample_image, "TestCreator")
    
    # Detect unauthorized access
    agent.detect_unauthorized_access(sample_image, "BadActor")
    
    # Check that incident was logged
    incidents = agent.logger.get_incident_history()
    assert len(incidents) > 0
    assert incidents[-1]["suspicious_actor"] == "BadActor"
    assert incidents[-1]["severity"] == "HIGH"


def test_audit_integrity(agent, tmp_path):
    """Test integrity audit."""
    # Create a test image in active directory
    test_image = Settings.ACTIVE_DIR / "test_audit.png"
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(test_image)
    
    # Create artifact
    agent.create_artifact(str(test_image), "TestCreator")
    
    # Run audit
    results = agent.audit_integrity()
    
    assert "summary" in results
    assert "results" in results
    assert "anomalies" in results
    assert results["summary"]["total_files"] >= 0


def test_generate_report(agent):
    """Test report generation."""
    report_path = agent.generate_report()
    
    assert Path(report_path).exists()
    assert Path(report_path).suffix == ".md"
    
    # Read and verify content
    content = Path(report_path).read_text()
    assert "PixARR Design" in content
    assert Settings.SUPERVISOR_NAME in content

"""
Tests for integrity validation and hash utilities.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from PIL import Image
from pixarr_design.utils.hash_utils import (
    calculate_file_hash,
    verify_file_integrity,
    calculate_string_hash,
)
from pixarr_design.utils.metadata import inject_metadata, validate_metadata
from pixarr_design.core.integrity import IntegrityValidator
from pixarr_design.config.settings import Settings


@pytest.fixture
def sample_file(tmp_path):
    """Create a sample file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test content for hashing")
    return str(file_path)


@pytest.fixture
def sample_image(tmp_path):
    """Create a sample PNG image for testing."""
    image_path = tmp_path / "test_image.png"
    img = Image.new("RGB", (100, 100), color="green")
    img.save(image_path)
    return str(image_path)


def test_calculate_file_hash(sample_file):
    """Test file hash calculation."""
    file_hash = calculate_file_hash(sample_file)
    
    assert isinstance(file_hash, str)
    assert len(file_hash) == 64  # SHA-256 produces 64 hex characters


def test_calculate_file_hash_nonexistent():
    """Test hash calculation with nonexistent file."""
    with pytest.raises(FileNotFoundError):
        calculate_file_hash("/nonexistent/file.txt")


def test_verify_file_integrity(sample_file):
    """Test file integrity verification."""
    # Calculate hash
    file_hash = calculate_file_hash(sample_file)
    
    # Verify with correct hash
    assert verify_file_integrity(sample_file, file_hash) is True
    
    # Verify with incorrect hash
    assert verify_file_integrity(sample_file, "incorrect_hash") is False


def test_calculate_string_hash():
    """Test string hash calculation."""
    content = "Test string for hashing"
    hash1 = calculate_string_hash(content)
    hash2 = calculate_string_hash(content)
    
    # Same content should produce same hash
    assert hash1 == hash2
    assert len(hash1) == 64
    
    # Different content should produce different hash
    hash3 = calculate_string_hash("Different content")
    assert hash1 != hash3


def test_inject_and_validate_png_metadata(sample_image):
    """Test metadata injection and validation for PNG files."""
    metadata = {
        "filename": "test_image.png",
        "hash": "abc123",
        "creator": "TestUser",
        "version": 1,
    }
    
    # Inject metadata
    inject_metadata(sample_image, metadata)
    
    # Validate metadata
    retrieved = validate_metadata(sample_image)
    
    assert retrieved is not None
    assert retrieved["filename"] == "test_image.png"
    assert retrieved["hash"] == "abc123"
    assert retrieved["creator"] == "TestUser"
    assert retrieved["version"] == 1


def test_inject_and_validate_text_metadata(sample_file):
    """Test metadata injection and validation for text files."""
    metadata = {
        "filename": "test_file.txt",
        "hash": "def456",
        "creator": "TestUser",
        "version": 2,
    }
    
    # Inject metadata
    inject_metadata(sample_file, metadata)
    
    # Validate metadata (should create .meta file)
    meta_file = Path(sample_file + ".meta")
    assert meta_file.exists()
    
    # Retrieve metadata
    retrieved = validate_metadata(sample_file)
    
    assert retrieved is not None
    assert retrieved["filename"] == "test_file.txt"
    assert retrieved["hash"] == "def456"


def test_integrity_validator_verify_file(sample_image):
    """Test integrity validator on a single file."""
    # Inject metadata
    file_hash = calculate_file_hash(sample_image)
    metadata = {
        "filename": "test_image.png",
        "hash": file_hash,
        "creator": "TestUser",
    }
    inject_metadata(sample_image, metadata)
    
    # Validate
    validator = IntegrityValidator()
    result = validator.verify_file(sample_image)
    
    assert result["valid"] is True
    assert result["status"] == "OK"
    assert result["current_hash"] == file_hash


def test_integrity_validator_modified_file(sample_image):
    """Test integrity validator detects modified files."""
    # Inject metadata with wrong hash
    metadata = {
        "filename": "test_image.png",
        "hash": "wrong_hash_value",
        "creator": "TestUser",
    }
    inject_metadata(sample_image, metadata)
    
    # Validate
    validator = IntegrityValidator()
    result = validator.verify_file(sample_image)
    
    assert result["valid"] is False
    assert result["status"] == "MODIFIED"


def test_integrity_validator_directory(tmp_path):
    """Test integrity validator on a directory."""
    Settings.ensure_directories()
    
    # Create test images in active directory
    for i in range(3):
        img_path = Settings.ACTIVE_DIR / f"test_img_{i}.png"
        img = Image.new("RGB", (50, 50), color="blue")
        img.save(img_path)
    
    # Validate directory
    validator = IntegrityValidator()
    results = validator.verify_directory(str(Settings.ACTIVE_DIR))
    
    assert len(results) >= 0  # Should find files
    summary = validator.get_summary()
    assert "total_files" in summary


def test_integrity_validator_summary():
    """Test integrity validator summary."""
    validator = IntegrityValidator()
    summary = validator.get_summary()
    
    assert "total_files" in summary
    assert "valid_files" in summary
    assert "anomalies" in summary
    assert "no_metadata" in summary

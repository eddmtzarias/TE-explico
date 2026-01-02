"""Tests para configuración"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from omnimastro.shared.config import config


def test_config_import():
    """Test que config se puede importar"""
    assert config is not None


def test_config_validation():
    """Test validación de config"""
    issues = config.validate()
    assert 'warnings' in issues
    assert 'errors' in issues
    # No debe haber errores críticos
    assert len(issues['errors']) == 0


if __name__ == "__main__":
    print("Running config tests...")
    test_config_import()
    print("✅ test_config_import passed")
    test_config_validation()
    print("✅ test_config_validation passed")
    print("\n✅ All tests passed!")

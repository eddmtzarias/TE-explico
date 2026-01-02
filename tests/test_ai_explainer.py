"""Tests para AI explainer"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_ai_explainer_import():
    """Test que AIExplainer se puede importar"""
    from omnimastro.core.ai_explainer import AIExplainer, UserLevel
    assert AIExplainer is not None
    assert UserLevel is not None


if __name__ == "__main__":
    print("Running AI explainer tests...")
    test_ai_explainer_import()
    print("✅ test_ai_explainer_import passed")
    print("\n✅ All tests passed!")

"""
Test de integración completo para validar el setup autónomo
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_directory_structure():
    """Verifica que los directorios requeridos existan"""
    project_root = Path(__file__).parent.parent
    
    required_dirs = [
        "data",
        "temp",
        ".cache",
        "logs",
        "screenshots",
        "designs",
        "omnimastro/core",
        "omnimastro/desktop",
        "omnimastro/shared",
        "tests",
    ]
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        assert full_path.exists(), f"Directorio faltante: {dir_path}"
        print(f"   ✅ {dir_path}/")


def test_core_modules():
    """Verifica que los módulos core se puedan importar"""
    modules = [
        ("omnimastro.shared.config", "config"),
        ("omnimastro.core.ai_explainer", "AIExplainer"),
        ("omnimastro.core.ai_explainer", "create_explainer"),
        ("omnimastro.core.ocr_engine", "OCREngine"),
        ("omnimastro.core.ai_engine", "AIEngine"),
    ]
    
    for module_path, item_name in modules:
        try:
            module = __import__(module_path, fromlist=[item_name])
            item = getattr(module, item_name)
            assert item is not None
            print(f"   ✅ {module_path}.{item_name}")
        except Exception as e:
            raise AssertionError(f"Error importando {module_path}.{item_name}: {e}")


def test_config_validation():
    """Verifica que la configuración se valide correctamente"""
    from omnimastro.shared.config import config
    
    issues = config.validate()
    assert 'warnings' in issues
    assert 'errors' in issues
    
    # No debe haber errores críticos de estructura
    assert len(issues['errors']) == 0, f"Errores críticos: {issues['errors']}"
    
    print(f"   ✅ Configuración válida")
    if issues['warnings']:
        print(f"   ⚠️  Advertencias: {len(issues['warnings'])}")


def test_env_file():
    """Verifica que el archivo .env exista"""
    project_root = Path(__file__).parent.parent
    env_path = project_root / ".env"
    
    assert env_path.exists(), "Archivo .env no existe"
    
    # Leer contenido
    content = env_path.read_text()
    
    # Verificar que tenga las secciones principales
    required_sections = [
        "=== PROYECTO ===",
        "=== IA / API KEYS ===",
        "=== OCR ===",
        "=== RECURSOS",
        "=== DATABASE ===",
    ]
    
    for section in required_sections:
        assert section in content, f"Sección faltante en .env: {section}"
    
    print(f"   ✅ Archivo .env completo")


def test_scripts():
    """Verifica que los scripts de setup existan"""
    project_root = Path(__file__).parent.parent
    scripts_dir = project_root / "scripts"
    
    required_scripts = [
        "resource_monitor.py",
        "auto_setup_env.py",
        "auto_core_setup.py",
        "RUN_AUTO_SETUP.bat",
    ]
    
    for script in required_scripts:
        script_path = scripts_dir / script
        assert script_path.exists(), f"Script faltante: {script}"
        print(f"   ✅ scripts/{script}")


def test_desktop_ui():
    """Verifica que la UI desktop esté creada"""
    from omnimastro.desktop.main import OmniMaestroApp
    
    assert OmniMaestroApp is not None
    print(f"   ✅ OmniMaestroApp class")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("🧪 TEST DE INTEGRACIÓN - SETUP AUTÓNOMO")
    print("="*60 + "\n")
    
    tests = [
        ("Estructura de directorios", test_directory_structure),
        ("Módulos core", test_core_modules),
        ("Validación de config", test_config_validation),
        ("Archivo .env", test_env_file),
        ("Scripts de setup", test_scripts),
        ("UI Desktop", test_desktop_ui),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"🔍 Test: {test_name}")
        try:
            test_func()
            passed += 1
            print(f"   ✅ PASSED\n")
        except AssertionError as e:
            failed += 1
            print(f"   ❌ FAILED: {e}\n")
        except Exception as e:
            failed += 1
            print(f"   ❌ ERROR: {e}\n")
    
    # Resumen
    print("="*60)
    print(f"📊 RESUMEN")
    print("="*60)
    print(f"   Total: {passed + failed}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print("="*60 + "\n")
    
    if failed == 0:
        print("🎉 ¡Todos los tests pasaron!")
        return 0
    else:
        print(f"⚠️  {failed} test(s) fallaron")
        return 1


if __name__ == "__main__":
    exit(main())

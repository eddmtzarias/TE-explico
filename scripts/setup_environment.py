#!/usr/bin/env python3
"""
Setup script for PixARR Design environment.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pixarr_design.config.settings import Settings


def setup_environment() -> None:
    """Setup the PixARR Design environment."""
    print("=" * 70)
    print("🔧 CONFIGURACIÓN DEL ENTORNO - PIXARR DESIGN")
    print("=" * 70)
    print()

    # Create directories
    print("📁 Creando estructura de directorios...")
    Settings.ensure_directories()

    directories = [
        Settings.DESIGNS_DIR,
        Settings.ACTIVE_DIR,
        Settings.ARCHIVE_DIR,
        Settings.QUARANTINE_DIR,
        Settings.LOGS_DIR,
        Settings.REPORTS_DIR,
    ]

    for directory in directories:
        if directory.exists():
            print(f"   ✅ {directory.relative_to(Settings.PROJECT_ROOT)}")
        else:
            print(f"   ❌ {directory.relative_to(Settings.PROJECT_ROOT)} - ERROR")

    print()

    # Check dependencies
    print("📦 Verificando dependencias...")
    dependencies = {
        "PIL": "Pillow",
        "dateutil": "python-dateutil",
        "watchdog": "watchdog (opcional)",
        "pytest": "pytest (testing)",
    }

    missing_deps = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ⚠️ {package} - No instalado")
            if "opcional" not in package and "testing" not in package:
                missing_deps.append(package.split()[0])

    print()

    if missing_deps:
        print("⚠️ Dependencias faltantes detectadas:")
        print(f"   Instalar con: pip install {' '.join(missing_deps)}")
        print()

    # Display configuration
    print("⚙️ Configuración del sistema:")
    print(f"   Supervisor: {Settings.SUPERVISOR_NAME}")
    print(f"   Email: {Settings.SUPERVISOR_EMAIL}")
    print(f"   Workspace: {Settings.PROJECT_ROOT}")
    print(f"   Extensiones monitoreadas: {len(Settings.MONITORED_EXTENSIONS)}")
    print()

    print("=" * 70)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 70)
    print()
    print("Para ejecutar la simulación:")
    print("   python scripts/run_simulation.py")
    print()


if __name__ == "__main__":
    setup_environment()

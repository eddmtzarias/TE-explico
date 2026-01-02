"""
Demo script para capturar el estado del sistema OmniMaestro
Genera un reporte visual del estado de la configuración
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from omnimastro.shared import config as cfg
from omnimastro.shared.config import config


def print_banner():
    """Imprime banner del sistema"""
    print("\n" + "="*70)
    print("   🎓 OMNIMAESTRO - SISTEMA DE ASISTENCIA EDUCATIVA")
    print("="*70)


def print_system_status():
    """Imprime estado detallado del sistema"""
    print("\n📊 ESTADO DEL SISTEMA")
    print("-" * 70)
    
    # Proveedores de IA
    providers = config.get_configured_ai_providers()
    print("\n🤖 MOTORES DE IA:")
    if providers:
        for provider in providers:
            print(f"   ✅ {provider.upper()} - Configurado y listo")
    else:
        print("   ⚠️  Ningún proveedor configurado")
        print("   💡 Configura OPENAI_API_KEY o ANTHROPIC_API_KEY en .env")
    
    # OCR
    print("\n📷 MOTOR OCR:")
    print(f"   Engine: {cfg.OCR_ENGINE}")
    print(f"   Idiomas: {', '.join(cfg.OCR_LANGUAGES)}")
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"   ✅ Tesseract v{version} - Disponible")
    except:
        print("   ⚠️  Tesseract no instalado/configurado")
    
    # Database
    print("\n💾 BASE DE DATOS:")
    print(f"   URL: {cfg.DATABASE_URL}")
    db_path = Path(str(cfg.DATA_DIR)) / "omnimaestro.db"
    if db_path.exists():
        size = db_path.stat().st_size / 1024
        print(f"   ✅ Archivo: {size:.2f} KB")
    else:
        print(f"   📝 Archivo: Se creará en primer uso")
    
    # Recursos
    print("\n⚡ LÍMITES DE RECURSOS:")
    print(f"   RAM máxima: {cfg.MAX_RAM_GB} GB")
    print(f"   CPU máxima: {cfg.MAX_CPU_PERCENT}%")
    print(f"   Tareas concurrentes: {cfg.MAX_CONCURRENT_TASKS}")
    
    # UI
    print("\n🖥️  INTERFAZ DESKTOP:")
    print(f"   Framework: Flet")
    print(f"   Tema: {cfg.UI_THEME}")
    print(f"   Dimensiones: {cfg.UI_WIDTH}x{cfg.UI_HEIGHT}px")
    
    # Directorios
    print("\n📁 DIRECTORIOS:")
    dirs = [
        ("Datos", cfg.DATA_DIR),
        ("Logs", cfg.LOGS_DIR),
        ("Temporal", cfg.TEMP_DIR),
        ("Cache", cfg.CACHE_DIR),
        ("Screenshots", cfg.SCREENSHOTS_DIR),
    ]
    for name, path in dirs:
        exists = "✅" if path.exists() else "❌"
        print(f"   {exists} {name}: {path.name}/")


def print_validation():
    """Imprime validación de configuración"""
    print("\n" + "="*70)
    print("🔍 VALIDACIÓN DE CONFIGURACIÓN")
    print("="*70)
    
    issues = config.validate()
    
    if not issues['errors'] and not issues['warnings']:
        print("\n✅ CONFIGURACIÓN PERFECTA")
        print("   Todos los sistemas operativos")
    else:
        if issues['errors']:
            print(f"\n❌ ERRORES CRÍTICOS ({len(issues['errors'])}):")
            for i, error in enumerate(issues['errors'], 1):
                print(f"   {i}. {error}")
        
        if issues['warnings']:
            print(f"\n⚠️  ADVERTENCIAS ({len(issues['warnings'])}):")
            for i, warning in enumerate(issues['warnings'], 1):
                print(f"   {i}. {warning}")


def print_next_steps():
    """Imprime próximos pasos"""
    print("\n" + "="*70)
    print("🚀 CÓMO USAR OMNIMAESTRO")
    print("="*70)
    
    providers = config.get_configured_ai_providers()
    
    if providers:
        print("\n✅ Sistema listo para usar:")
        print("   python omnimastro/desktop/main.py")
        print("\n📝 Funcionalidades disponibles:")
        print("   • Explicaciones educativas con IA")
        print("   • Niveles adaptativos (Principiante/Intermedio/Avanzado)")
        print("   • Interfaz gráfica intuitiva")
    else:
        print("\n⚠️  Configuración incompleta:")
        print("   1. Edita el archivo .env")
        print("   2. Completa al menos una API key:")
        print("      - OPENAI_API_KEY=sk-...")
        print("      - o ANTHROPIC_API_KEY=sk-ant-...")
        print("   3. Guarda el archivo")
        print("   4. Ejecuta: python omnimastro/desktop/main.py")


def print_footer():
    """Imprime footer con información del proyecto"""
    print("\n" + "="*70)
    print("   Versión: 0.2.0 | Progreso: 20% | MVP Funcional")
    print("   Documentación: SETUP_README.md")
    print("="*70 + "\n")


def main():
    """Función principal"""
    print_banner()
    print_system_status()
    print_validation()
    print_next_steps()
    print_footer()


if __name__ == "__main__":
    main()

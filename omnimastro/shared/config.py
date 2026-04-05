"""
Configuración Global de OmniMaestro (Enhanced)
Gestiona la configuración del sistema con validación completa
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Cargar variables de entorno desde .env
load_dotenv()

# Directorios base
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / os.getenv("DATA_DIR", "data")
LOGS_DIR = PROJECT_ROOT / os.getenv("LOG_DIR", "logs")
TEMP_DIR = PROJECT_ROOT / os.getenv("TEMP_DIR", "temp")
CACHE_DIR = PROJECT_ROOT / os.getenv("CACHE_DIR", ".cache")
DESIGNS_DIR = PROJECT_ROOT / os.getenv("DESIGN_DIR", "designs")
SCREENSHOTS_DIR = PROJECT_ROOT / os.getenv("SCREENSHOTS_DIR", "screenshots")

# Crear directorios si no existen
for directory in [DATA_DIR, LOGS_DIR, TEMP_DIR, CACHE_DIR, DESIGNS_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# === Configuración de IA ===
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # "openai" o "anthropic"
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2000"))

# === Configuración de OCR ===
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "tesseract")
OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")
OCR_LANGUAGES = os.getenv("OCR_LANGUAGES", "eng,spa").split(",")

# === Recursos del Sistema ===
MAX_RAM_GB = float(os.getenv("MAX_RAM_GB", "6.5"))
MAX_CPU_PERCENT = int(os.getenv("MAX_CPU_PERCENT", "80"))
MAX_CONCURRENT_TASKS = int(os.getenv("MAX_CONCURRENT_TASKS", "2"))

# === Database ===
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'omnimaestro.db'}")

# === UI Desktop ===
UI_THEME = os.getenv("UI_THEME", "dark")
UI_WIDTH = int(os.getenv("UI_WIDTH", "450"))
UI_HEIGHT = int(os.getenv("UI_HEIGHT", "700"))

# === Logging ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# === Plataforma ===
CURRENT_PLATFORM = os.getenv("OMNIMASTRO_PLATFORM", "desktop")


class Config:
    """Clase de configuración con validación"""
    
    @staticmethod
    def is_api_key_configured(service: str) -> bool:
        """Verifica si una API key está configurada"""
        if service.lower() == "openai":
            return bool(OPENAI_API_KEY and OPENAI_API_KEY != "")
        elif service.lower() == "anthropic":
            return bool(ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "")
        return False
    
    @staticmethod
    def get_configured_ai_providers() -> List[str]:
        """Retorna lista de proveedores de IA configurados"""
        providers = []
        if Config.is_api_key_configured("openai"):
            providers.append("openai")
        if Config.is_api_key_configured("anthropic"):
            providers.append("anthropic")
        return providers
    
    @staticmethod
    def validate() -> Dict[str, List[str]]:
        """
        Valida la configuración completa
        
        Returns:
            Dict con 'warnings' y 'errors'
        """
        issues = {'warnings': [], 'errors': []}
        
        # Validar API keys
        providers = Config.get_configured_ai_providers()
        if not providers:
            issues['warnings'].append(
                "No hay API keys de IA configuradas. "
                "La funcionalidad de explicaciones no estará disponible."
            )
        
        # Validar directorios
        for name, path in [
            ("DATA_DIR", DATA_DIR),
            ("LOGS_DIR", LOGS_DIR),
            ("TEMP_DIR", TEMP_DIR),
        ]:
            if not path.exists():
                issues['errors'].append(f"Directorio {name} no existe: {path}")
        
        # Validar OCR
        if OCR_ENGINE == "tesseract":
            try:
                import pytesseract
                pytesseract.get_tesseract_version()
            except Exception as e:
                issues['warnings'].append(
                    f"Tesseract OCR no está disponible: {e}. "
                    "Instala desde: https://github.com/tesseract-ocr/tesseract"
                )
        
        return issues
    
    @staticmethod
    def print_status():
        """Imprime el estado de la configuración"""
        print("\n" + "="*60)
        print("⚙️  CONFIGURACIÓN DE OMNIMAESTRO")
        print("="*60)
        
        # IA Providers
        providers = Config.get_configured_ai_providers()
        print(f"\n🤖 Proveedores de IA:")
        if providers:
            for provider in providers:
                print(f"   ✅ {provider.upper()}")
        else:
            print("   ❌ Ninguno configurado")
        
        # OCR
        print(f"\n📷 OCR Engine: {OCR_ENGINE}")
        print(f"   Idiomas: {', '.join(OCR_LANGUAGES)}")
        
        # Database
        print(f"\n💾 Database: {DATABASE_URL}")
        
        # Recursos
        print(f"\n⚡ Límites de recursos:")
        print(f"   RAM máxima: {MAX_RAM_GB} GB")
        print(f"   CPU máxima: {MAX_CPU_PERCENT}%")
        
        # Validación
        issues = Config.validate()
        if issues['errors']:
            print(f"\n❌ Errores ({len(issues['errors'])}):")
            for error in issues['errors']:
                print(f"   • {error}")
        
        if issues['warnings']:
            print(f"\n⚠️  Advertencias ({len(issues['warnings'])}):")
            for warning in issues['warnings']:
                print(f"   • {warning}")
        
        if not issues['errors'] and not issues['warnings']:
            print("\n✅ Configuración válida")
        
        print("\n" + "="*60 + "\n")


# Instancia global
config = Config()


def get_config_value(key: str, default=None):
    """Obtiene un valor de configuración con fallback"""
    return os.getenv(key, default)

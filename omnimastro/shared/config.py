"""
Configuración Global de OmniMaestro

Gestiona la configuración del sistema cargando variables de entorno
y proporcionando valores por defecto.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Directorios base
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
DESIGNS_DIR = PROJECT_ROOT / "designs"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"

# Crear directorios si no existen
for directory in [DATA_DIR, LOGS_DIR, DESIGNS_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(exist_ok=True)

# Configuración de API Keys (desde .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Configuración de OCR
OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")  # tesseract o easyocr
OCR_LANGUAGES = os.getenv("OCR_LANGUAGES", "eng,spa").split(",")

# Configuración de IA
AI_MODEL = os.getenv("AI_MODEL", "gpt-4")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2000"))

# Configuración de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Plataforma actual
CURRENT_PLATFORM = os.getenv("OMNIMASTRO_PLATFORM", "desktop")

def get_config_value(key: str, default=None):
    """Obtiene un valor de configuración con fallback."""
    return os.getenv(key, default)

def is_api_key_configured(service: str) -> bool:
    """Verifica si una API key está configurada."""
    if service.lower() == "openai":
        return bool(OPENAI_API_KEY)
    elif service.lower() == "anthropic":
        return bool(ANTHROPIC_API_KEY)
    return False
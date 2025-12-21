"""
OmniMaestro - Sistema de IA Pedagógica Multiplataforma

Sistema inteligente que analiza capturas de pantalla y proporciona
explicaciones adaptativas a través de múltiples plataformas:
- Desktop (Windows, macOS, Linux) vía Tauri
- Mobile (Android) vía Flutter  
- Web (PWA) vía React/Next.js

Integra:
- Procesamiento de imágenes con OCR
- IA conversacional para explicaciones adaptativas
- Guía inteligente de desarrollo paso a paso
"""

__version__ = "0.1.0"
__author__ = "TOKRAGGCORP-System"
__license__ = "MIT"

# Metadata del proyecto
PROJECT_NAME = "OmniMaestro"
PROJECT_DESCRIPTION = "Sistema de IA pedagógica multiplataforma"

# Plataformas soportadas
SUPPORTED_PLATFORMS = {
    "desktop": {
        "framework": "Tauri",
        "os": ["Windows", "macOS", "Linux"],
        "status": "in_development"
    },
    "mobile": {
        "framework": "Flutter",
        "os": ["Android"],
        "status": "planned"
    },
    "web": {
        "framework": "PWA",
        "deployment": ["Vercel", "Netlify"],
        "status": "planned"
    }
}

# Configuración de características
FEATURES = {
    "screenshot_capture": True,
    "ocr_processing": True,
    "ai_explanations": True,
    "adaptive_learning": True,
    "offline_mode": False,  # Próximamente
}

def get_version():
    """Retorna la versión actual del proyecto."""
    return __version__

def get_platform_info(platform: str) -> dict:
    """
    Retorna información sobre una plataforma específica.
    
    Args:
        platform (str): Nombre de la plataforma ('desktop', 'mobile', 'web')
    
    Returns:
        dict: Información de la plataforma o None si no existe
    """
    return SUPPORTED_PLATFORMS.get(platform.lower())

def is_feature_enabled(feature: str) -> bool:
    """
    Verifica si una característica está habilitada.
    
    Args:
        feature (str): Nombre de la característica
    
    Returns:
        bool: True si está habilitada, False en caso contrario
    """
    return FEATURES.get(feature, False)

# Exportaciones principales (se agregarán cuando existan los módulos)
__all__ = [
    "__version__",
    "PROJECT_NAME",
    "PROJECT_DESCRIPTION",
    "get_version",
    "get_platform_info",
    "is_feature_enabled",
]
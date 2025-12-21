"""
Sistema de Logging de OmniMaestro

Proporciona logging configurado para todo el proyecto con:
- Salida a archivo y consola
- Rotación de logs
- Niveles configurables
- Formato consistente
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .config import LOGS_DIR, LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Configura y retorna un logger.
    
    Args:
        name (str): Nombre del logger (generalmente __name__)
        log_file (str): Nombre del archivo de log (opcional)
    
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Nivel de log
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Formato
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo (con rotación)
    if log_file:
        log_path = LOGS_DIR / log_file
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Logger principal del proyecto
main_logger = setup_logger("omnimastro", "omnimastro.log")

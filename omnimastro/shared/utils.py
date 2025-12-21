"""
Utilidades Compartidas de OmniMaestro

Funciones de utilidad usadas en todo el proyecto.
"""

import hashlib
from pathlib import Path
from typing import Union

def calculate_file_hash(file_path: Union[str, Path], algorithm: str = "sha256") -> str:
    """
    Calcula el hash de un archivo.
    
    Args:
        file_path: Ruta al archivo
        algorithm: Algoritmo de hash (sha256, md5, etc.)
    
    Returns:
        str: Hash hexadecimal del archivo
    """
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Asegura que un directorio existe, creándolo si es necesario.
    
    Args:
        path: Ruta al directorio
    
    Returns:
        Path: Objeto Path del directorio
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Trunca un string a una longitud máxima.
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        suffix: Sufijo a agregar si se trunca
    
    Returns:
        str: Texto truncado
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def format_bytes(bytes_value: int) -> str:
    """
    Formatea bytes a una representación legible.
    
    Args:
        bytes_value: Cantidad de bytes
    
    Returns:
        str: Representación formateada (ej: "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"
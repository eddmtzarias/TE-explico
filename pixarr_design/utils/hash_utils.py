"""
Utility functions for calculating file hashes.
"""

import hashlib
from pathlib import Path


def calculate_file_hash(file_path, algorithm="sha256"):
    """
    Calculate the hash of a file.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (default: sha256)
        
    Returns:
        Hexadecimal hash string
    """
    path = Path(file_path)
    hash_obj = hashlib.new(algorithm)
    
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

"""
Utility functions for managing file metadata.
"""

import json
from pathlib import Path
from datetime import datetime
from pixarr_design.config.settings import Settings


def get_metadata_path(file_path):
    """
    Get the metadata file path for a given design file.
    
    Args:
        file_path: Path to the design file
        
    Returns:
        Path to the metadata JSON file
    """
    file_path = Path(file_path)
    relative_path = file_path.relative_to(Settings.BASE_DIR)
    metadata_name = f"{relative_path.as_posix().replace('/', '_')}.json"
    return Settings.METADATA_DIR / metadata_name


def validate_metadata(file_path):
    """
    Read and validate metadata for a file.
    
    Args:
        file_path: Path to the design file
        
    Returns:
        Metadata dict if valid, None otherwise
    """
    metadata_path = get_metadata_path(file_path)
    
    if not metadata_path.exists():
        return None
    
    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        return metadata
    except (json.JSONDecodeError, IOError):
        return None


def inject_metadata(file_path, metadata):
    """
    Write metadata for a file.
    
    Args:
        file_path: Path to the design file
        metadata: Metadata dictionary to write
    """
    metadata_path = get_metadata_path(file_path)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

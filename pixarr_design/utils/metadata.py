"""
Metadata injection and validation utilities for design files.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image
from PIL.PngImagePlugin import PngInfo


def inject_metadata(file_path: str, metadata: Dict[str, Any]) -> None:
    """
    Inject metadata into a file.

    For PNG files, metadata is embedded directly into the image.
    For other files, a separate .meta JSON file is created.

    Args:
        file_path: Path to the target file
        metadata: Dictionary containing metadata to inject

    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Handle PNG files with embedded metadata
    if path.suffix.lower() == ".png":
        _inject_png_metadata(path, metadata)
    else:
        _inject_meta_file(path, metadata)


def _inject_png_metadata(path: Path, metadata: Dict[str, Any]) -> None:
    """
    Inject metadata into a PNG file.

    Args:
        path: Path to the PNG file
        metadata: Metadata dictionary
    """
    # Load the existing image
    img = Image.open(path)

    # Create PngInfo object
    png_info = PngInfo()

    # Add metadata as JSON in a custom chunk
    metadata_json = json.dumps(metadata, indent=2)
    png_info.add_text("PixARR_Metadata", metadata_json)

    # Save with metadata
    img.save(path, pnginfo=png_info)


def _inject_meta_file(path: Path, metadata: Dict[str, Any]) -> None:
    """
    Create a separate .meta file with metadata.

    Args:
        path: Path to the target file
        metadata: Metadata dictionary
    """
    meta_path = path.with_suffix(path.suffix + ".meta")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def validate_metadata(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Validate and extract metadata from a file.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary containing metadata if found, None otherwise
    """
    path = Path(file_path)
    if not path.exists():
        return None

    # Handle PNG files
    if path.suffix.lower() == ".png":
        return _extract_png_metadata(path)
    else:
        return _extract_meta_file(path)


def _extract_png_metadata(path: Path) -> Optional[Dict[str, Any]]:
    """
    Extract metadata from a PNG file.

    Args:
        path: Path to the PNG file

    Returns:
        Metadata dictionary if found, None otherwise
    """
    try:
        img = Image.open(path)
        if "PixARR_Metadata" in img.info:
            return json.loads(img.info["PixARR_Metadata"])
    except (json.JSONDecodeError, KeyError, Exception):
        pass

    return None


def _extract_meta_file(path: Path) -> Optional[Dict[str, Any]]:
    """
    Extract metadata from a .meta file.

    Args:
        path: Path to the target file

    Returns:
        Metadata dictionary if found, None otherwise
    """
    meta_path = path.with_suffix(path.suffix + ".meta")
    if not meta_path.exists():
        return None

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None

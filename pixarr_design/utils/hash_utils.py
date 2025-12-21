"""
Hash utility functions for file integrity verification.
"""

import hashlib
from pathlib import Path
from typing import Optional


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Calculate the hash of a file using the specified algorithm.

    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        Hexadecimal hash string

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the algorithm is not supported
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        hash_obj = hashlib.new(algorithm)
    except ValueError as e:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}") from e

    # Read file in blocks for memory efficiency
    block_size = 8192  # 8KB blocks
    with open(path, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            hash_obj.update(data)

    return hash_obj.hexdigest()


def verify_file_integrity(file_path: str, expected_hash: str, algorithm: str = "sha256") -> bool:
    """
    Verify the integrity of a file by comparing its hash with an expected value.

    Args:
        file_path: Path to the file
        expected_hash: Expected hash value
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        True if hashes match, False otherwise
    """
    try:
        actual_hash = calculate_file_hash(file_path, algorithm)
        return actual_hash == expected_hash
    except (FileNotFoundError, ValueError):
        return False


def calculate_string_hash(content: str, algorithm: str = "sha256") -> str:
    """
    Calculate the hash of a string.

    Args:
        content: String content to hash
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        Hexadecimal hash string

    Raises:
        ValueError: If the algorithm is not supported
    """
    try:
        hash_obj = hashlib.new(algorithm)
    except ValueError as e:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}") from e

    hash_obj.update(content.encode("utf-8"))
    return hash_obj.hexdigest()

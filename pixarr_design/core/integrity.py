"""
Integrity validation for design artifacts.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from ..utils.hash_utils import calculate_file_hash, verify_file_integrity
from ..utils.metadata import validate_metadata
from ..config.settings import Settings


class IntegrityValidator:
    """Validator for file integrity and metadata verification."""

    def __init__(self):
        """Initialize the integrity validator."""
        self.validation_results: List[Dict[str, Any]] = []

    def verify_file(self, file_path: str) -> Dict[str, Any]:
        """
        Verify the integrity of a single file.

        Args:
            file_path: Path to the file to verify

        Returns:
            Dictionary containing verification results
        """
        path = Path(file_path)

        if not path.exists():
            return {
                "filename": path.name,
                "status": "ERROR",
                "message": "File not found",
                "valid": False,
            }

        # Calculate current hash
        try:
            current_hash = calculate_file_hash(str(path))
        except Exception as e:
            return {
                "filename": path.name,
                "status": "ERROR",
                "message": f"Failed to calculate hash: {str(e)}",
                "valid": False,
            }

        # Validate metadata
        metadata = validate_metadata(str(path))

        result = {
            "filename": path.name,
            "path": str(path),
            "current_hash": current_hash,
            "has_metadata": metadata is not None,
        }

        if metadata:
            # Compare with stored hash
            stored_hash = metadata.get("hash", "")
            if stored_hash and stored_hash != current_hash:
                result.update(
                    {
                        "status": "MODIFIED",
                        "message": "File hash does not match stored hash",
                        "stored_hash": stored_hash,
                        "valid": False,
                    }
                )
            else:
                result.update(
                    {
                        "status": "OK",
                        "message": "File integrity verified",
                        "stored_hash": stored_hash,
                        "valid": True,
                        "metadata": metadata,
                    }
                )
        else:
            result.update(
                {
                    "status": "NO_METADATA",
                    "message": "No metadata found for verification",
                    "valid": True,  # Not invalid, just untracked
                }
            )

        self.validation_results.append(result)
        return result

    def verify_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Verify all monitored files in a directory.

        Args:
            directory_path: Path to the directory

        Returns:
            List of verification results for all files
        """
        results = []
        dir_path = Path(directory_path)

        if not dir_path.exists() or not dir_path.is_dir():
            return results

        # Find all monitored files
        for file_path in dir_path.rglob("*"):
            if file_path.is_file() and Settings.is_monitored_file(file_path.name):
                # Skip .meta files
                if file_path.suffix == ".meta":
                    continue
                result = self.verify_file(str(file_path))
                results.append(result)

        return results

    def get_anomalies(self) -> List[Dict[str, Any]]:
        """
        Get all files with integrity issues.

        Returns:
            List of files that failed validation
        """
        return [
            result
            for result in self.validation_results
            if not result.get("valid", False) and result.get("status") != "NO_METADATA"
        ]

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation results.

        Returns:
            Dictionary containing validation statistics
        """
        total = len(self.validation_results)
        valid = sum(1 for r in self.validation_results if r.get("valid", False))
        anomalies = len(self.get_anomalies())
        no_metadata = sum(
            1 for r in self.validation_results if r.get("status") == "NO_METADATA"
        )

        return {
            "total_files": total,
            "valid_files": valid,
            "anomalies": anomalies,
            "no_metadata": no_metadata,
        }

    def clear_results(self) -> None:
        """Clear validation results."""
        self.validation_results.clear()

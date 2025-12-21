"""
Integrity audit system for PixARR Design files.
"""

from pathlib import Path
from pixarr_design.config.settings import Settings
from pixarr_design.utils.hash_utils import calculate_file_hash
from pixarr_design.utils.metadata import validate_metadata


class IntegrityAuditor:
    """Auditor for checking file integrity."""
    
    def __init__(self):
        self.results = []
    
    def audit_file(self, file_path):
        """
        Audit a single file for integrity.
        
        Args:
            file_path: Path to the file to audit
            
        Returns:
            Dictionary with audit result
        """
        file_path = Path(file_path)
        filename = file_path.name
        
        # Check if file exists
        if not file_path.exists():
            return {
                "filename": filename,
                "path": str(file_path),
                "status": "ERROR",  # Line 34 reference in problem statement
                "message": "File not found",
                "valid": False
            }
        
        # Try to read metadata
        try:
            metadata = validate_metadata(file_path)
        except Exception as e:
            return {
                "filename": filename,
                "path": str(file_path),
                "status": "ERROR",
                "message": f"Error reading metadata: {str(e)}",
                "valid": False
            }
        
        # Check if metadata exists
        if metadata is None:
            return {
                "filename": filename,
                "path": str(file_path),
                "status": "NO_METADATA",
                "message": "No metadata found",
                "valid": True  # NO_METADATA files are still valid (line 131)
            }
        
        # Calculate current hash
        try:
            current_hash = calculate_file_hash(file_path)
        except Exception as e:
            return {
                "filename": filename,
                "path": str(file_path),
                "status": "ERROR",
                "message": f"Error calculating hash: {str(e)}",
                "valid": False
            }
        
        # Compare hashes
        stored_hash = metadata.get("hash", "")
        
        if current_hash != stored_hash:
            return {
                "filename": filename,
                "path": str(file_path),
                "status": "MODIFIED",  # Line 66 reference in problem statement
                "message": "File hash does not match stored metadata",
                "stored_hash": stored_hash,
                "current_hash": current_hash,
                "valid": False  # Line 69 reference in problem statement
            }
        
        # File is valid
        return {
            "filename": filename,
            "path": str(file_path),
            "status": "OK",
            "message": "File integrity verified",
            "valid": True
        }
    
    def audit_all(self):
        """
        Audit all monitored files.
        
        Returns:
            Dictionary with audit results and summary
        """
        results = []
        
        # Find all monitored files
        if Settings.DESIGN_DIR.exists():
            for ext in Settings.MONITORED_EXTENSIONS:
                for file_path in Settings.DESIGN_DIR.rglob(f"*{ext}"):
                    result = self.audit_file(file_path)
                    results.append(result)
        
        # Calculate summary
        total_files = len(results)
        anomalies = []
        
        for result in results:
            # Anomalies are files with ERROR or MODIFIED status
            # NO_METADATA does NOT count as anomaly (line 131)
            if result["status"] in ["ERROR", "MODIFIED"]:
                anomalies.append(result)
        
        return {
            "results": results,
            "anomalies": anomalies,
            "summary": {
                "total_files": total_files,
                "valid_files": sum(1 for r in results if r["valid"]),
                "anomalies": len(anomalies)
            }
        }

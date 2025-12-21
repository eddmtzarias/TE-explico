#!/usr/bin/env python3
"""
Test script to create test files with metadata to simulate integrity issues.
"""

from pixarr_design.config.settings import Settings
from pixarr_design.utils.hash_utils import calculate_file_hash
from pixarr_design.utils.metadata import inject_metadata
from pathlib import Path
from datetime import datetime, timezone

def setup_test_data():
    """Create test design files with metadata."""
    Settings.ensure_directories()
    
    # Create test files
    designs_dir = Settings.DESIGN_DIR
    
    # File 1: Logo with metadata (will be modified later)
    logo_path = designs_dir / "test_logo.svg"
    with open(logo_path, "w") as f:
        f.write('''<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="#007bff"/>
</svg>''')
    
    # Create metadata with correct hash first
    logo_hash = calculate_file_hash(logo_path)
    logo_metadata = {
        "filename": "test_logo.svg",
        "hash": logo_hash,
        "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "created_by": "TestUser",
        "version": 1,
        "project": "TestProject"
    }
    inject_metadata(logo_path, logo_metadata)
    print(f"✅ Created metadata for {logo_path.name}")
    
    # File 2: Icon without metadata (to test NO_METADATA status)
    icon_path = designs_dir / "test_icon.svg"
    with open(icon_path, "w") as f:
        f.write('''<svg width="50" height="50" xmlns="http://www.w3.org/2000/svg">
  <rect width="50" height="50" fill="#28a745"/>
</svg>''')
    print(f"✅ Created {icon_path.name} (without metadata)")
    
    # File 3: Banner with metadata (will remain unchanged)
    banner_path = designs_dir / "test_banner.png"
    with open(banner_path, "wb") as f:
        # Create a minimal PNG file
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    
    banner_hash = calculate_file_hash(banner_path)
    banner_metadata = {
        "filename": "test_banner.png",
        "hash": banner_hash,
        "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "created_by": "TestUser",
        "version": 1,
        "project": "TestProject"
    }
    inject_metadata(banner_path, banner_metadata)
    print(f"✅ Created metadata for {banner_path.name}")
    
    print("\n📝 Now simulating integrity issues...")
    
    # Modify the logo file to create a hash mismatch (simulate external modification)
    with open(logo_path, "w") as f:
        f.write('''<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="#ff0000"/>
</svg>''')
    print(f"⚠️ Modified {logo_path.name} (hash mismatch will be detected)")
    
    print("\n✅ Test data setup complete!")
    print(f"\nFiles created:")
    print(f"  - {logo_path.name}: Has metadata, but file was modified (ANOMALY)")
    print(f"  - {icon_path.name}: No metadata (NO_METADATA, not an anomaly)")
    print(f"  - {banner_path.name}: Has metadata, unchanged (OK)")

if __name__ == "__main__":
    setup_test_data()

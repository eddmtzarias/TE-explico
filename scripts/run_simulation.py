#!/usr/bin/env python3
"""
Complete simulation script for PixARR Design system.
Executes all 6 steps of the emulator test.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PIL import Image, ImageDraw, ImageFont
from pixarr_design.core.agent import PixARRAgent
from pixarr_design.config.settings import Settings


def create_sample_image(filename: str, text: str, color: str = "blue") -> str:
    """
    Create a sample PNG image with text.

    Args:
        filename: Name for the image file
        text: Text to display on the image
        color: Background color

    Returns:
        Path to the created image
    """
    # Create image
    img = Image.new("RGB", (400, 300), color=color)
    draw = ImageDraw.Draw(img)

    # Add text
    try:
        # Try to use a default font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    # Draw text
    text_lines = text.split("\n")
    y_position = 100
    for line in text_lines:
        # Get text bounding box
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x_position = (400 - text_width) // 2
        draw.text((x_position, y_position), line, fill="white", font=font)
        y_position += text_height + 10

    # Save image
    image_path = Settings.ACTIVE_DIR / filename
    img.save(image_path)

    return str(image_path)


def print_step_header(step_num: int, title: str) -> None:
    """Print a formatted step header."""
    print()
    print(f"📌 PASO {step_num}: {title}")
    print("-" * 70)


def run_simulation() -> None:
    """Execute the complete PixARR Design simulation."""
    print("=" * 70)
    print("🚀 INICIANDO SIMULACIÓN COMPLETA - PIXARR DESIGN EMULATOR")
    print("=" * 70)

    # Ensure directories exist
    Settings.ensure_directories()

    # STEP 1: Agent Configuration
    print_step_header(1, "Configuración del Agente")
    agent = PixARRAgent()
    agent.activate()

    # STEP 2: Create Visual Artifact
    print_step_header(2, "Generación de Artefacto Visual")
    
    # Create first image
    print("   🎨 Imagen creada: logo_emulador.png")
    logo_path = create_sample_image(
        "logo_emulador.png",
        "PixARR Design\nEmulator v1.0",
        color="darkblue"
    )
    
    artifact_info = agent.create_artifact(logo_path, "PixARR Design")

    # STEP 3: Editing and Changes
    print_step_header(3, "Edición y Cambios")
    
    # Create modified version
    print("   🎨 Imagen creada: logo_emulador_v2.png")
    logo_v2_path = create_sample_image(
        "logo_emulador_v2.png",
        "PixARR Design\nEmulator v2.0\n⭐ Actualizado",
        color="navy"
    )
    
    modification_info = agent.modify_artifact(
        logo_v2_path,
        "PixARR Design",
        "Añadir estrella y actualizar versión"
    )

    # STEP 4: Integrity Audit
    print_step_header(4, "Auditoría de Integridad")
    audit_results = agent.audit_integrity()

    # STEP 5: Incident Detection (Simulated)
    print_step_header(5, "Detección de Incidentes (Simulada)")
    
    # Simulate unauthorized access
    agent.detect_unauthorized_access(logo_v2_path, "sim_agenteX")

    # STEP 6: Documentation and Closure
    print_step_header(6, "Documentación y Cierre")
    report_path = agent.generate_report()

    # Final Summary
    print()
    print("=" * 70)
    print("✅ SIMULACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print()
    print(f"📄 Reporte generado: {report_path}")
    print(f"📊 Logs disponibles en: {Settings.LOGS_DIR}")
    print(f"🔒 Archivos en cuarentena: {Settings.QUARANTINE_DIR}")
    print(f"📧 Supervisor notificado: {Settings.SUPERVISOR_EMAIL}")
    print("=" * 70)
    print()

    # Statistics
    audit_history = agent.logger.get_audit_history()
    incident_history = agent.logger.get_incident_history()
    
    artifacts = [e for e in audit_history if e.get("type") == "artifact_created"]
    
    print("📈 ESTADÍSTICAS FINALES:")
    print(f"   - Artefactos monitoreados: {len(artifacts)}")
    print(f"   - Incidentes detectados: {len(incident_history)}")
    print(f"   - Archivos en cuarentena: {len(incident_history)}")
    print(f"   - Auditorías realizadas: 1")
    print()
    print("✅ Script ejecutado correctamente")
    print()


if __name__ == "__main__":
    try:
        run_simulation()
    except Exception as e:
        print(f"\n❌ Error durante la simulación: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

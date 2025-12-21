#!/usr/bin/env python3
"""
Script para corregir anomalías de integridad en archivos de diseño.
Actualiza los metadatos de archivos que fueron modificados fuera del sistema PixARR.
"""

from pixarr_design.core.agent import PixARRAgent
from pixarr_design.config.settings import Settings
from pixarr_design.utils.hash_utils import calculate_file_hash
from pixarr_design.utils.metadata import inject_metadata, validate_metadata
from pathlib import Path
from datetime import datetime, timezone


def main():
    # Configurar entorno
    Settings.ensure_directories()
    
    # Activar agente
    agent = PixARRAgent()
    agent.activate()
    
    print("\n🔍 Ejecutando auditoría inicial...")
    results = agent.audit_integrity()
    anomalies = results['anomalies']
    
    if not anomalies:
        print("✅ No se detectaron anomalías")
        return 0
    
    print(f"\n⚠️ Se detectaron {len(anomalies)} anomalías")
    print("\n📝 Detalles de las anomalías:")
    
    for i, anomaly in enumerate(anomalies, 1):
        print(f"\n{i}. {anomaly['filename']}")
        print(f"   Status: {anomaly['status']}")
        print(f"   Mensaje: {anomaly['message']}")
        print(f"   Path: {anomaly.get('path', 'N/A')}")
    
    print("\n🔧 Corrigiendo anomalías...")
    
    fixed_count = 0
    error_count = 0
    
    for anomaly in anomalies:
        file_path = anomaly.get('path')
        filename = anomaly['filename']
        status = anomaly['status']
        
        if status == "MODIFIED":
            # Archivo modificado - actualizar metadatos
            try:
                path = Path(file_path)
                if not path.exists():
                    print(f"   ❌ {filename}: Archivo no encontrado")
                    error_count += 1
                    continue
                
                # Obtener metadatos existentes
                old_metadata = validate_metadata(file_path)
                if not old_metadata:
                    print(f"   ❌ {filename}: No se pudieron leer metadatos")
                    error_count += 1
                    continue
                
                # Calcular nuevo hash
                new_hash = calculate_file_hash(file_path)
                
                # Actualizar metadatos
                updated_metadata = {
                    **old_metadata,
                    "hash": new_hash,
                    "last_modified_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                    "last_modified_by": Settings.SUPERVISOR_NAME,
                    "modification_description": "Corrección automática de integridad",
                    "previous_hash": anomaly.get('stored_hash', old_metadata.get('hash', '')),
                    "version": old_metadata.get("version", 1) + 1,
                }
                
                inject_metadata(file_path, updated_metadata)
                print(f"   ✅ {filename}: Metadatos actualizados (v{updated_metadata['version']})")
                fixed_count += 1
                
            except Exception as e:
                print(f"   ❌ {filename}: Error al corregir - {str(e)}")
                error_count += 1
                
        elif status == "ERROR":
            print(f"   ❌ {filename}: Error de archivo - {anomaly['message']}")
            error_count += 1
    
    print(f"\n📊 Resumen de correcciones:")
    print(f"   ✅ Archivos corregidos: {fixed_count}")
    print(f"   ❌ Errores: {error_count}")
    
    # Ejecutar auditoría final
    print("\n🔍 Ejecutando auditoría final...")
    final_results = agent.audit_integrity()
    final_anomalies = final_results['summary']['anomalies']
    
    if final_anomalies == 0:
        print("✅ ¡Todas las anomalías fueron corregidas!")
        print(f"   Archivos verificados: {final_results['summary']['total_files']}")
        return 0
    else:
        print(f"⚠️ Aún quedan {final_anomalies} anomalías sin resolver")
        return 1


if __name__ == "__main__":
    exit(main())

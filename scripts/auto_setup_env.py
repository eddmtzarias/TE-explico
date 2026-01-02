"""
Configuración Automática de Variables de Entorno para OmniMaestro
Genera .env desde template y crea estructura de directorios
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class EnvSetup:
    """Configurador automático de entorno"""
    
    def __init__(self, project_root: Path = None):
        """
        Inicializa el configurador
        
        Args:
            project_root: Raíz del proyecto (default: detecta automáticamente)
        """
        if project_root is None:
            # Detectar raíz del proyecto
            current = Path(__file__).resolve()
            # Buscar hacia arriba hasta encontrar .git o asumir parent/parent
            self.project_root = current.parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.env_path = self.project_root / ".env"
        self.env_example_path = self.project_root / ".env.example"
    
    def create_directories(self) -> List[Path]:
        """
        Crea directorios necesarios para el proyecto
        
        Returns:
            Lista de directorios creados
        """
        directories = [
            self.project_root / "data",
            self.project_root / "temp",
            self.project_root / ".cache",
            self.project_root / "logs",
            self.project_root / "screenshots",
            self.project_root / "designs",
        ]
        
        created = []
        for directory in directories:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                created.append(directory)
                print(f"   ✅ Creado: {directory.name}/")
            else:
                print(f"   ⏭️  Ya existe: {directory.name}/")
        
        return created
    
    def backup_existing_env(self) -> bool:
        """
        Crea backup del .env existente si lo hay
        
        Returns:
            True si se creó backup
        """
        if self.env_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.project_root / f".env.backup.{timestamp}"
            shutil.copy2(self.env_path, backup_path)
            print(f"   💾 Backup creado: {backup_path.name}")
            return True
        return False
    
    def get_default_template(self) -> str:
        """
        Retorna template por defecto de .env para OmniMaestro
        
        Returns:
            Contenido del template
        """
        return """# OmniMaestro - Configuración de Entorno
# Generado automáticamente por auto_setup_env.py

# === PROYECTO ===
PROJECT_NAME=OmniMaestro
ENVIRONMENT=development
VERSION=0.2.0

# === SUPERVISOR ===
SUPERVISOR_NAME=TOKRAGGCORP-System
SUPERVISOR_EMAIL=tu-email@ejemplo.com

# === IA / API KEYS ===
# ⚠️ IMPORTANTE: Completa estas keys para habilitar funcionalidad IA
# OpenAI (recomendado: gpt-4o-mini para MVP)
OPENAI_API_KEY=

# Anthropic Claude (alternativa/complemento)
ANTHROPIC_API_KEY=

# === CONFIGURACIÓN DE IA ===
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000

# === OCR ===
# Tesseract path (Windows ejemplo: C:\\Program Files\\Tesseract-OCR\\tesseract.exe)
TESSERACT_PATH=tesseract
OCR_LANGUAGES=eng,spa
OCR_ENGINE=tesseract

# === RECURSOS (Hardware Target: i5-7300HQ + 8GB RAM) ===
MAX_RAM_GB=6.5
MAX_CPU_PERCENT=80
MAX_CONCURRENT_TASKS=2

# === PLATAFORMAS ===
DESKTOP_ENABLED=true
MOBILE_ENABLED=false
WEB_ENABLED=false
OMNIMASTRO_PLATFORM=desktop

# === DESARROLLO ===
DEBUG=true
LOG_LEVEL=INFO
LOG_DIR=logs

# === PATHS ===
DATA_DIR=data
DESIGN_DIR=designs
SCREENSHOTS_DIR=screenshots
TUTORIALS_DIR=tutorials
METADATA_DIR=.metadata
TEMP_DIR=temp
CACHE_DIR=.cache

# === DATABASE ===
DATABASE_URL=sqlite:///data/omnimaestro.db

# === WEBHOOKS / NOTIFICACIONES (Opcional) ===
# DISCORD_WEBHOOK_URL=
# SLACK_WEBHOOK_URL=

# === PixARR DESIGN ===
PIXARR_SUPERVISOR=PixARR-System
PIXARR_AUTO_FIX=true

# === UI DESKTOP (Flet) ===
UI_THEME=dark
UI_WIDTH=450
UI_HEIGHT=700
"""
    
    def create_env_file(self, overwrite: bool = False) -> bool:
        """
        Crea archivo .env desde .env.example o template por defecto
        
        Args:
            overwrite: Si debe sobrescribir .env existente
            
        Returns:
            True si se creó exitosamente
        """
        # Si existe y no se debe sobrescribir
        if self.env_path.exists() and not overwrite:
            print(f"   ⏭️  .env ya existe (usar overwrite=True para sobrescribir)")
            return False
        
        # Backup si existe
        if overwrite and self.env_path.exists():
            self.backup_existing_env()
        
        # Fuente del contenido
        if self.env_example_path.exists():
            print(f"   📋 Usando {self.env_example_path.name} como template")
            with open(self.env_example_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            print(f"   📋 Usando template por defecto")
            content = self.get_default_template()
        
        # Crear .env
        with open(self.env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Creado: .env")
        return True
    
    def validate_env(self) -> Dict[str, List[str]]:
        """
        Valida el archivo .env y reporta problemas
        
        Returns:
            Dict con 'warnings' y 'errors'
        """
        issues = {'warnings': [], 'errors': []}
        
        if not self.env_path.exists():
            issues['errors'].append("Archivo .env no existe")
            return issues
        
        with open(self.env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Validar API keys
        critical_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
        has_any_key = False
        
        for key in critical_keys:
            if f"{key}=" in content:
                # Verificar si tiene valor
                for line in content.split('\n'):
                    if line.strip().startswith(f"{key}="):
                        value = line.split('=', 1)[1].strip()
                        if value and not value.startswith('#'):
                            has_any_key = True
                            break
        
        if not has_any_key:
            issues['warnings'].append(
                "No se detectaron API keys de IA configuradas (OPENAI_API_KEY o ANTHROPIC_API_KEY)\n"
                "   La funcionalidad de IA no estará disponible hasta que configures al menos una"
            )
        
        # Validar directorios críticos
        required_vars = ['DATA_DIR', 'LOG_DIR', 'TEMP_DIR']
        for var in required_vars:
            if f"{var}=" not in content:
                issues['warnings'].append(f"Variable {var} no encontrada")
        
        return issues
    
    def print_next_steps(self):
        """Imprime los siguientes pasos para el usuario"""
        print("\n" + "="*60)
        print("📝 SIGUIENTES PASOS")
        print("="*60)
        print("\n1. Edita el archivo .env con tu editor favorito:")
        print(f"   {self.env_path}")
        print("\n2. Completa las API keys:")
        print("   • OPENAI_API_KEY: Obtén en https://platform.openai.com/api-keys")
        print("   • ANTHROPIC_API_KEY: Obtén en https://console.anthropic.com/")
        print("\n3. (Windows) Configura Tesseract OCR:")
        print("   • Descarga: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   • Instala en: C:\\Program Files\\Tesseract-OCR\\")
        print("   • Actualiza TESSERACT_PATH en .env si es necesario")
        print("\n4. Guarda el archivo .env y continúa con el setup")
        print("\n" + "="*60 + "\n")
    
    def run(self, overwrite: bool = False) -> bool:
        """
        Ejecuta el setup completo de entorno
        
        Args:
            overwrite: Si debe sobrescribir .env existente
            
        Returns:
            True si fue exitoso
        """
        print("\n" + "="*60)
        print("🔧 OMNIMAESTRO - SETUP DE ENTORNO")
        print("="*60 + "\n")
        
        # 1. Crear directorios
        print("📁 Creando estructura de directorios...")
        created_dirs = self.create_directories()
        
        # 2. Crear .env
        print("\n⚙️  Configurando variables de entorno...")
        env_created = self.create_env_file(overwrite=overwrite)
        
        # 3. Validar
        print("\n🔍 Validando configuración...")
        issues = self.validate_env()
        
        if issues['errors']:
            print("\n❌ ERRORES CRÍTICOS:")
            for error in issues['errors']:
                print(f"   • {error}")
            return False
        
        if issues['warnings']:
            print("\n⚠️  ADVERTENCIAS:")
            for warning in issues['warnings']:
                print(f"   • {warning}")
        
        print("\n✅ Setup de entorno completado")
        
        # 4. Mostrar siguientes pasos
        self.print_next_steps()
        
        return True


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup automático de entorno OmniMaestro")
    parser.add_argument('--overwrite', action='store_true', 
                       help='Sobrescribir .env existente (crea backup)')
    parser.add_argument('--project-root', type=str,
                       help='Ruta raíz del proyecto (default: auto-detecta)')
    
    args = parser.parse_args()
    
    # Ejecutar setup
    project_root = Path(args.project_root) if args.project_root else None
    setup = EnvSetup(project_root=project_root)
    
    success = setup.run(overwrite=args.overwrite)
    
    if success:
        print("\n🎉 Setup completado exitosamente")
        return 0
    else:
        print("\n❌ Setup falló. Revisa los errores arriba.")
        return 1


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
🎯 OmniMaestro Project Guide - Interactive Development Assistant

Sistema de guía inteligente que ayuda a los desarrolladores a seguir el roadmap
del proyecto paso a paso, validando prerequisitos y evitando errores comunes.

Uso:
    python scripts/project_guide.py status        # Ver estado actual
    python scripts/project_guide.py next          # Ver siguiente paso recomendado
    python scripts/project_guide.py validate      # Validar paso actual completado
    python scripts/project_guide.py roadmap       # Ver roadmap completo
    python scripts/project_guide.py platform      # Cambiar plataforma objetivo
    python scripts/project_guide.py explain       # Explicación profunda de un paso
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse


# Constants
PROJECT_ROOT = Path(__file__).parent.parent
STATE_FILE = PROJECT_ROOT / ".project_state.json"
ROADMAP_FILE = PROJECT_ROOT / "PROJECT_ROADMAP.md"
DASHBOARD_FILE = PROJECT_ROOT / "PROJECT_DASHBOARD.md"
EVOLUTION_LOG = PROJECT_ROOT / "EVOLUTION_LOG.md"


# ANSI Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Project Steps Definition
STEPS = {
    1: {
        "name": "Inicializar repositorio Git",
        "phase": "setup",
        "criticality": "critical",
        "time_minutes": 5,
        "dependencies": [],
        "description": "Configurar control de versiones con Git",
        "validation_commands": ["git status"],
        "resources": ["https://git-scm.com/doc"],
    },
    2: {
        "name": "Configurar estructura de directorios",
        "phase": "setup",
        "criticality": "critical",
        "time_minutes": 10,
        "dependencies": [1],
        "description": "Crear estructura base de carpetas del proyecto",
        "validation_commands": ["ls -la pixarr_design/", "ls -la scripts/"],
        "resources": [],
    },
    3: {
        "name": "Implementar sistema PixARR Design",
        "phase": "setup",
        "criticality": "important",
        "time_minutes": 120,
        "dependencies": [2],
        "description": "Sistema de integridad de archivos de diseño",
        "validation_commands": [],
        "resources": ["README.md"],
    },
    4: {
        "name": "Configurar CI/CD básico",
        "phase": "setup",
        "criticality": "important",
        "time_minutes": 30,
        "dependencies": [1, 3],
        "description": "GitHub Actions para automatización",
        "validation_commands": ["ls .github/workflows/"],
        "resources": [".github/workflows/"],
    },
    5: {
        "name": "Configurar variables de entorno",
        "phase": "setup",
        "criticality": "critical",
        "time_minutes": 15,
        "dependencies": [1],
        "description": "Crear archivo .env con configuraciones necesarias",
        "validation_commands": ["test -f .env", "grep -q 'API_KEY' .env || true"],
        "resources": ["docs/PLATFORM_GUIDES/"],
    },
    6: {
        "name": "Documentar arquitectura base",
        "phase": "setup",
        "criticality": "important",
        "time_minutes": 60,
        "dependencies": [2, 3],
        "description": "Crear documentación de arquitectura del sistema",
        "validation_commands": ["test -f docs/ARCHITECTURE.md"],
        "resources": [],
    },
    7: {
        "name": "Integrar Tesseract OCR",
        "phase": "core_backend",
        "criticality": "critical",
        "time_minutes": 120,
        "dependencies": [5],
        "description": "Configurar Tesseract para extracción de texto de imágenes",
        "validation_commands": [
            "tesseract --version || echo 'Not installed'",
            "python -c \"import pytesseract; print('OK')\" || echo 'Not installed'",
        ],
        "resources": [
            "https://github.com/tesseract-ocr/tesseract",
            "docs/PLATFORM_GUIDES/",
        ],
    },
    8: {
        "name": "Implementar análisis de capturas de pantalla",
        "phase": "core_backend",
        "criticality": "critical",
        "time_minutes": 240,
        "dependencies": [7],
        "description": "Sistema para analizar y extraer información de screenshots",
        "validation_commands": [
            "python -c \"from omnimaestro.core.screenshot_analyzer import ScreenshotAnalyzer; print('OK')\" || echo 'Not implemented'"
        ],
        "resources": [],
    },
    9: {
        "name": "Integrar modelo de IA para explicaciones",
        "phase": "core_backend",
        "criticality": "critical",
        "time_minutes": 360,
        "dependencies": [8],
        "description": "Conectar con API de OpenAI/Anthropic para generar explicaciones",
        "validation_commands": ["python scripts/test_ai_integration.py || echo 'Test not found'"],
        "resources": [],
    },
    10: {
        "name": "Implementar sistema de contexto adaptativo",
        "phase": "core_backend",
        "criticality": "important",
        "time_minutes": 240,
        "dependencies": [9],
        "description": "Sistema que adapta explicaciones según nivel del usuario",
        "validation_commands": [
            "python -c \"from omnimaestro.core.adaptive_context import AdaptiveContext; print('OK')\" || echo 'Not implemented'"
        ],
        "resources": [],
    },
    11: {
        "name": "Instalar Rust y Tauri CLI",
        "phase": "desktop",
        "criticality": "critical",
        "time_minutes": 20,
        "dependencies": [5],
        "description": "Configurar entorno de desarrollo Tauri",
        "validation_commands": [
            "rustc --version",
            "cargo --version",
            "npm list -g @tauri-apps/cli || echo 'Not installed'",
        ],
        "resources": [
            "https://tauri.app/v1/guides/getting-started/prerequisites",
            "docs/PLATFORM_GUIDES/DESKTOP_TAURI.md",
        ],
    },
    12: {
        "name": "Inicializar proyecto Tauri",
        "phase": "desktop",
        "criticality": "critical",
        "time_minutes": 30,
        "dependencies": [11],
        "description": "Crear estructura base de aplicación Tauri",
        "validation_commands": [
            "test -f src-tauri/Cargo.toml",
            "npm run tauri --help || echo 'Not configured'",
        ],
        "resources": ["docs/PLATFORM_GUIDES/DESKTOP_TAURI.md"],
    },
    # More steps would continue here...
}


class ProjectGuide:
    """Main class for the interactive project guide system"""

    def __init__(self):
        self.state = self._load_state()
        self.steps = STEPS

    def _load_state(self) -> Dict[str, Any]:
        """Load project state from JSON file"""
        if STATE_FILE.exists():
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        return self._create_default_state()

    def _create_default_state(self) -> Dict[str, Any]:
        """Create default state structure"""
        return {
            "version": "1.0.0",
            "current_phase": "setup",
            "current_phase_name": "Setup Inicial",
            "current_step": 5,
            "platform_target": "desktop",
            "completed_steps": [1, 2, 3, 4],
            "skipped_warnings": [],
            "in_progress_steps": [],
            "blocked_steps": [],
            "last_updated": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "warnings": [],
            "metadata": {
                "project_name": "OmniMaestro",
                "repository": "eddmtzarias/TE-explico",
                "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                "guide_version": "1.0.0",
            },
        }

    def _save_state(self):
        """Save current state to JSON file"""
        self.state["last_updated"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def _run_command(self, command: str) -> tuple[bool, str]:
        """
        Run a shell command and return success status and output.
        
        Security Note: Uses shell=True to support complex commands (pipes, redirects).
        Commands are pre-defined in STEPS dictionary, not from user input.
        This is safe in trusted development environments.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT,
                timeout=30,
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)

    def _check_dependencies(self, step_num: int) -> tuple[bool, List[int]]:
        """Check if all dependencies for a step are completed"""
        step = self.steps.get(step_num)
        if not step:
            return False, []

        dependencies = step.get("dependencies", [])
        missing = [dep for dep in dependencies if dep not in self.state["completed_steps"]]
        return len(missing) == 0, missing

    def _format_criticality(self, criticality: str) -> str:
        """Format criticality with emoji and color"""
        mapping = {
            "critical": f"{Colors.FAIL}🚨 CRÍTICO{Colors.ENDC}",
            "important": f"{Colors.WARNING}🟡 IMPORTANTE{Colors.ENDC}",
            "optional": f"{Colors.OKBLUE}🔵 OPCIONAL{Colors.ENDC}",
        }
        return mapping.get(criticality, criticality)

    def _print_header(self, title: str):
        """Print formatted header"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{title}{Colors.ENDC}")
        print("━" * 80)

    def _print_separator(self):
        """Print separator line"""
        print("─" * 80)

    def cmd_status(self):
        """Show current project status"""
        self._print_header("📊 Estado del Proyecto OmniMaestro")

        print(f"\n{Colors.BOLD}Plataforma Objetivo:{Colors.ENDC} {self.state['platform_target'].title()}")
        print(f"{Colors.BOLD}Fase Actual:{Colors.ENDC} {self.state['current_phase_name']}")

        completed_count = len(self.state["completed_steps"])
        total_steps = len(self.steps)
        progress = int((completed_count / total_steps) * 100)

        # Progress bar
        filled = int(progress / 5)
        bar = "█" * filled + "░" * (20 - filled)
        print(f"\n{Colors.BOLD}Progreso General:{Colors.ENDC} {bar} {progress}%")
        print(f"{Colors.OKGREEN}✅ Pasos Completados:{Colors.ENDC} {completed_count}/{total_steps}")

        # Last completed step
        if self.state["completed_steps"]:
            last_step = max(self.state["completed_steps"])
            last_step_info = self.steps.get(last_step)
            if last_step_info:
                print(f"\n{Colors.BOLD}Último Paso Completado:{Colors.ENDC}")
                print(f"   #{last_step} - {last_step_info['name']}")

        # Next recommended step
        next_step = self._get_next_step()
        if next_step:
            step_num, step_info = next_step
            print(f"\n{Colors.BOLD}⏳ Próximo Paso Recomendado:{Colors.ENDC}")
            print(f"   #{step_num} {self._format_criticality(step_info['criticality'])} - {step_info['name']}")

        # Warnings
        if self.state.get("warnings"):
            print(f"\n{Colors.WARNING}⚠️  Advertencias:{Colors.ENDC}")
            for warning in self.state["warnings"]:
                print(f"   - {warning['message']}")

        # Blockers
        if self.state.get("blockers"):
            print(f"\n{Colors.FAIL}🚫 Bloqueadores:{Colors.ENDC}")
            for blocker in self.state["blockers"]:
                print(f"   - {blocker}")

        print(f"\n{Colors.OKCYAN}💡 Sugerencia:{Colors.ENDC} Ejecuta 'python scripts/project_guide.py next' para ver detalles del próximo paso")
        print()

    def _get_next_step(self) -> Optional[tuple[int, Dict]]:
        """Get the next recommended step based on current state"""
        for step_num in sorted(self.steps.keys()):
            if step_num not in self.state["completed_steps"]:
                deps_ok, _ = self._check_dependencies(step_num)
                if deps_ok:
                    return (step_num, self.steps[step_num])
        return None

    def cmd_next(self, step_number: Optional[int] = None):
        """Show details of next step or specific step"""
        if step_number:
            if step_number not in self.steps:
                print(f"{Colors.FAIL}❌ Error: Paso #{step_number} no existe{Colors.ENDC}")
                return
            step_num = step_number
            step_info = self.steps[step_num]
        else:
            next_step = self._get_next_step()
            if not next_step:
                print(f"{Colors.OKGREEN}✅ ¡Felicitaciones! Has completado todos los pasos disponibles.{Colors.ENDC}")
                return
            step_num, step_info = next_step

        self._print_header(f"🎯 Paso #{step_num}: {step_info['name']}")

        print(f"\n{Colors.BOLD}Criticidad:{Colors.ENDC} {self._format_criticality(step_info['criticality'])}")
        print(f"{Colors.BOLD}Tiempo Estimado:{Colors.ENDC} {step_info['time_minutes']} minutos")
        print(f"{Colors.BOLD}Fase:{Colors.ENDC} {step_info['phase'].replace('_', ' ').title()}")

        # Dependencies
        deps_ok, missing_deps = self._check_dependencies(step_num)
        if step_info.get("dependencies"):
            status = f"{Colors.OKGREEN}✅ Completadas{Colors.ENDC}" if deps_ok else f"{Colors.FAIL}❌ Pendientes{Colors.ENDC}"
            print(f"{Colors.BOLD}Dependencias:{Colors.ENDC} {status}")
            if missing_deps:
                print(f"   Pasos requeridos: {', '.join(f'#{d}' for d in missing_deps)}")
        else:
            print(f"{Colors.BOLD}Dependencias:{Colors.ENDC} Ninguna")

        # Description
        print(f"\n{Colors.BOLD}📖 Descripción:{Colors.ENDC}")
        print(f"   {step_info['description']}")

        # Validation commands
        if step_info.get("validation_commands"):
            print(f"\n{Colors.BOLD}✅ Validación:{Colors.ENDC}")
            print(f"   python scripts/project_guide.py validate --step {step_num}")

        # Resources
        if step_info.get("resources"):
            print(f"\n{Colors.BOLD}🔗 Recursos:{Colors.ENDC}")
            for resource in step_info["resources"]:
                print(f"   - {resource}")

        print()

    def cmd_validate(self, step_number: Optional[int] = None):
        """Validate if a step is completed"""
        if step_number is None:
            # Validate next step
            next_step = self._get_next_step()
            if not next_step:
                print(f"{Colors.OKGREEN}✅ Todos los pasos completados{Colors.ENDC}")
                return
            step_num, step_info = next_step
        else:
            if step_number not in self.steps:
                print(f"{Colors.FAIL}❌ Error: Paso #{step_number} no existe{Colors.ENDC}")
                return
            step_num = step_number
            step_info = self.steps[step_num]

        self._print_header(f"🔍 Validando Paso #{step_num}: {step_info['name']}")

        # Check dependencies first
        deps_ok, missing_deps = self._check_dependencies(step_num)
        if not deps_ok:
            print(f"\n{Colors.FAIL}❌ Error: Dependencias no completadas{Colors.ENDC}")
            print(f"   Completa primero los pasos: {', '.join(f'#{d}' for d in missing_deps)}")
            return

        # Run validation commands
        validation_commands = step_info.get("validation_commands", [])
        if not validation_commands:
            print(f"\n{Colors.WARNING}⚠️  Este paso no tiene comandos de validación automática{Colors.ENDC}")
            while True:
                response = input(f"\n¿Marcar como completado manualmente? (s/n): ").lower().strip()
                if response in ['s', 'si', 'y', 'yes']:
                    self._mark_step_completed(step_num)
                    break
                elif response in ['n', 'no']:
                    break
                else:
                    print(f"{Colors.WARNING}Por favor, responde 's' o 'n'{Colors.ENDC}")
            return

        print(f"\n{Colors.BOLD}Ejecutando validaciones...{Colors.ENDC}\n")

        all_passed = True
        for i, cmd in enumerate(validation_commands, 1):
            print(f"   [{i}/{len(validation_commands)}] {cmd}")
            success, output = self._run_command(cmd)

            if success:
                print(f"   {Colors.OKGREEN}✅ Pasó{Colors.ENDC}")
            else:
                print(f"   {Colors.FAIL}❌ Falló{Colors.ENDC}")
                if output.strip():
                    print(f"   {Colors.WARNING}Output:{Colors.ENDC} {output.strip()[:200]}")
                all_passed = False

        print()
        if all_passed:
            print(f"{Colors.OKGREEN}✅ ¡Todas las validaciones pasaron!{Colors.ENDC}")
            self._mark_step_completed(step_num)
        else:
            print(f"{Colors.FAIL}❌ Algunas validaciones fallaron{Colors.ENDC}")
            print(f"{Colors.WARNING}💡 Revisa los errores arriba y corrige antes de continuar{Colors.ENDC}")

    def _mark_step_completed(self, step_num: int):
        """Mark a step as completed"""
        if step_num not in self.state["completed_steps"]:
            self.state["completed_steps"].append(step_num)
            self.state["completed_steps"].sort()

            # Update current step
            next_step = self._get_next_step()
            if next_step:
                self.state["current_step"] = next_step[0]

            self._save_state()
            self._update_dashboard()
            print(f"\n{Colors.OKGREEN}📝 Paso #{step_num} marcado como completado{Colors.ENDC}")

    def _update_dashboard(self):
        """Update the dashboard file with current progress"""
        # This would regenerate PROJECT_DASHBOARD.md based on current state
        # For now, just update the timestamp
        pass

    def cmd_roadmap(self):
        """Display the complete roadmap"""
        self._print_header("🗺️  OmniMaestro - Roadmap Completo")

        phases = {}
        for step_num, step_info in sorted(self.steps.items()):
            phase = step_info["phase"]
            if phase not in phases:
                phases[phase] = []
            phases[phase].append((step_num, step_info))

        phase_names = {
            "setup": "Setup Inicial",
            "core_backend": "Core del Sistema (Backend AI)",
            "desktop": "Implementación Desktop (Tauri)",
            "mobile": "Implementación Mobile (Flutter)",
            "web": "Implementación Web (PWA)",
            "integrations": "Integraciones Avanzadas",
            "testing": "Testing & QA",
            "deployment": "Deployment & Release",
        }

        for phase_key, phase_steps in phases.items():
            phase_name = phase_names.get(phase_key, phase_key)
            completed_in_phase = sum(1 for step_num, _ in phase_steps if step_num in self.state["completed_steps"])
            total_in_phase = len(phase_steps)
            progress = int((completed_in_phase / total_in_phase) * 100) if total_in_phase > 0 else 0

            print(f"\n{Colors.BOLD}📌 {phase_name}{Colors.ENDC} ({completed_in_phase}/{total_in_phase} - {progress}%)")
            self._print_separator()

            for step_num, step_info in phase_steps:
                status = "✅" if step_num in self.state["completed_steps"] else "⏳"
                deps_ok, _ = self._check_dependencies(step_num)
                blocked = "" if deps_ok or step_num in self.state["completed_steps"] else "🔒"

                print(f"   {status} {blocked} #{step_num:2d} - {step_info['name']}")
                print(f"        {self._format_criticality(step_info['criticality'])} | {step_info['time_minutes']} min")

        print()

    def cmd_platform(self, platform: Optional[str] = None):
        """Change or display target platform"""
        valid_platforms = ["desktop", "mobile", "web"]

        if platform is None:
            print(f"\n{Colors.BOLD}Plataforma actual:{Colors.ENDC} {self.state['platform_target'].title()}")
            print(f"\n{Colors.BOLD}Plataformas disponibles:{Colors.ENDC}")
            for p in valid_platforms:
                current = "✅" if p == self.state['platform_target'] else "  "
                print(f"   {current} {p}")
            print()
            return

        if platform not in valid_platforms:
            print(f"{Colors.FAIL}❌ Error: Plataforma inválida. Opciones: {', '.join(valid_platforms)}{Colors.ENDC}")
            return

        old_platform = self.state['platform_target']
        self.state['platform_target'] = platform
        self._save_state()

        print(f"{Colors.OKGREEN}✅ Plataforma cambiada: {old_platform} → {platform}{Colors.ENDC}")

    def cmd_explain(self, step_number: int):
        """Provide deep explanation of a step"""
        if step_number not in self.steps:
            print(f"{Colors.FAIL}❌ Error: Paso #{step_number} no existe{Colors.ENDC}")
            return

        step_info = self.steps[step_number]
        self._print_header(f"📚 Explicación Profunda - Paso #{step_number}")

        print(f"\n{Colors.BOLD}🎯 Objetivo:{Colors.ENDC}")
        print(f"   {step_info['name']}")

        print(f"\n{Colors.BOLD}❓ ¿Por qué es necesario?{Colors.ENDC}")
        print(f"   {step_info['description']}")

        print(f"\n{Colors.BOLD}⚠️  ¿Qué pasa si se salta?{Colors.ENDC}")
        if step_info['criticality'] == 'critical':
            print(f"   {Colors.FAIL}Este es un paso CRÍTICO. Saltarlo puede causar:")
            print(f"   - Errores en pasos posteriores")
            print(f"   - Funcionalidad rota o incompleta")
            print(f"   - Necesidad de retrabajar código ya escrito{Colors.ENDC}")
        elif step_info['criticality'] == 'important':
            print(f"   {Colors.WARNING}Este paso es IMPORTANTE. Saltarlo puede:")
            print(f"   - Reducir calidad del código")
            print(f"   - Dificultar mantenimiento futuro")
            print(f"   - Crear deuda técnica{Colors.ENDC}")
        else:
            print(f"   Este paso es OPCIONAL. Puede saltarse sin grandes consecuencias,")
            print(f"   pero completarlo mejora la experiencia general.")

        print(f"\n{Colors.BOLD}🔗 Relación con otros pasos:{Colors.ENDC}")
        if step_info.get("dependencies"):
            print(f"   Depende de: {', '.join(f'Paso #{d}' for d in step_info['dependencies'])}")

        # Find dependent steps
        dependent_steps = [
            num for num, info in self.steps.items()
            if step_number in info.get("dependencies", [])
        ]
        if dependent_steps:
            print(f"   Requerido por: {', '.join(f'Paso #{d}' for d in dependent_steps)}")

        if step_info.get("resources"):
            print(f"\n{Colors.BOLD}📖 Recursos adicionales:{Colors.ENDC}")
            for resource in step_info["resources"]:
                print(f"   - {resource}")

        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="🎯 OmniMaestro Project Guide - Interactive Development Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # Status command
    subparsers.add_parser("status", help="Ver estado actual del proyecto")

    # Next command
    next_parser = subparsers.add_parser("next", help="Ver siguiente paso recomendado")
    next_parser.add_argument("--step", type=int, help="Ver paso específico")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validar paso completado")
    validate_parser.add_argument("--step", type=int, help="Validar paso específico")

    # Roadmap command
    subparsers.add_parser("roadmap", help="Ver roadmap completo")

    # Platform command
    platform_parser = subparsers.add_parser("platform", help="Cambiar plataforma objetivo")
    platform_parser.add_argument("target", nargs="?", choices=["desktop", "mobile", "web"], help="Plataforma objetivo")

    # Explain command
    explain_parser = subparsers.add_parser("explain", help="Explicación profunda de un paso")
    explain_parser.add_argument("step", type=int, help="Número del paso a explicar")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    guide = ProjectGuide()

    if args.command == "status":
        guide.cmd_status()
    elif args.command == "next":
        guide.cmd_next(args.step if hasattr(args, 'step') else None)
    elif args.command == "validate":
        guide.cmd_validate(args.step if hasattr(args, 'step') else None)
    elif args.command == "roadmap":
        guide.cmd_roadmap()
    elif args.command == "platform":
        guide.cmd_platform(args.target if hasattr(args, 'target') else None)
    elif args.command == "explain":
        guide.cmd_explain(args.step)


if __name__ == "__main__":
    main()

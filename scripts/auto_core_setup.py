"""
Setup Automático del Core Backend de OmniMaestro
Instala dependencias y genera módulos principales del sistema
"""

import sys
import subprocess
import os
from pathlib import Path
from typing import List, Tuple, Optional
import time


class CoreSetup:
    """Configurador del core backend de OmniMaestro"""
    
    def __init__(self, project_root: Path = None):
        """
        Inicializa el configurador
        
        Args:
            project_root: Raíz del proyecto
        """
        if project_root is None:
            current = Path(__file__).resolve()
            self.project_root = current.parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.omnimastro_dir = self.project_root / "omnimastro"
        self.tests_dir = self.project_root / "tests"
    
    def check_python_version(self) -> Tuple[bool, str]:
        """Verifica la versión de Python"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        return False, f"Python {version.major}.{version.minor} (requiere >= 3.8)"
    
    def install_dependencies(self) -> bool:
        """
        Instala las dependencias necesarias
        
        Returns:
            True si fue exitoso
        """
        print("\n📦 Instalando dependencias de Python...")
        print("   (Esto puede tomar varios minutos en i5-7300HQ)\n")
        
        # Lista de dependencias críticas
        dependencies = [
            "flet>=0.21.0",
            "pytesseract>=0.3.10",
            "opencv-python-headless>=4.8.0",
            "openai>=1.7.0",
            "anthropic>=0.8.0",
            "psutil>=5.9.0",
            "python-dotenv>=1.0.0",
            "pillow>=10.0.0",
            "numpy>=1.24.0",
            "sqlalchemy>=2.0.0",
            "aiosqlite>=0.19.0",
        ]
        
        try:
            # Actualizar pip primero
            print("   Actualizando pip...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                check=True,
                capture_output=True
            )
            
            # Instalar dependencias una por una para mejor tracking
            for i, dep in enumerate(dependencies, 1):
                print(f"   [{i}/{len(dependencies)}] Instalando {dep.split('>=')[0]}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep, "--quiet"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"      ⚠️  Error instalando {dep}: {result.stderr}")
                    # Intentar sin versión específica
                    pkg_name = dep.split('>=')[0]
                    print(f"      Reintentando {pkg_name} sin versión específica...")
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", pkg_name, "--quiet"],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        print(f"      ❌ No se pudo instalar {pkg_name}")
                        return False
            
            print("\n   ✅ Todas las dependencias instaladas correctamente")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n   ❌ Error instalando dependencias: {e}")
            print(f"   Salida: {e.output if hasattr(e, 'output') else 'N/A'}")
            return False
        except Exception as e:
            print(f"\n   ❌ Error inesperado: {e}")
            return False
    
    def create_directory_structure(self) -> bool:
        """Crea la estructura de directorios de omnimastro"""
        print("\n📁 Creando estructura de módulos...")
        
        directories = [
            self.omnimastro_dir / "core",
            self.omnimastro_dir / "desktop",
            self.omnimastro_dir / "shared",
            self.tests_dir,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {directory.relative_to(self.project_root)}/")
            
            # Crear __init__.py si no existe
            init_file = directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""OmniMaestro module"""\n')
        
        return True
    
    def create_enhanced_config(self) -> bool:
        """Crea versión mejorada de shared/config.py"""
        print("\n⚙️  Generando omnimastro/shared/config.py...")
        
        config_path = self.omnimastro_dir / "shared" / "config.py"
        
        # Si ya existe, hacer backup
        if config_path.exists():
            backup_path = config_path.with_suffix('.py.backup')
            config_path.rename(backup_path)
            print(f"   💾 Backup: config.py.backup")
        
        config_content = '''"""
Configuración Global de OmniMaestro (Enhanced)
Gestiona la configuración del sistema con validación completa
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Cargar variables de entorno desde .env
load_dotenv()

# Directorios base
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / os.getenv("DATA_DIR", "data")
LOGS_DIR = PROJECT_ROOT / os.getenv("LOG_DIR", "logs")
TEMP_DIR = PROJECT_ROOT / os.getenv("TEMP_DIR", "temp")
CACHE_DIR = PROJECT_ROOT / os.getenv("CACHE_DIR", ".cache")
DESIGNS_DIR = PROJECT_ROOT / os.getenv("DESIGN_DIR", "designs")
SCREENSHOTS_DIR = PROJECT_ROOT / os.getenv("SCREENSHOTS_DIR", "screenshots")

# Crear directorios si no existen
for directory in [DATA_DIR, LOGS_DIR, TEMP_DIR, CACHE_DIR, DESIGNS_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# === Configuración de IA ===
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # "openai" o "anthropic"
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2000"))

# === Configuración de OCR ===
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "tesseract")
OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")
OCR_LANGUAGES = os.getenv("OCR_LANGUAGES", "eng,spa").split(",")

# === Recursos del Sistema ===
MAX_RAM_GB = float(os.getenv("MAX_RAM_GB", "6.5"))
MAX_CPU_PERCENT = int(os.getenv("MAX_CPU_PERCENT", "80"))
MAX_CONCURRENT_TASKS = int(os.getenv("MAX_CONCURRENT_TASKS", "2"))

# === Database ===
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'omnimaestro.db'}")

# === UI Desktop ===
UI_THEME = os.getenv("UI_THEME", "dark")
UI_WIDTH = int(os.getenv("UI_WIDTH", "450"))
UI_HEIGHT = int(os.getenv("UI_HEIGHT", "700"))

# === Logging ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# === Plataforma ===
CURRENT_PLATFORM = os.getenv("OMNIMASTRO_PLATFORM", "desktop")


class Config:
    """Clase de configuración con validación"""
    
    @staticmethod
    def is_api_key_configured(service: str) -> bool:
        """Verifica si una API key está configurada"""
        if service.lower() == "openai":
            return bool(OPENAI_API_KEY and OPENAI_API_KEY != "")
        elif service.lower() == "anthropic":
            return bool(ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "")
        return False
    
    @staticmethod
    def get_configured_ai_providers() -> List[str]:
        """Retorna lista de proveedores de IA configurados"""
        providers = []
        if Config.is_api_key_configured("openai"):
            providers.append("openai")
        if Config.is_api_key_configured("anthropic"):
            providers.append("anthropic")
        return providers
    
    @staticmethod
    def validate() -> Dict[str, List[str]]:
        """
        Valida la configuración completa
        
        Returns:
            Dict con 'warnings' y 'errors'
        """
        issues = {'warnings': [], 'errors': []}
        
        # Validar API keys
        providers = Config.get_configured_ai_providers()
        if not providers:
            issues['warnings'].append(
                "No hay API keys de IA configuradas. "
                "La funcionalidad de explicaciones no estará disponible."
            )
        
        # Validar directorios
        for name, path in [
            ("DATA_DIR", DATA_DIR),
            ("LOGS_DIR", LOGS_DIR),
            ("TEMP_DIR", TEMP_DIR),
        ]:
            if not path.exists():
                issues['errors'].append(f"Directorio {name} no existe: {path}")
        
        # Validar OCR
        if OCR_ENGINE == "tesseract":
            try:
                import pytesseract
                pytesseract.get_tesseract_version()
            except Exception as e:
                issues['warnings'].append(
                    f"Tesseract OCR no está disponible: {e}. "
                    "Instala desde: https://github.com/tesseract-ocr/tesseract"
                )
        
        return issues
    
    @staticmethod
    def print_status():
        """Imprime el estado de la configuración"""
        print("\\n" + "="*60)
        print("⚙️  CONFIGURACIÓN DE OMNIMAESTRO")
        print("="*60)
        
        # IA Providers
        providers = Config.get_configured_ai_providers()
        print(f"\\n🤖 Proveedores de IA:")
        if providers:
            for provider in providers:
                print(f"   ✅ {provider.upper()}")
        else:
            print("   ❌ Ninguno configurado")
        
        # OCR
        print(f"\\n📷 OCR Engine: {OCR_ENGINE}")
        print(f"   Idiomas: {', '.join(OCR_LANGUAGES)}")
        
        # Database
        print(f"\\n💾 Database: {DATABASE_URL}")
        
        # Recursos
        print(f"\\n⚡ Límites de recursos:")
        print(f"   RAM máxima: {MAX_RAM_GB} GB")
        print(f"   CPU máxima: {MAX_CPU_PERCENT}%")
        
        # Validación
        issues = Config.validate()
        if issues['errors']:
            print(f"\\n❌ Errores ({len(issues['errors'])}):")
            for error in issues['errors']:
                print(f"   • {error}")
        
        if issues['warnings']:
            print(f"\\n⚠️  Advertencias ({len(issues['warnings'])}):")
            for warning in issues['warnings']:
                print(f"   • {warning}")
        
        if not issues['errors'] and not issues['warnings']:
            print("\\n✅ Configuración válida")
        
        print("\\n" + "="*60 + "\\n")


# Instancia global
config = Config()


def get_config_value(key: str, default=None):
    """Obtiene un valor de configuración con fallback"""
    return os.getenv(key, default)
'''
        
        config_path.write_text(config_content)
        print("   ✅ Generado")
        return True
    
    def create_ai_explainer(self) -> bool:
        """Crea módulo ai_explainer.py optimizado"""
        print("\n🤖 Generando omnimastro/core/ai_explainer.py...")
        
        explainer_path = self.omnimastro_dir / "core" / "ai_explainer.py"
        
        explainer_content = '''"""
Motor de Explicaciones con IA para OmniMaestro
Versión simplificada para MVP con OpenAI y Anthropic
"""

import os
import logging
from typing import Optional, Dict
from enum import Enum

logger = logging.getLogger(__name__)


class UserLevel(Enum):
    """Niveles de usuario para explicaciones adaptativas"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class AIExplainer:
    """Motor de explicaciones con IA"""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        """
        Inicializa el motor de explicaciones
        
        Args:
            provider: "openai" o "anthropic"
            api_key: API key (opcional, usa variable de entorno)
        """
        self.provider = provider.lower()
        self.client = None
        self.model = "gpt-4o-mini" if provider == "openai" else "claude-3-haiku-20240307"
        
        # Inicializar cliente
        if self.provider == "openai":
            self._init_openai(api_key)
        elif self.provider == "anthropic":
            self._init_anthropic(api_key)
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")
    
    def _init_openai(self, api_key: Optional[str]):
        """Inicializa cliente OpenAI"""
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            logger.warning("OPENAI_API_KEY no configurada")
            return
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=key)
            logger.info(f"✅ OpenAI inicializado (modelo: {self.model})")
        except ImportError:
            logger.error("openai no instalado: pip install openai")
        except Exception as e:
            logger.error(f"Error inicializando OpenAI: {e}")
    
    def _init_anthropic(self, api_key: Optional[str]):
        """Inicializa cliente Anthropic"""
        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            logger.warning("ANTHROPIC_API_KEY no configurada")
            return
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=key)
            logger.info(f"✅ Anthropic inicializado (modelo: {self.model})")
        except ImportError:
            logger.error("anthropic no instalado: pip install anthropic")
        except Exception as e:
            logger.error(f"Error inicializando Anthropic: {e}")
    
    def is_ready(self) -> bool:
        """Verifica si el motor está listo"""
        return self.client is not None
    
    def explain(self, 
                text: str, 
                level: UserLevel = UserLevel.INTERMEDIATE,
                language: str = "es") -> Optional[str]:
        """
        Genera explicación pedagógica del texto
        
        Args:
            text: Texto a explicar
            level: Nivel del usuario
            language: Idioma (default: español)
            
        Returns:
            Explicación generada o None si falla
        """
        if not self.is_ready():
            return "❌ Error: Motor de IA no inicializado. Verifica tu .env"
        
        # Construir prompt pedagógico
        prompt = self._build_prompt(text, level, language)
        
        try:
            if self.provider == "openai":
                return self._explain_openai(prompt)
            elif self.provider == "anthropic":
                return self._explain_anthropic(prompt)
        except Exception as e:
            logger.error(f"Error generando explicación: {e}")
            return f"❌ Error: {str(e)}"
    
    def _build_prompt(self, text: str, level: UserLevel, language: str) -> str:
        """Construye prompt pedagógico"""
        level_instructions = {
            UserLevel.BEGINNER: "Usa lenguaje muy simple, evita tecnicismos. Explica como si fuera a un principiante absoluto.",
            UserLevel.INTERMEDIATE: "Usa lenguaje claro pero puedes incluir algunos términos técnicos explicados.",
            UserLevel.ADVANCED: "Puedes usar terminología técnica avanzada y asumir conocimientos previos."
        }
        
        instruction = level_instructions.get(level, level_instructions[UserLevel.INTERMEDIATE])
        
        return f"""Eres TE-explico, un asistente educativo experto.

Explica el siguiente contenido de manera pedagógica:

{text}

Requisitos:
1. {instruction}
2. Idioma: {language}
3. Estructura: 
   - Resumen breve (2-3 líneas)
   - Explicación detallada
   - Conceptos clave
   - Ejemplo práctico si aplica
4. Estilo: formal pero amigable, técnicamente preciso pero comprensible

Genera una explicación completa y útil."""
    
    def _explain_openai(self, prompt: str) -> str:
        """Genera explicación con OpenAI"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Eres TE-explico, un asistente educativo pedagógico."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    def _explain_anthropic(self, prompt: str) -> str:
        """Genera explicación con Anthropic"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system="Eres TE-explico, un asistente educativo pedagógico.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text


def create_explainer(provider: str = None) -> AIExplainer:
    """
    Factory function para crear explainer
    
    Args:
        provider: "openai", "anthropic" o None (auto-detecta)
        
    Returns:
        AIExplainer configurado
    """
    if provider is None:
        # Auto-detectar proveedor disponible
        if os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        elif os.getenv("ANTHROPIC_API_KEY"):
            provider = "anthropic"
        else:
            raise ValueError("No hay API keys configuradas. Configura OPENAI_API_KEY o ANTHROPIC_API_KEY en .env")
    
    return AIExplainer(provider=provider)
'''
        
        explainer_path.write_text(explainer_content)
        print("   ✅ Generado")
        return True
    
    def create_desktop_ui(self) -> bool:
        """Crea UI desktop con Flet"""
        print("\n🖥️  Generando omnimastro/desktop/main.py...")
        
        main_path = self.omnimastro_dir / "desktop" / "main.py"
        
        main_content = '''"""
OmniMaestro Desktop UI - MVP con Flet
Interfaz simple para probar el sistema de explicaciones
"""

import flet as ft
import sys
from pathlib import Path

# Agregar directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from omnimastro.shared.config import config
from omnimastro.core.ai_explainer import create_explainer, UserLevel


class OmniMaestroApp:
    """Aplicación principal de OmniMaestro"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.explainer = None
        self.setup_page()
        self.create_ui()
        self.init_explainer()
    
    def setup_page(self):
        """Configura propiedades de la página"""
        self.page.title = "OmniMaestro - TE-explico MVP"
        self.page.window_width = 450
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
    
    def init_explainer(self):
        """Inicializa el motor de IA"""
        try:
            self.explainer = create_explainer()
            if self.explainer.is_ready():
                self.status_text.value = f"✅ Motor IA listo ({self.explainer.provider})"
                self.status_text.color = ft.colors.GREEN
            else:
                self.status_text.value = "❌ Motor IA no inicializado"
                self.status_text.color = ft.colors.RED
        except Exception as e:
            self.status_text.value = f"❌ Error: {str(e)}"
            self.status_text.color = ft.colors.RED
        
        self.page.update()
    
    def create_ui(self):
        """Crea la interfaz de usuario"""
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "🎓 OmniMaestro",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "TE-explico - Asistente Educativo",
                    size=14,
                    color=ft.colors.GREY_400,
                    text_align=ft.TextAlign.CENTER,
                ),
            ]),
            margin=ft.margin.only(bottom=20)
        )
        
        # Status indicator
        self.status_text = ft.Text(
            "⏳ Inicializando...",
            size=12,
            color=ft.colors.ORANGE,
        )
        
        status_bar = ft.Container(
            content=self.status_text,
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=10,
            border_radius=5,
            margin=ft.margin.only(bottom=20)
        )
        
        # Input field
        self.input_field = ft.TextField(
            label="Texto o pregunta a explicar",
            multiline=True,
            min_lines=5,
            max_lines=10,
            hint_text="Ejemplo: ¿Qué es la fotosíntesis?\\nEjemplo: Explica el teorema de Pitágoras",
        )
        
        # Level selector
        self.level_dropdown = ft.Dropdown(
            label="Nivel de explicación",
            options=[
                ft.dropdown.Option("beginner", "Principiante"),
                ft.dropdown.Option("intermediate", "Intermedio"),
                ft.dropdown.Option("advanced", "Avanzado"),
            ],
            value="intermediate",
            width=200,
        )
        
        # Buttons
        explain_btn = ft.ElevatedButton(
            "🤖 Explicar",
            on_click=self.on_explain_click,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE,
            )
        )
        
        screenshot_btn = ft.ElevatedButton(
            "📸 Capturar Pantalla",
            on_click=self.on_screenshot_click,
            width=200,
            height=50,
            disabled=True,  # MVP: feature no implementada aún
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.GREY_700,
            )
        )
        
        button_row = ft.Row(
            [explain_btn, screenshot_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        
        # Output area
        self.output_text = ft.Text(
            "Las explicaciones aparecerán aquí...",
            size=14,
            selectable=True,
            color=ft.colors.GREY_400,
        )
        
        output_container = ft.Container(
            content=ft.Column([
                ft.Text("Explicación:", weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.output_text,
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=15,
            border_radius=5,
            expand=True,
        )
        
        # Main layout
        main_column = ft.Column([
            header,
            status_bar,
            self.input_field,
            self.level_dropdown,
            button_row,
            ft.Divider(height=20),
            output_container,
        ], expand=True)
        
        self.page.add(main_column)
    
    def on_explain_click(self, e):
        """Maneja click en botón Explicar"""
        text = self.input_field.value
        
        if not text or not text.strip():
            self.output_text.value = "⚠️  Por favor ingresa un texto o pregunta"
            self.output_text.color = ft.colors.ORANGE
            self.page.update()
            return
        
        if not self.explainer or not self.explainer.is_ready():
            self.output_text.value = "❌ Motor de IA no está listo. Verifica tu configuración en .env"
            self.output_text.color = ft.colors.RED
            self.page.update()
            return
        
        # Mostrar indicador de carga
        self.output_text.value = "⏳ Generando explicación..."
        self.output_text.color = ft.colors.BLUE
        self.page.update()
        
        # Generar explicación
        try:
            level = UserLevel(self.level_dropdown.value)
            explanation = self.explainer.explain(text, level=level)
            
            self.output_text.value = explanation
            self.output_text.color = ft.colors.WHITE
        except Exception as ex:
            self.output_text.value = f"❌ Error: {str(ex)}"
            self.output_text.color = ft.colors.RED
        
        self.page.update()
    
    def on_screenshot_click(self, e):
        """Maneja click en botón Capturar Pantalla (placeholder)"""
        self.output_text.value = "📸 Captura de pantalla: Feature próximamente..."
        self.output_text.color = ft.colors.ORANGE
        self.page.update()


def main(page: ft.Page):
    """Punto de entrada principal"""
    OmniMaestroApp(page)


if __name__ == "__main__":
    print("🚀 Iniciando OmniMaestro Desktop...")
    print("   Presiona Ctrl+C para salir\\n")
    
    # Mostrar configuración
    config.print_status()
    
    # Lanzar app
    ft.app(target=main)
'''
        
        main_path.write_text(main_content)
        print("   ✅ Generado")
        return True
    
    def create_basic_tests(self) -> bool:
        """Crea tests básicos"""
        print("\n🧪 Generando tests básicos...")
        
        # Test config
        test_config_path = self.tests_dir / "test_config.py"
        test_config_content = '''"""Tests para configuración"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from omnimastro.shared.config import config


def test_config_import():
    """Test que config se puede importar"""
    assert config is not None


def test_config_validation():
    """Test validación de config"""
    issues = config.validate()
    assert 'warnings' in issues
    assert 'errors' in issues
    # No debe haber errores críticos
    assert len(issues['errors']) == 0


if __name__ == "__main__":
    print("Running config tests...")
    test_config_import()
    print("✅ test_config_import passed")
    test_config_validation()
    print("✅ test_config_validation passed")
    print("\\n✅ All tests passed!")
'''
        test_config_path.write_text(test_config_content)
        print("   ✅ tests/test_config.py")
        
        # Test AI explainer
        test_ai_path = self.tests_dir / "test_ai_explainer.py"
        test_ai_content = '''"""Tests para AI explainer"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_ai_explainer_import():
    """Test que AIExplainer se puede importar"""
    from omnimastro.core.ai_explainer import AIExplainer, UserLevel
    assert AIExplainer is not None
    assert UserLevel is not None


if __name__ == "__main__":
    print("Running AI explainer tests...")
    test_ai_explainer_import()
    print("✅ test_ai_explainer_import passed")
    print("\\n✅ All tests passed!")
'''
        test_ai_path.write_text(test_ai_content)
        print("   ✅ tests/test_ai_explainer.py")
        
        return True
    
    def run(self) -> bool:
        """
        Ejecuta el setup completo del core
        
        Returns:
            True si fue exitoso
        """
        print("\n" + "="*60)
        print("🚀 OMNIMAESTRO - SETUP DEL CORE BACKEND")
        print("="*60)
        
        # 1. Verificar Python
        print("\n🐍 Verificando Python...")
        ok, version = self.check_python_version()
        if ok:
            print(f"   ✅ {version}")
        else:
            print(f"   ❌ {version}")
            return False
        
        # 2. Instalar dependencias
        if not self.install_dependencies():
            print("\n❌ Error instalando dependencias")
            return False
        
        # 3. Crear estructura
        if not self.create_directory_structure():
            return False
        
        # 4. Generar módulos
        if not self.create_enhanced_config():
            return False
        
        if not self.create_ai_explainer():
            return False
        
        if not self.create_desktop_ui():
            return False
        
        # 5. Crear tests
        if not self.create_basic_tests():
            return False
        
        print("\n✅ Setup del core completado exitosamente")
        
        # Instrucciones finales
        print("\n" + "="*60)
        print("🎉 ¡CORE BACKEND LISTO!")
        print("="*60)
        print("\nPara lanzar la aplicación desktop:")
        print(f"   python {self.omnimastro_dir / 'desktop' / 'main.py'}")
        print("\nPara ejecutar tests:")
        print(f"   python {self.tests_dir / 'test_config.py'}")
        print(f"   python {self.tests_dir / 'test_ai_explainer.py'}")
        print("\n" + "="*60 + "\n")
        
        return True


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup del core backend de OmniMaestro")
    parser.add_argument('--project-root', type=str,
                       help='Ruta raíz del proyecto')
    
    args = parser.parse_args()
    
    project_root = Path(args.project_root) if args.project_root else None
    setup = CoreSetup(project_root=project_root)
    
    success = setup.run()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())

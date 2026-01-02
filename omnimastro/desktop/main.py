"""
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
            hint_text="Ejemplo: ¿Qué es la fotosíntesis?\nEjemplo: Explica el teorema de Pitágoras",
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
    print("   Presiona Ctrl+C para salir\n")
    
    # Mostrar configuración
    config.print_status()
    
    # Lanzar app
    ft.app(target=main)

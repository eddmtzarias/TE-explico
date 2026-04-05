"""
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

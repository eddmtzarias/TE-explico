"""
Motor de IA para TE-explico - Generación de Explicaciones Educativas Adaptativas
Integra OpenAI y Anthropic para análisis de screenshots y generación de contenido educativo.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass
import json
import base64
from abc import ABC, abstractmethod

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIProvider(Enum):
    """Proveedores de IA disponibles"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AUTO = "auto"  # Selección automática basada en disponibilidad y contexto


class EducationLevel(Enum):
    """Niveles educativos para adaptación de contenido"""
    ELEMENTARY = "elementary"  # Primaria
    MIDDLE_SCHOOL = "middle_school"  # Secundaria
    HIGH_SCHOOL = "high_school"  # Preparatoria
    UNIVERSITY = "university"  # Universidad
    PROFESSIONAL = "professional"  # Profesional
    AUTO = "auto"  # Detección automática


class ExplanationStyle(Enum):
    """Estilos de explicación"""
    SIMPLE = "simple"  # Explicaciones muy básicas
    DETAILED = "detailed"  # Explicaciones detalladas
    STEP_BY_STEP = "step_by_step"  # Paso a paso
    CONCEPTUAL = "conceptual"  # Enfoque en conceptos
    PRACTICAL = "practical"  # Enfoque en aplicaciones prácticas
    VISUAL = "visual"  # Con énfasis en descripciones visuales


@dataclass
class AnalysisContext:
    """Contexto para el análisis de contenido educativo"""
    education_level: EducationLevel
    subject_area: Optional[str] = None
    language: str = "es"  # Español por defecto
    style: ExplanationStyle = ExplanationStyle.DETAILED
    previous_context: Optional[str] = None
    user_preferences: Optional[Dict[str, Any]] = None


@dataclass
class ExplanationResult:
    """Resultado de una explicación generada"""
    content: str
    summary: str
    key_concepts: List[str]
    difficulty_level: str
    estimated_time: int  # minutos
    follow_up_questions: List[str]
    resources: List[Dict[str, str]]
    provider_used: AIProvider
    confidence_score: float
    metadata: Dict[str, Any]


class AIProviderInterface(ABC):
    """Interfaz abstracta para proveedores de IA"""
    
    @abstractmethod
    async def analyze_image(self, image_data: bytes, context: AnalysisContext) -> Dict[str, Any]:
        """Analiza una imagen y extrae información educativa"""
        pass
    
    @abstractmethod
    async def generate_explanation(self, content: str, context: AnalysisContext) -> ExplanationResult:
        """Genera una explicación educativa adaptativa"""
        pass
    
    @abstractmethod
    async def enhance_explanation(self, explanation: str, feedback: str, context: AnalysisContext) -> str:
        """Mejora una explicación basada en feedback"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica si el proveedor está disponible"""
        pass


class OpenAIProvider(AIProviderInterface):
    """Implementación del proveedor OpenAI (GPT-4 Vision)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o"  # Modelo con capacidades de visión
        self.client = None
        
        if self.api_key:
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key)
                logger.info("OpenAI provider inicializado correctamente")
            except ImportError:
                logger.warning("OpenAI library no instalada. Instalar con: pip install openai")
            except Exception as e:
                logger.error(f"Error inicializando OpenAI: {e}")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    async def analyze_image(self, image_data: bytes, context: AnalysisContext) -> Dict[str, Any]:
        """Analiza imagen usando GPT-4 Vision"""
        if not self.is_available():
            raise RuntimeError("OpenAI provider no disponible")
        
        # Codificar imagen en base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        prompt = self._build_image_analysis_prompt(context)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente educativo experto en analizar contenido visual y extraer información relevante para crear explicaciones pedagógicas."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_analysis_response(content)
            
        except Exception as e:
            logger.error(f"Error analizando imagen con OpenAI: {e}")
            raise
    
    async def generate_explanation(self, content: str, context: AnalysisContext) -> ExplanationResult:
        """Genera explicación educativa usando GPT-4"""
        if not self.is_available():
            raise RuntimeError("OpenAI provider no disponible")
        
        prompt = self._build_explanation_prompt(content, context)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(context)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=3000,
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return self._create_explanation_result(result, AIProvider.OPENAI)
            
        except Exception as e:
            logger.error(f"Error generando explicación con OpenAI: {e}")
            raise
    
    async def enhance_explanation(self, explanation: str, feedback: str, context: AnalysisContext) -> str:
        """Mejora explicación basada en feedback"""
        if not self.is_available():
            raise RuntimeError("OpenAI provider no disponible")
        
        prompt = f"""
        Explicación actual:
        {explanation}
        
        Feedback del usuario:
        {feedback}
        
        Por favor, mejora la explicación incorporando el feedback del usuario.
        Mantén el nivel educativo: {context.education_level.value}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(context)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error mejorando explicación con OpenAI: {e}")
            raise
    
    def _build_image_analysis_prompt(self, context: AnalysisContext) -> str:
        return f"""
        Analiza esta imagen educativa y extrae:
        1. Tema o materia identificada
        2. Conceptos clave presentes
        3. Tipo de contenido (diagrama, texto, fórmula, gráfico, etc.)
        4. Nivel de complejidad estimado
        5. Elementos visuales importantes
        6. Texto visible (si hay)
        
        Contexto: Nivel educativo {context.education_level.value}, Idioma {context.language}
        
        Responde en formato JSON con las claves: subject, key_concepts, content_type, complexity, visual_elements, text_content
        """
    
    def _build_explanation_prompt(self, content: str, context: AnalysisContext) -> str:
        style_instructions = {
            ExplanationStyle.SIMPLE: "Usa lenguaje muy simple y ejemplos cotidianos",
            ExplanationStyle.DETAILED: "Proporciona explicaciones completas con múltiples niveles de detalle",
            ExplanationStyle.STEP_BY_STEP: "Divide la explicación en pasos numerados y secuenciales",
            ExplanationStyle.CONCEPTUAL: "Enfócate en la comprensión profunda de los conceptos fundamentales",
            ExplanationStyle.PRACTICAL: "Enfatiza aplicaciones prácticas y ejemplos del mundo real",
            ExplanationStyle.VISUAL: "Describe visualmente y sugiere diagramas o representaciones visuales"
        }
        
        return f"""
        Genera una explicación educativa completa sobre el siguiente contenido:
        
        {content}
        
        Parámetros:
        - Nivel educativo: {context.education_level.value}
        - Estilo: {context.style.value} - {style_instructions.get(context.style, '')}
        - Idioma: {context.language}
        {f"- Área de estudio: {context.subject_area}" if context.subject_area else ""}
        {f"- Contexto previo: {context.previous_context}" if context.previous_context else ""}
        
        Genera un JSON con la siguiente estructura:
        {{
            "content": "Explicación completa y detallada",
            "summary": "Resumen breve (2-3 oraciones)",
            "key_concepts": ["Concepto 1", "Concepto 2", ...],
            "difficulty_level": "fácil|medio|difícil|avanzado",
            "estimated_time": tiempo_estimado_en_minutos,
            "follow_up_questions": ["Pregunta 1", "Pregunta 2", ...],
            "resources": [
                {{"title": "Título del recurso", "type": "video|artículo|ejercicio", "description": "Descripción"}}
            ],
            "confidence_score": 0.0-1.0
        }}
        """
    
    def _get_system_prompt(self, context: AnalysisContext) -> str:
        level_descriptions = {
            EducationLevel.ELEMENTARY: "estudiantes de primaria (6-12 años)",
            EducationLevel.MIDDLE_SCHOOL: "estudiantes de secundaria (12-15 años)",
            EducationLevel.HIGH_SCHOOL: "estudiantes de preparatoria (15-18 años)",
            EducationLevel.UNIVERSITY: "estudiantes universitarios",
            EducationLevel.PROFESSIONAL: "profesionales y autodidactas avanzados"
        }
        
        target_audience = level_descriptions.get(context.education_level, "estudiantes")
        
        return f"""Eres TE-explico, un asistente educativo avanzado especializado en crear explicaciones pedagógicas adaptativas.

Tu objetivo es generar explicaciones claras, precisas y adaptadas al nivel de {target_audience}.

Principios pedagógicos:
1. Claridad: Usa lenguaje apropiado para el nivel educativo
2. Estructura: Organiza la información de manera lógica y progresiva
3. Contextualización: Conecta conceptos nuevos con conocimientos previos
4. Ejemplos: Proporciona ejemplos relevantes y comprensibles
5. Verificación: Incluye preguntas para verificar comprensión
6. Motivación: Muestra la relevancia y aplicación práctica

Siempre responde en {context.language} con un tono amigable pero profesional."""
    
    def _parse_analysis_response(self, content: str) -> Dict[str, Any]:
        """Parse la respuesta del análisis de imagen"""
        try:
            # Intentar extraer JSON si está embebido en texto
            if "```json" in content:
                start = content.find("```json") + 7
                end = content.find("```", start)
                content = content[start:end].strip()
            
            return json.loads(content)
        except json.JSONDecodeError:
            # Si no es JSON válido, crear estructura básica
            return {
                "subject": "No identificado",
                "key_concepts": [],
                "content_type": "text",
                "complexity": "medium",
                "visual_elements": [],
                "text_content": content
            }
    
    def _create_explanation_result(self, data: Dict[str, Any], provider: AIProvider) -> ExplanationResult:
        """Crea objeto ExplanationResult desde respuesta"""
        return ExplanationResult(
            content=data.get("content", ""),
            summary=data.get("summary", ""),
            key_concepts=data.get("key_concepts", []),
            difficulty_level=data.get("difficulty_level", "medium"),
            estimated_time=data.get("estimated_time", 10),
            follow_up_questions=data.get("follow_up_questions", []),
            resources=data.get("resources", []),
            provider_used=provider,
            confidence_score=data.get("confidence_score", 0.8),
            metadata={"raw_response": data}
        )


class AnthropicProvider(AIProviderInterface):
    """Implementación del proveedor Anthropic (Claude)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = "claude-3-5-sonnet-20241022"  # Modelo con visión
        self.client = None
        
        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
                logger.info("Anthropic provider inicializado correctamente")
            except ImportError:
                logger.warning("Anthropic library no instalada. Instalar con: pip install anthropic")
            except Exception as e:
                logger.error(f"Error inicializando Anthropic: {e}")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    async def analyze_image(self, image_data: bytes, context: AnalysisContext) -> Dict[str, Any]:
        """Analiza imagen usando Claude Vision"""
        if not self.is_available():
            raise RuntimeError("Anthropic provider no disponible")
        
        # Codificar imagen en base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Detectar tipo de imagen (simplificado)
        media_type = "image/jpeg"  # Por defecto
        if image_data[:4] == b'\x89PNG':
            media_type = "image/png"
        elif image_data[:3] == b'GIF':
            media_type = "image/gif"
        elif image_data[:4] == b'WEBP':
            media_type = "image/webp"
        
        prompt = self._build_image_analysis_prompt(context)
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system="Eres un asistente educativo experto en analizar contenido visual y extraer información relevante para crear explicaciones pedagógicas.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            content = response.content[0].text
            return self._parse_analysis_response(content)
            
        except Exception as e:
            logger.error(f"Error analizando imagen con Anthropic: {e}")
            raise
    
    async def generate_explanation(self, content: str, context: AnalysisContext) -> ExplanationResult:
        """Genera explicación educativa usando Claude"""
        if not self.is_available():
            raise RuntimeError("Anthropic provider no disponible")
        
        prompt = self._build_explanation_prompt(content, context)
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=self._get_system_prompt(context),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8
            )
            
            result_text = response.content[0].text
            result = self._extract_json_from_response(result_text)
            return self._create_explanation_result(result, AIProvider.ANTHROPIC)
            
        except Exception as e:
            logger.error(f"Error generando explicación con Anthropic: {e}")
            raise
    
    async def enhance_explanation(self, explanation: str, feedback: str, context: AnalysisContext) -> str:
        """Mejora explicación basada en feedback"""
        if not self.is_available():
            raise RuntimeError("Anthropic provider no disponible")
        
        prompt = f"""
        Explicación actual:
        {explanation}
        
        Feedback del usuario:
        {feedback}
        
        Por favor, mejora la explicación incorporando el feedback del usuario.
        Mantén el nivel educativo: {context.education_level.value}
        """
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=self._get_system_prompt(context),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error mejorando explicación con Anthropic: {e}")
            raise
    
    def _build_image_analysis_prompt(self, context: AnalysisContext) -> str:
        return OpenAIProvider(None)._build_image_analysis_prompt(context)
    
    def _build_explanation_prompt(self, content: str, context: AnalysisContext) -> str:
        return OpenAIProvider(None)._build_explanation_prompt(content, context)
    
    def _get_system_prompt(self, context: AnalysisContext) -> str:
        return OpenAIProvider(None)._get_system_prompt(context)
    
    def _parse_analysis_response(self, content: str) -> Dict[str, Any]:
        return OpenAIProvider(None)._parse_analysis_response(content)
    
    def _extract_json_from_response(self, text: str) -> Dict[str, Any]:
        """Extrae JSON de la respuesta de Claude"""
        try:
            if "```json" in text:
                start = text.find("```json") + 7
                end = text.find("```", start)
                json_str = text[start:end].strip()
            else:
                # Buscar estructura JSON en el texto
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
            
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"No se pudo extraer JSON: {e}")
            # Crear respuesta estructurada por defecto
            return {
                "content": text,
                "summary": text[:200] + "..." if len(text) > 200 else text,
                "key_concepts": [],
                "difficulty_level": "medium",
                "estimated_time": 10,
                "follow_up_questions": [],
                "resources": [],
                "confidence_score": 0.7
            }
    
    def _create_explanation_result(self, data: Dict[str, Any], provider: AIProvider) -> ExplanationResult:
        return OpenAIProvider(None)._create_explanation_result(data, provider)


class AIEngine:
    """Motor principal de IA que gestiona múltiples proveedores"""
    
    def __init__(self, 
                 openai_key: Optional[str] = None,
                 anthropic_key: Optional[str] = None,
                 default_provider: AIProvider = AIProvider.AUTO):
        
        self.providers: Dict[AIProvider, AIProviderInterface] = {}
        
        # Inicializar proveedores
        openai_provider = OpenAIProvider(openai_key)
        if openai_provider.is_available():
            self.providers[AIProvider.OPENAI] = openai_provider
            logger.info("✓ OpenAI provider disponible")
        
        anthropic_provider = AnthropicProvider(anthropic_key)
        if anthropic_provider.is_available():
            self.providers[AIProvider.ANTHROPIC] = anthropic_provider
            logger.info("✓ Anthropic provider disponible")
        
        if not self.providers:
            logger.warning("⚠ No hay proveedores de IA disponibles. Configura las API keys.")
        
        self.default_provider = default_provider
        self._usage_stats: Dict[AIProvider, int] = {p: 0 for p in AIProvider}
    
    def _select_provider(self, preferred: AIProvider = AIProvider.AUTO) -> AIProviderInterface:
        """Selecciona el proveedor óptimo"""
        if preferred != AIProvider.AUTO and preferred in self.providers:
            return self.providers[preferred]
        
        # Selección automática: preferir Anthropic para análisis visual, OpenAI para texto
        if AIProvider.ANTHROPIC in self.providers:
            return self.providers[AIProvider.ANTHROPIC]
        elif AIProvider.OPENAI in self.providers:
            return self.providers[AIProvider.OPENAI]
        
        raise RuntimeError("No hay proveedores de IA disponibles")
    
    async def analyze_screenshot(self, 
                                 image_data: bytes,
                                 context: Optional[AnalysisContext] = None,
                                 provider: AIProvider = AIProvider.AUTO) -> Dict[str, Any]:
        """
        Analiza un screenshot y extrae información educativa
        
        Args:
            image_data: Datos binarios de la imagen
            context: Contexto para el análisis
            provider: Proveedor de IA a utilizar
            
        Returns:
            Diccionario con información extraída
        """
        if context is None:
            context = AnalysisContext(education_level=EducationLevel.AUTO)
        
        selected_provider = self._select_provider(provider)
        provider_type = next(k for k, v in self.providers.items() if v == selected_provider)
        
        logger.info(f"Analizando screenshot con {provider_type.value}")
        
        try:
            result = await selected_provider.analyze_image(image_data, context)
            self._usage_stats[provider_type] += 1
            
            # Auto-detectar nivel educativo si está en AUTO
            if context.education_level == EducationLevel.AUTO:
                context.education_level = self._detect_education_level(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error en análisis: {e}")
            # Intentar con proveedor alternativo
            if len(self.providers) > 1:
                logger.info("Intentando con proveedor alternativo...")
                alt_provider = self._get_alternative_provider(provider_type)
                if alt_provider:
                    return await alt_provider.analyze_image(image_data, context)
            raise
    
    async def generate_explanation(self,
                                   content: str,
                                   context: Optional[AnalysisContext] = None,
                                   provider: AIProvider = AIProvider.AUTO) -> ExplanationResult:
        """
        Genera una explicación educativa completa
        
        Args:
            content: Contenido a explicar (texto o análisis previo)
            context: Contexto para la explicación
            provider: Proveedor de IA a utilizar
            
        Returns:
            ExplanationResult con la explicación generada
        """
        if context is None:
            context = AnalysisContext(
                education_level=EducationLevel.HIGH_SCHOOL,
                style=ExplanationStyle.DETAILED
            )
        
        selected_provider = self._select_provider(provider)
        provider_type = next(k for k, v in self.providers.items() if v == selected_provider)
        
        logger.info(f"Generando explicación con {provider_type.value}")
        
        try:
            result = await selected_provider.generate_explanation(content, context)
            self._usage_stats[provider_type] += 1
            return result
            
        except Exception as e:
            logger.error(f"Error generando explicación: {e}")
            # Intentar con proveedor alternativo
            if len(self.providers) > 1:
                logger.info("Intentando con proveedor alternativo...")
                alt_provider = self._get_alternative_provider(provider_type)
                if alt_provider:
                    return await alt_provider.generate_explanation(content, context)
            raise
    
    async def explain_screenshot(self,
                                image_data: bytes,
                                context: Optional[AnalysisContext] = None,
                                provider: AIProvider = AIProvider.AUTO) -> ExplanationResult:
        """
        Pipeline completo: analiza screenshot y genera explicación
        
        Args:
            image_data: Datos binarios de la imagen
            context: Contexto para análisis y explicación
            provider: Proveedor de IA a utilizar
            
        Returns:
            ExplanationResult con explicación completa
        """
        if context is None:
            context = AnalysisContext(
                education_level=EducationLevel.AUTO,
                style=ExplanationStyle.DETAILED
            )
        
        logger.info("🎓 Iniciando pipeline de explicación de screenshot")
        
        # Paso 1: Analizar imagen
        analysis = await self.analyze_screenshot(image_data, context, provider)
        logger.info(f"✓ Análisis completado: {analysis.get('subject', 'tema detectado')}")
        
        # Paso 2: Enriquecer contexto con análisis
        if context.subject_area is None:
            context.subject_area = analysis.get('subject', 'General')
        
        # Paso 3: Generar explicación
        content_to_explain = self._build_content_from_analysis(analysis)
        explanation = await self.generate_explanation(content_to_explain, context, provider)
        
        # Paso 4: Enriquecer con información del análisis
        explanation.metadata['image_analysis'] = analysis
        
        logger.info("✓ Explicación generada exitosamente")
        return explanation
    
    async def enhance_explanation(self,
                                 explanation: str,
                                 feedback: str,
                                 context: Optional[AnalysisContext] = None,
                                 provider: AIProvider = AIProvider.AUTO) -> str:
        """
        Mejora una explicación basada en feedback del usuario
        
        Args:
            explanation: Explicación original
            feedback: Feedback del usuario
            context: Contexto educativo
            provider: Proveedor de IA a utilizar
            
        Returns:
            Explicación mejorada
        """
        if context is None:
            context = AnalysisContext(education_level=EducationLevel.AUTO)
        
        selected_provider = self._select_provider(provider)
        provider_type = next(k for k, v in self.providers.items() if v == selected_provider)
        
        logger.info(f"Mejorando explicación con {provider_type.value}")
        
        result = await selected_provider.enhance_explanation(explanation, feedback, context)
        self._usage_stats[provider_type] += 1
        return result
    
    def _detect_education_level(self, analysis: Dict[str, Any]) -> EducationLevel:
        """Detecta el nivel educativo basado en el análisis"""
        complexity = analysis.get('complexity', 'medium').lower()
        
        complexity_map = {
            'very_simple': EducationLevel.ELEMENTARY,
            'simple': EducationLevel.MIDDLE_SCHOOL,
            'medium': EducationLevel.HIGH_SCHOOL,
            'complex': EducationLevel.UNIVERSITY,
            'very_complex': EducationLevel.PROFESSIONAL
        }
        
        return complexity_map.get(complexity, EducationLevel.HIGH_SCHOOL)
    
    def _get_alternative_provider(self, current: AIProvider) -> Optional[AIProviderInterface]:
        """Obtiene un proveedor alternativo"""
        for provider_type, provider in self.providers.items():
            if provider_type != current:
                return provider
        return None
    
    def _build_content_from_analysis(self, analysis: Dict[str, Any]) -> str:
        """Construye contenido para explicación desde análisis"""
        parts = []
        
        if 'subject' in analysis:
            parts.append(f"Tema: {analysis['subject']}")
        
        if 'text_content' in analysis and analysis['text_content']:
            parts.append(f"\nContenido textual:\n{analysis['text_content']}")
        
        if 'key_concepts' in analysis and analysis['key_concepts']:
            concepts = ', '.join(analysis['key_concepts'])
            parts.append(f"\nConceptos identificados: {concepts}")
        
        if 'content_type' in analysis:
            parts.append(f"\nTipo de contenido: {analysis['content_type']}")
        
        return '\n'.join(parts)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de uso"""
        return {
            'providers_available': list(self.providers.keys()),
            'usage_count': {k.value: v for k, v in self._usage_stats.items()},
            'total_requests': sum(self._usage_stats.values())
        }
    
    def is_ready(self) -> bool:
        """Verifica si el motor está listo para usar"""
        return len(self.providers) > 0


# Funciones de utilidad

def create_engine(openai_key: Optional[str] = None,
                 anthropic_key: Optional[str] = None) -> AIEngine:
    """
    Factory function para crear un motor de IA configurado
    
    Args:
        openai_key: API key de OpenAI (opcional, usa variable de entorno)
        anthropic_key: API key de Anthropic (opcional, usa variable de entorno)
        
    Returns:
        AIEngine configurado
    """
    return AIEngine(openai_key=openai_key, anthropic_key=anthropic_key)


async def quick_explain(image_path: str,
                       level: EducationLevel = EducationLevel.HIGH_SCHOOL,
                       style: ExplanationStyle = ExplanationStyle.DETAILED,
                       language: str = "es") -> ExplanationResult:
    """
    Función rápida para explicar una imagen desde archivo
    
    Args:
        image_path: Ruta al archivo de imagen
        level: Nivel educativo
        style: Estilo de explicación
        language: Idioma
        
    Returns:
        ExplanationResult
    """
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    engine = create_engine()
    context = AnalysisContext(
        education_level=level,
        style=style,
        language=language
    )
    
    return await engine.explain_screenshot(image_data, context)


# Ejemplo de uso
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        """Demostración del motor de IA"""
        print("🎓 TE-explico - Motor de IA Educativo")
        print("=" * 50)
        
        # Crear motor
        engine = create_engine()
        
        if not engine.is_ready():
            print("⚠ Configura las API keys:")
            print("  export OPENAI_API_KEY='tu-key'")
            print("  export ANTHROPIC_API_KEY='tu-key'")
            return
        
        print(f"✓ Motor inicializado con {len(engine.providers)} proveedores")
        print(f"  Disponibles: {[p.value for p in engine.providers.keys()]}")
        print()
        
        # Ejemplo de explicación de texto
        context = AnalysisContext(
            education_level=EducationLevel.HIGH_SCHOOL,
            subject_area="Matemáticas",
            style=ExplanationStyle.STEP_BY_STEP,
            language="es"
        )
        
        content = """
        Resolver la ecuación cuadrática: x² + 5x + 6 = 0
        """
        
        print("📝 Generando explicación...")
        result = await engine.generate_explanation(content, context)
        
        print(f"\n✓ Explicación generada ({result.provider_used.value})")
        print(f"  Nivel: {result.difficulty_level}")
        print(f"  Tiempo estimado: {result.estimated_time} min")
        print(f"  Confianza: {result.confidence_score:.0%}")
        print()
        print("Resumen:")
        print(result.summary)
        print()
        print("Conceptos clave:")
        for concept in result.key_concepts:
            print(f"  • {concept}")
        print()
        
        # Estadísticas
        stats = engine.get_statistics()
        print("📊 Estadísticas:")
        print(f"  Total de solicitudes: {stats['total_requests']}")
        
    # Ejecutar demo
    asyncio.run(demo())

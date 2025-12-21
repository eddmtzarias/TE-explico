"""
Motor OCR de OmniMaestro

Integración con Tesseract OCR para extracción de texto de imágenes.
Soporta múltiples idiomas y optimización de procesamiento.
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from PIL import Image
import io

# Configuración de logging
logger = logging.getLogger(__name__)

class OCREngine:
    """
    Motor de OCR para extracción de texto de imágenes.
    
    Utiliza Tesseract OCR con optimizaciones para capturas de pantalla.
    """
    
    def __init__(self, languages: List[str] = None, config: str = "--psm 6"):
        """
        Inicializa el motor OCR.
        
        Args:
            languages: Lista de idiomas a reconocer (ej: ['eng', 'spa'])
            config: Configuración de Tesseract PSM (Page Segmentation Mode)
                   --psm 6: Asume un bloque de texto uniforme (recomendado para capturas)
        """
        self.languages = languages or ['eng', 'spa']
        self.config = config
        self._tesseract_available = False
        self._check_tesseract()
    
    def _check_tesseract(self) -> bool:
        """
        Verifica si Tesseract está instalado y disponible.
        
        Returns:
            bool: True si Tesseract está disponible
        """
        try:
            import pytesseract
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract OCR v{version} detectado")
            self._tesseract_available = True
            return True
        except Exception as e:
            logger.error(f"Tesseract no disponible: {e}")
            logger.warning("Instala Tesseract: https://github.com/tesseract-ocr/tesseract")
            self._tesseract_available = False
            return False
    
    def extract_text(self, image_path: str, preprocess: bool = True) -> Optional[str]:
        """
        Extrae texto de una imagen.
        
        Args:
            image_path: Ruta a la imagen
            preprocess: Si debe preprocesar la imagen para mejor OCR
        
        Returns:
            str: Texto extraído o None si falla
        """
        if not self._tesseract_available:
            logger.error("Tesseract no está disponible. No se puede extraer texto.")
            return None
        
        try:
            import pytesseract
            
            # Cargar imagen
            image = Image.open(image_path)
            
            # Preprocesar si se solicita
            if preprocess:
                image = self._preprocess_image(image)
            
            # Configurar idiomas
            lang_str = '+'.join(self.languages)
            
            # Extraer texto
            text = pytesseract.image_to_string(
                image,
                lang=lang_str,
                config=self.config
            )
            
            logger.info(f"Texto extraído: {len(text)} caracteres")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extrayendo texto: {e}")
            return None
    
    def extract_text_with_confidence(
        self, 
        image_path: str, 
        preprocess: bool = True
    ) -> Optional[Dict]:
        """
        Extrae texto con información de confianza.
        
        Args:
            image_path: Ruta a la imagen
            preprocess: Si debe preprocesar la imagen
        
        Returns:
            dict: Diccionario con 'text', 'confidence', 'words'
        """
        if not self._tesseract_available:
            return None
        
        try:
            import pytesseract
            
            image = Image.open(image_path)
            
            if preprocess:
                image = self._preprocess_image(image)
            
            lang_str = '+'.join(self.languages)
            
            # Obtener datos detallados
            data = pytesseract.image_to_data(
                image,
                lang=lang_str,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extraer palabras con confianza > 0
            words = []
            confidences = []
            
            for i, conf in enumerate(data['conf']):
                if conf > 0:
                    words.append(data['text'][i])
                    confidences.append(conf)
            
            text = ' '.join(words)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'text': text,
                'confidence': avg_confidence,
                'words': list(zip(words, confidences)),
                'word_count': len(words)
            }
            
        except Exception as e:
            logger.error(f"Error extrayendo texto con confianza: {e}")
            return None
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocesa imagen para mejorar OCR.
        
        Args:
            image: Imagen PIL
        
        Returns:
            Image: Imagen preprocesada
        """
        try:
            from PIL import ImageEnhance, ImageFilter
            
            # Convertir a escala de grises
            image = image.convert('L')
            
            # Aumentar contraste
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Aumentar nitidez
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            
            # Reducir ruido
            image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return image
            
        except Exception as e:
            logger.warning(f"Error en preprocesamiento: {e}. Usando imagen original.")
            return image
    
    def extract_from_region(
        self, 
        image_path: str, 
        region: Tuple[int, int, int, int]
    ) -> Optional[str]:
        """
        Extrae texto de una región específica de la imagen.
        
        Args:
            image_path: Ruta a la imagen
            region: Tupla (x, y, width, height) de la región
        
        Returns:
            str: Texto extraído de la región
        """
        try:
            image = Image.open(image_path)
            
            # Recortar región
            x, y, w, h = region
            cropped = image.crop((x, y, x + w, y + h))
            
            # Guardar temporalmente y extraer
            temp_path = Path(image_path).parent / "temp_crop.png"
            cropped.save(temp_path)
            
            text = self.extract_text(str(temp_path))
            
            # Limpiar archivo temporal
            temp_path.unlink(missing_ok=True)
            
            return text
            
        except Exception as e:
            logger.error(f"Error extrayendo de región: {e}")
            return None
    
    def detect_language(self, image_path: str) -> Optional[str]:
        """
        Detecta el idioma predominante en una imagen.
        
        Args:
            image_path: Ruta a la imagen
        
        Returns:
            str: Código de idioma detectado (ej: 'eng', 'spa')
        """
        if not self._tesseract_available:
            return None
        
        try:
            import pytesseract
            
            image = Image.open(image_path)
            osd = pytesseract.image_to_osd(image)
            
            # Parsear resultado
            for line in osd.split('\n'):
                if 'Script:' in line:
                    script = line.split(':')[1].strip()
                    logger.info(f"Idioma detectado: {script}")
                    return script
            
            return None
            
        except Exception as e:
            logger.warning(f"No se pudo detectar idioma: {e}")
            return None


# Instancia global (singleton)
_ocr_engine_instance = None

def get_ocr_engine(languages: List[str] = None) -> OCREngine:
    """
    Obtiene la instancia global del motor OCR.
    
    Args:
        languages: Lista de idiomas (solo se usa en primera llamada)
    
    Returns:
        OCREngine: Instancia del motor OCR
    """
    global _ocr_engine_instance
    
    if _ocr_engine_instance is None:
        _ocr_engine_instance = OCREngine(languages=languages)
    
    return _ocr_engine_instance
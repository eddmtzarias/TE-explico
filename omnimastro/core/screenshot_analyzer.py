"""
Screenshot Analyzer Module
Integrates OCR and image analysis for educational content extraction.
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import base64
from io import BytesIO

try:
    from PIL import Image, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL/Pillow not available. Image preprocessing will be limited.")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("pytesseract not available. OCR functionality will be limited.")

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logging.warning("OpenCV not available. Advanced image processing will be limited.")


logger = logging.getLogger(__name__)


class ScreenshotAnalyzer:
    """
    Analyzes screenshots to extract text, diagrams, formulas, and educational content.
    Combines OCR with image analysis for comprehensive content extraction.
    """
    
    def __init__(self, tesseract_cmd: Optional[str] = None, language: str = 'spa'):
        """
        Initialize the Screenshot Analyzer.
        
        Args:
            tesseract_cmd: Path to tesseract executable (optional)
            language: OCR language code (default: 'spa' for Spanish)
        """
        self.language = language
        
        if TESSERACT_AVAILABLE and tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp']
        
        logger.info(f"ScreenshotAnalyzer initialized with language: {language}")
        logger.info(f"PIL Available: {PIL_AVAILABLE}, Tesseract: {TESSERACT_AVAILABLE}, OpenCV: {CV2_AVAILABLE}")
    
    def analyze_screenshot(self, image_path: str) -> Dict[str, Any]:
        """
        Main method to analyze a screenshot comprehensively.
        
        Args:
            image_path: Path to the screenshot image
            
        Returns:
            Dictionary containing analysis results
        """
        logger.info(f"Analyzing screenshot: {image_path}")
        
        if not PIL_AVAILABLE:
            return {"error": "PIL/Pillow is not available"}
        
        try:
            image = Image.open(image_path)
            
            # Perform various analyses
            results = {
                "image_info": self._get_image_info(image),
                "text_extraction": self._extract_text(image),
                "content_detection": self._detect_content_types(image),
                "text_regions": self._detect_text_regions(image),
                "quality_assessment": self._assess_quality(image),
                "educational_elements": self._detect_educational_elements(image)
            }
            
            logger.info("Screenshot analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing screenshot: {e}")
            return {"error": str(e)}
    
    def _get_image_info(self, image: Image.Image) -> Dict[str, Any]:
        """Extract basic image information."""
        return {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
            "size_bytes": len(image.tobytes())
        }
    
    def _extract_text(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract text from image using OCR.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if not TESSERACT_AVAILABLE:
            return {
                "text": "",
                "confidence": 0,
                "method": "unavailable",
                "error": "Tesseract not available"
            }
        
        try:
            # Preprocess image for better OCR
            processed_image = self._preprocess_for_ocr(image)
            
            # Extract text with details
            text = pytesseract.image_to_string(
                processed_image,
                lang=self.language,
                config='--psm 6'  # Assume uniform text block
            )
            
            # Get confidence scores
            data = pytesseract.image_to_data(
                processed_image,
                lang=self.language,
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Extract words with positions
            words = []
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                if int(data['conf'][i]) > 60:  # Confidence threshold
                    words.append({
                        "text": data['text'][i],
                        "confidence": int(data['conf'][i]),
                        "bbox": {
                            "x": data['left'][i],
                            "y": data['top'][i],
                            "width": data['width'][i],
                            "height": data['height'][i]
                        }
                    })
            
            return {
                "text": text.strip(),
                "confidence": avg_confidence,
                "word_count": len(text.split()),
                "words": words,
                "method": "tesseract_ocr"
            }
            
        except Exception as e:
            logger.error(f"Error in text extraction: {e}")
            return {
                "text": "",
                "confidence": 0,
                "error": str(e)
            }
    
    def _preprocess_for_ocr(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image to improve OCR accuracy.
        
        Args:
            image: Original PIL Image
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to grayscale
        gray = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(2.0)
        
        # Sharpen
        sharpened = enhanced.filter(ImageFilter.SHARPEN)
        
        # Optional: Apply threshold for better text detection
        # This converts to pure black and white
        threshold = 150
        processed = sharpened.point(lambda x: 0 if x < threshold else 255, '1')
        
        return processed
    
    def _detect_text_regions(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Detect regions in the image that contain text.
        
        Args:
            image: PIL Image object
            
        Returns:
            List of text region bounding boxes
        """
        if not CV2_AVAILABLE:
            return []
        
        try:
            # Convert PIL to OpenCV format
            img_array = np.array(image)
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, 11, 2
            )
            
            # Find contours
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            
            # Filter and extract text regions
            regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by size (likely text regions)
                if w > 20 and h > 10 and w < image.width * 0.9:
                    regions.append({
                        "bbox": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                        "area": int(w * h),
                        "aspect_ratio": float(w / h) if h > 0 else 0
                    })
            
            # Sort by position (top to bottom, left to right)
            regions.sort(key=lambda r: (r["bbox"]["y"], r["bbox"]["x"]))
            
            return regions
            
        except Exception as e:
            logger.error(f"Error detecting text regions: {e}")
            return []
    
    def _detect_content_types(self, image: Image.Image) -> Dict[str, bool]:
        """
        Detect types of content present in the image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary indicating presence of different content types
        """
        content_types = {
            "has_text": False,
            "has_diagrams": False,
            "has_charts": False,
            "has_formulas": False,
            "has_code": False,
            "has_tables": False
        }
        
        if not TESSERACT_AVAILABLE:
            return content_types
        
        try:
            # Extract text for analysis
            text_result = self._extract_text(image)
            text = text_result.get("text", "")
            
            # Check for text
            content_types["has_text"] = len(text.strip()) > 0
            
            # Check for mathematical formulas (common indicators)
            formula_indicators = ['=', '∫', '∑', '√', '±', 'dx', 'dy', 'π', 'α', 'β', 'θ']
            content_types["has_formulas"] = any(indicator in text for indicator in formula_indicators)
            
            # Check for code (common programming keywords)
            code_indicators = ['def ', 'function', 'class ', 'import ', 'return', 'if ', 'for ', 'while ']
            content_types["has_code"] = any(indicator in text.lower() for indicator in code_indicators)
            
            # Check for table indicators
            table_indicators = ['|', '─', '│', '┌', '┐', '└', '┘']
            content_types["has_tables"] = any(indicator in text for indicator in table_indicators)
            
            # Use image analysis for diagrams and charts
            if CV2_AVAILABLE:
                img_array = np.array(image.convert('L'))
                
                # Detect lines (common in diagrams and charts)
                edges = cv2.Canny(img_array, 50, 150)
                lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)
                
                if lines is not None and len(lines) > 10:
                    content_types["has_diagrams"] = True
                
                # Detect circles (common in diagrams)
                circles = cv2.HoughCircles(img_array, cv2.HOUGH_GRADIENT, 1, 20,
                                          param1=50, param2=30, minRadius=10, maxRadius=100)
                
                if circles is not None and len(circles) > 0:
                    content_types["has_diagrams"] = True
            
            return content_types
            
        except Exception as e:
            logger.error(f"Error detecting content types: {e}")
            return content_types
    
    def _assess_quality(self, image: Image.Image) -> Dict[str, Any]:
        """
        Assess the quality of the screenshot for text extraction.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with quality metrics
        """
        quality = {
            "resolution": "unknown",
            "clarity": "unknown",
            "brightness": 0,
            "contrast": 0,
            "suitable_for_ocr": False
        }
        
        try:
            # Check resolution
            pixels = image.width * image.height
            if pixels >= 1920 * 1080:
                quality["resolution"] = "high"
            elif pixels >= 1280 * 720:
                quality["resolution"] = "medium"
            else:
                quality["resolution"] = "low"
            
            # Convert to grayscale for analysis
            gray = image.convert('L')
            img_array = np.array(gray)
            
            # Calculate brightness (average pixel value)
            brightness = np.mean(img_array)
            quality["brightness"] = float(brightness)
            
            # Calculate contrast (standard deviation)
            contrast = np.std(img_array)
            quality["contrast"] = float(contrast)
            
            # Assess clarity using Laplacian variance (blur detection)
            if CV2_AVAILABLE:
                laplacian_var = cv2.Laplacian(img_array, cv2.CV_64F).var()
                quality["clarity_score"] = float(laplacian_var)
                quality["clarity"] = "sharp" if laplacian_var > 100 else "blurry"
            
            # Overall suitability for OCR
            quality["suitable_for_ocr"] = (
                quality["resolution"] in ["high", "medium"] and
                quality["contrast"] > 30 and
                50 < brightness < 200
            )
            
            return quality
            
        except Exception as e:
            logger.error(f"Error assessing quality: {e}")
            return quality
    
    def _detect_educational_elements(self, image: Image.Image) -> Dict[str, Any]:
        """
        Detect specific educational elements in the screenshot.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with detected educational elements
        """
        elements = {
            "topics": [],
            "question_detected": False,
            "answer_detected": False,
            "step_by_step": False,
            "has_examples": False,
            "language": self.language
        }
        
        if not TESSERACT_AVAILABLE:
            return elements
        
        try:
            text = self._extract_text(image).get("text", "").lower()
            
            # Detect questions
            question_markers = ['?', '¿', 'pregunta', 'cuestión', 'problema', 'ejercicio']
            elements["question_detected"] = any(marker in text for marker in question_markers)
            
            # Detect answers
            answer_markers = ['respuesta:', 'solución:', 'resultado:', 'answer:']
            elements["answer_detected"] = any(marker in text for marker in answer_markers)
            
            # Detect step-by-step content
            step_markers = ['paso 1', 'paso 2', 'step 1', 'step 2', '1)', '2)', '3)']
            elements["step_by_step"] = any(marker in text for marker in step_markers)
            
            # Detect examples
            example_markers = ['ejemplo:', 'por ejemplo', 'example:', 'for example']
            elements["has_examples"] = any(marker in text for marker in example_markers)
            
            # Detect subject topics (basic keyword detection)
            topics_keywords = {
                'mathematics': ['matemática', 'ecuación', 'álgebra', 'geometría', 'cálculo'],
                'physics': ['física', 'fuerza', 'energía', 'velocidad', 'movimiento'],
                'chemistry': ['química', 'átomo', 'molécula', 'reacción', 'elemento'],
                'biology': ['biología', 'célula', 'organismo', 'genética', 'evolución'],
                'programming': ['código', 'programa', 'función', 'variable', 'algoritmo']
            }
            
            for topic, keywords in topics_keywords.items():
                if any(keyword in text for keyword in keywords):
                    elements["topics"].append(topic)
            
            return elements
            
        except Exception as e:
            logger.error(f"Error detecting educational elements: {e}")
            return elements
    
    def extract_and_explain(self, image_path: str) -> Dict[str, Any]:
        """
        Extract content and provide a structured explanation.
        
        Args:
            image_path: Path to the screenshot
            
        Returns:
            Dictionary with extracted content and explanation structure
        """
        analysis = self.analyze_screenshot(image_path)
        
        if "error" in analysis:
            return analysis
        
        # Build structured explanation
        explanation = {
            "extracted_text": analysis["text_extraction"].get("text", ""),
            "content_summary": {
                "type": self._determine_content_type(analysis),
                "topics": analysis["educational_elements"].get("topics", []),
                "complexity": self._estimate_complexity(analysis)
            },
            "teaching_suggestions": self._generate_teaching_suggestions(analysis),
            "quality_notes": self._get_quality_notes(analysis),
            "raw_analysis": analysis
        }
        
        return explanation
    
    def _determine_content_type(self, analysis: Dict[str, Any]) -> str:
        """Determine the primary type of content in the screenshot."""
        content_detection = analysis.get("content_detection", {})
        
        if content_detection.get("has_code"):
            return "programming"
        elif content_detection.get("has_formulas"):
            return "mathematical"
        elif content_detection.get("has_diagrams"):
            return "visual_diagram"
        elif content_detection.get("has_tables"):
            return "tabular_data"
        elif content_detection.get("has_text"):
            return "text_content"
        else:
            return "unknown"
    
    def _estimate_complexity(self, analysis: Dict[str, Any]) -> str:
        """Estimate the complexity level of the content."""
        text = analysis["text_extraction"].get("text", "")
        word_count = len(text.split())
        
        has_formulas = analysis["content_detection"].get("has_formulas", False)
        has_diagrams = analysis["content_detection"].get("has_diagrams", False)
        
        if word_count > 200 or has_formulas or has_diagrams:
            return "advanced"
        elif word_count > 100:
            return "intermediate"
        else:
            return "basic"
    
    def _generate_teaching_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate suggestions for teaching based on the content."""
        suggestions = []
        
        content_type = self._determine_content_type(analysis)
        educational = analysis.get("educational_elements", {})
        
        if educational.get("question_detected"):
            suggestions.append("Identificar la pregunta principal y desglosarla")
        
        if educational.get("step_by_step"):
            suggestions.append("Seguir el proceso paso a paso presentado")
        
        if content_type == "mathematical":
            suggestions.append("Explicar conceptos matemáticos con ejemplos prácticos")
        
        if content_type == "programming":
            suggestions.append("Demostrar el código con ejemplos ejecutables")
        
        if analysis["content_detection"].get("has_diagrams"):
            suggestions.append("Utilizar el diagrama para explicación visual")
        
        return suggestions if suggestions else ["Revisar el contenido extraído y estructurar la explicación"]
    
    def _get_quality_notes(self, analysis: Dict[str, Any]) -> List[str]:
        """Get notes about the quality of the screenshot."""
        notes = []
        quality = analysis.get("quality_assessment", {})
        
        if not quality.get("suitable_for_ocr"):
            notes.append("⚠️ La calidad de la imagen puede afectar la extracción de texto")
        
        if quality.get("clarity") == "blurry":
            notes.append("⚠️ Imagen desenfocada, considerar una captura más nítida")
        
        if quality.get("resolution") == "low":
            notes.append("⚠️ Resolución baja, preferible usar imágenes de mayor calidad")
        
        confidence = analysis["text_extraction"].get("confidence", 0)
        if confidence < 70:
            notes.append(f"⚠️ Confianza de OCR baja ({confidence:.1f}%), verificar texto extraído")
        
        if not notes:
            notes.append("✓ Calidad de imagen adecuada para análisis")
        
        return notes


def main():
    """Example usage of ScreenshotAnalyzer."""
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) < 2:
        print("Usage: python screenshot_analyzer.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    analyzer = ScreenshotAnalyzer(language='spa')
    result = analyzer.extract_and_explain(image_path)
    
    print("\n=== SCREENSHOT ANALYSIS ===")
    print(f"\nExtracted Text:\n{result.get('extracted_text', 'N/A')}")
    print(f"\nContent Type: {result['content_summary']['type']}")
    print(f"Topics: {', '.join(result['content_summary']['topics'])}")
    print(f"Complexity: {result['content_summary']['complexity']}")
    
    print("\nTeaching Suggestions:")
    for suggestion in result['teaching_suggestions']:
        print(f"  - {suggestion}")
    
    print("\nQuality Notes:")
    for note in result['quality_notes']:
        print(f"  {note}")


if __name__ == "__main__":
    main()

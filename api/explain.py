"""
Vercel Function: /api/explain
Genera explicaciones pedagógicas de texto
"""
from http.server import BaseHTTPRequestHandler
import json
import os

# Import solo lo necesario (sin OCR para reducir bundle)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST /api/explain"""
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            text = data.get('text', '')
            context = data.get('context', '')
            user_level = data.get('user_level', 'beginner')
            
            if not text:
                # Send JSON error response
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    'error': "Missing 'text' parameter",
                    'status': 'error'
                }
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
            
            # Generate explanation
            explanation = self.generate_explanation(text, context, user_level)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'explanation': explanation,
                'provider': 'openai',
                'model': 'gpt-4o-mini',
                'status': 'success'
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {
                'error': str(e),
                'status': 'error'
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def generate_explanation(self, text: str, context: str, user_level: str) -> str:
        """Generate explanation using OpenAI"""
        if not OPENAI_AVAILABLE:
            return "Error: OpenAI library not available"
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Error: OPENAI_API_KEY not configured in Vercel environment variables"
        
        client = openai.OpenAI(api_key=api_key)
        
        system_prompt = f"""Eres OmniMaestro, un asistente pedagógico que explica interfaces de software. 

Usuario: Nivel {user_level}
Tono: Amigable, paciente, alentador

SIEMPRE estructura tu respuesta así:
1. **Explicación Técnica**: Nombre correcto y definición formal
2. **En lenguaje simple**: Analogía o explicación coloquial
3. **¿Para qué sirve?**: Utilidad práctica
4. **Próximos pasos**: 2-3 acciones sugeridas

Contexto: {context or 'Usuario explorando software'}
"""
        
        user_prompt = f"""Texto de la pantalla: 
{text}

Explica qué significa esto y cómo puede ayudar al usuario."""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating explanation: {str(e)}"

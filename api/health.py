"""
Vercel Function: /api/health
Simple health check
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET /api/health"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'healthy',
            'service': 'OmniMaestro API',
            'version': '1.0.0'
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))

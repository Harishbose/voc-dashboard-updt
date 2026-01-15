#!/usr/bin/env python3
"""
Minimal VOC Dashboard Server - Ultra Simple Version
"""

import http.server
import socketserver
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/Original%20Code.html'
        return super().do_GET()

try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("\n" + "="*60)
        print("VOC DASHBOARD SERVER RUNNING")
        print("="*60)
        print(f"\nOpen in browser: http://localhost:{PORT}")
        print("\nPress Ctrl+C to stop\n")
        httpd.serve_forever()
        
except KeyboardInterrupt:
    print("\n\nServer stopped.")
    sys.exit(0)
except OSError as e:
    print(f"\nError: {e}")
    print(f"Port {PORT} may already be in use.")
    print("Try a different port or close other applications.")
    input("Press Enter to exit...")
    sys.exit(1)

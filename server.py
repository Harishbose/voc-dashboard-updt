#!/usr/bin/env python3
"""
Simple HTTP Server for VOC Dashboard
Run this script to access the dashboard at:
http://localhost:8000 (local machine)
http://YOUR_IP:8000 (from other machines on network)
"""

import http.server
import socketserver
import os
import webbrowser
import socket

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    
    local_ip = get_local_ip()
    
    print("=" * 70)
    print("🎯 VOC DASHBOARD SERVER STARTED")
    print("=" * 70)
    print(f"\n📱 Local Access (This Machine):")
    print(f"   👉 http://localhost:{PORT}")
    print(f"\n🌐 Network Access (Share with Others):")
    print(f"   👉 http://{local_ip}:{PORT}")
    print(f"\n📁 Dashboard Location: {DIRECTORY}")
    print("\n💡 Instructions to Share:")
    print(f"   1. Share the link: http://{local_ip}:{PORT}")
    print("   2. Make sure this script keeps running")
    print("   3. Others on your network can access it via that IP")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    # Open browser automatically
    webbrowser.open(f"http://localhost:{PORT}/Original%20Code.html")
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped.")

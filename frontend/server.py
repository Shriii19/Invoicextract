"""
Simple static file server for the InvoiceXtract frontend.
Run from the repo root:  python frontend/server.py
Or from inside frontend/:  python server.py
"""
import http.server
import os
import socketserver

PORT = 3000

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Frontend running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()

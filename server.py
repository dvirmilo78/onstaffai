import http.server
import socketserver
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/OnStaffAI.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Change to the directory containing the HTML files
os.chdir('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow')

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()

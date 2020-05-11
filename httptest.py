import http.server
import socketserver
import urllib.parse

import webbrowser

PORT = 8000

class HandleRequests(http.server.BaseHTTPRequestHandler):
    PATH = 'index.html'

    def handleData(self, data):
        print(data)

    handleData = handleData

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        self._set_headers()
        
        file = None
        if self.path == '/':
            file = open(self.PATH, 'rb')
        elif self.path != '/favicon.ico':
            file = open('.' + self.path, 'rb')
        
        if self.path != '/favicon.ico':
            self.wfile.write(file.read())

    def do_POST(self):
        self._set_headers()
        contentLen = int(self.headers.get('content-length', 0))
        content = self.rfile.read(contentLen).decode('utf-8')

        contentDict = {}

        for i in content.split('&'):            
            key = i.split('=')[0]
            data = i.split('=')[1]
            
            data = data.replace('+', ' ')
            data = urllib.parse.unquote(data)

            contentDict[key] = data
        
        self.handleData(contentDict)

    def do_PUT(self):
        self.do_POST()

def setupServer(port, requestHandler):
    with socketserver.TCPServer(('', port), requestHandler) as httpd:
        webbrowser.open('http://localhost:' + str(port) + '/')

        print('port ' + str(port))
        httpd.serve_forever()

def main():
    handleRequests = HandleRequests
    setupServer(PORT, handleRequests)

if __name__ == "__main__":
    main()
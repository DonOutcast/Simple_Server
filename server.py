from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from io import BytesIO

class HttpGetHandler(BaseHTTPRequestHandler):
    def _headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def _html(self, message):
         
        content = f"""
                        <html>
                              <head>
                                    <meta charset='utf-8'>
                                    <title>
                                            Простой HTTP-сервер
                                    </title>
                              </head>
                              <body>
                                    <h1>
                                        {message}
                                    </h1>
                              </body>
                        </html>
                    """
                    
        return content.encode("utf8")

    def do_GET(self):
        self._headers()
        message = "Hello, World!"
        self.wfile.write(self._html(message))
    
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str({"POST": True}).encode("utf8"))
        
    def do_PUT(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")    
        self.end_headers()
        self.wfile.write(str({"PUT": True}).encode("utf8"))

    def do_DELETE(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str({"DELETE": True}).encode("utf8"))

def run_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
if __name__ == "__main__":
    run_server(handler_class=HttpGetHandler)


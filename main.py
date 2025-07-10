from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
from urllib.request import urlopen

class HttpServer(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            self._set_response()
            response = urlopen("http://localhost:8001" + self.path)
            content = response.read()
            self.wfile.write(content)
        except ConnectionAbortedError:
            logging.info("Connection aborted by client")


def run(server_class=HTTPServer, handler_class=HttpServer):
    port = 8000
    if port is None:
        raise Exception("Server Port Variable Missing")
    port = int(port)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


run()
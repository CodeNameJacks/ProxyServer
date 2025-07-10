from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
from urllib.error import URLError
from urllib.request import urlopen, HTTPError, urlretrieve
import os

domain_list = (".com", ".ru",".org", ".net", ".ir", ".in", ".uk", ".au", ".de", ".ua",)
last_cache = ""

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
            filename = self.path
            content = fetch_file(filename)
            self._set_response()
            self.wfile.write(content)
        except ConnectionAbortedError:
            logging.info("Connection aborted by client")
        except TypeError:
            self.wfile.write('empty'.encode('utf-8'))





def fetch_file(filename):
    
    domain = filename.endswith(domain_list)
    if domain:
        last_cache = filename
        
        last_cached_file = open('cache/last_cache', 'w')
        last_cached_file.write(filename)
        last_cached_file.close()
    else:
        
        try:
            # Check if we have this file locally
            fin = open('cache/last_cache')
            last_cached_value = fin.read()
            fin.close()
            # If we have it, let's send it
            last_cache = last_cached_value
        except IOError:
            last_cache = ''

    # Let's try to read the file locally first
    file_from_cache = fetch_from_cache(filename)

    if file_from_cache:
        print('Fetched successfully from cache.')
        return file_from_cache.encode('utf-8')
    else:
        print('Not in cache. Fetching from server.')
        if domain:
            fetch_from_server(filename, domain=True)
            file_from_server = fetch_from_cache(filename).encode('utf-8')
        else:
            file_from_server = fetch_from_server(last_cache + filename)

        if file_from_server:
            return file_from_server
    return None
       


def fetch_from_cache(filename):
    try:
        # Check if we have this file locally
        fin = open('cache' + filename, encoding="utf8")
        content = fin.read()
        fin.close()
        # If we have it, let's send it
        return content
    except UnicodeDecodeError:
        try:
            # Check if we have this file locally
            fin = open('cache' + filename)
            content = fin.read()
            fin.close()
            # If we have it, let's send it
            return content
        except IOError:
            return None

    except IOError:
        return None


def fetch_from_server(filename, domain=False):
    try:
        if domain:
            urlretrieve("http:/" + filename, "Cache" + filename)
            return True
        else:
            response = urlopen("http:/" + filename)
            content = response.read()
            return content
    except HTTPError:
        return None
    except URLError:
        return None


def save_in_cache(filename, content):
    print('Saving a copy of {} in the cache'.format(filename))

    cached_file = open('cache' + filename, 'w')
    cached_file.write(str(content))
    cached_file.close()


def run(server_class=HTTPServer, handler_class=HttpServer):
    port = 8001
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
run()
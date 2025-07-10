# Proxy Web Server

This is a simple web proxy server that has the ability to cache web pages. It handles GET requests as well as images. 

The web server uses the HTTP/1.1 GET request protocol to receive and respond to web server requests. The request, when received from a client by the server, is processed and 
a response is sent back to the client. The requests and responses pass through a proxy server which act as a middle-man that receives and forwards the requests and responses between 
the client server and the web server. The request is received by the proxy server which checks to see if the response to that request is cached. If cached, the response is retrieved and 
sent back to the client. If it is not cached, then the request is forwarded to the web server which responds with the content and the status code. The response is received by the web server 
which then caches the response. The proxy server then sends the cached response to the client. For caching we stored the file name in our file system in a folder that we created named cache. 



In setting up the proxy server the following approach was used:

There are two files, main.py and cache.py.

We begin in main.py where we define the port, the server type, add the listener, server address and the handler.

In the request handler class, the do_GET method receives the HTTP request, reads it, prepares the header and sends the request to the proxy server. 
The proxy server was created using the HTTP Request protocol. 

In cache_proxy.py, we get the requested filename from the server.

We then check to see if the file is stored in cache. If it is stored in cache, the fetch_from_cache method retrieves the cached data and send it to the server as the response. If it is not in cache,
then the save_in_cache method saves the file and associated data in the system's cache folder and then sends the cached file as a response to the server. 

import http.server
import os
import socketserver
import threading


def serve_opml():
    """
    Serves OPML file over HTTP server
    """
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", int(os.environ["HTTP_PORT"])), handler) as httpd:
        print(f"Server started on port {os.environ['HTTP_PORT']}")
        httpd.serve_forever()

import http.server
import os
import socketserver


def serve_opml():
    """
    Serves the .opml file over HTTP server
    """

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", int(os.environ["HTTP_PORT"])), Handler) as httpd:
        print(f"Serving at port {os.environ['HTTP_PORT']}")
        httpd.serve_forever()

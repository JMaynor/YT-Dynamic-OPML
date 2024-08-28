import http.server
import os
import socketserver
import xml.etree.ElementTree as ET

from logger import logger


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = "/subscriptions.opml"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


def create_opml(subscriptions: dict):
    """
    Creates/recreates the OPML file with the given list of subscriptions
    subscriptions is a dictionary with the channel ID as the key and
    the channel information as the value (itself a dictionary)
    """

    # If the file already exists, delete it
    if os.path.exists("subscriptions.opml"):
        os.remove("subscriptions.opml")

    # Create the root element
    root = ET.Element("opml")
    root.set("version", "1.0")

    # Create the head element
    head = ET.SubElement(root, "head")
    title = ET.SubElement(head, "title")
    title.text = "YouTube Subscriptions"

    # Create the body element
    body = ET.SubElement(root, "body")

    # Create the outline element for each subscription
    for channel_id, channel_info in subscriptions.items():
        outline = ET.SubElement(
            body,
            "outline",
            text=channel_info["title"],
            type="rss",
            title=channel_info["title"],
            xmlUrl=f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
            htmlUrl=f"https://www.youtube.com/channel/{channel_id}",
        )

    # Write the OPML file
    tree = ET.ElementTree(root)
    tree.write("subscriptions.opml")


def serve_opml():
    """
    Serves the .opml file over HTTP server
    """
    # Set the directory to the location of the OPML file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    Handler = CustomHandler

    with socketserver.TCPServer(("", int(os.environ["HTTP_PORT"])), Handler) as httpd:
        logger.info(f"Serving at port {os.environ['HTTP_PORT']}")
        httpd.serve_forever()

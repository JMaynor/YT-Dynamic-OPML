import os
import time
import xml.etree.ElementTree as ET

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


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


def get_subscriptions():
    """
    Retrieves the list of subscriptions for the authenticated user's channel
    1. Authenticate the user with API
    2. Retrieve list of channel subscriptions for the authenticated user
    3. Return dictionary of info for each subscription
    """

    subscriptions = {}

    youtube = build(
        os.environ["YOUTUBE_API_SERVICE_NAME"],
        os.environ["YOUTUBE_API_VERSION"],
        developerKey=os.environ["DEVELOPER_KEY"],
    )

    return subscriptions


def format_subscriptions(subscriptions):
    """
    Formats subscription info from API into dictionary
    """
    pass

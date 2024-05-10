import http.server
import socketserver
import threading
import time
import xml.etree.ElementTree as ET

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "YOUR_DEVELOPER_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def update_subscriptions():
    while True:

        youtube = build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
        )

        # Retrieve the contentDetails part of the channel resource for the authenticated user's channel.
        channels_response = (
            youtube.channels().list(mine=True, part="contentDetails").execute()
        )

        for channel in channels_response["items"]:
            # From the API response, extract the playlist ID that identifies the list of videos
            # uploaded to the authenticated user's channel.
            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

            print("Subscriptions of channel %s" % uploads_list_id)

            # Retrieve the list of subscriptions for the authenticated user's channel.
            subscriptions_list_request = youtube.subscriptions().list(
                channelId=uploads_list_id, part="snippet", maxResults=50
            )

            print("Channels subscribed by the authenticated user.")
            while subscriptions_list_request:
                subscriptions_list_response = subscriptions_list_request.execute()

                # Print information about each subscription.
                for subscription in subscriptions_list_response["items"]:
                    title = subscription["snippet"]["title"]
                    channel_id = subscription["snippet"]["resourceId"]["channelId"]
                    print("%s (%s)" % (title, channel_id))

                    subscriptions_list_request = youtube.subscriptions().list_next(
                        subscriptions_list_request, subscriptions_list_response
                    )

        # Wait for 24 hours
        time.sleep(24 * 60 * 60)


# Start a thread that updates the subscriptions every day
threading.Thread(target=update_subscriptions).start()

# Start the HTTP server
# ...

import os
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from logger import logger


def get_subscriptions():
    """
    Retrieves the list of subscriptions for the authenticated user's channel
    1. Authenticate the user with API
    2. Retrieve list of channel subscriptions for the authenticated user
    3. Return dictionary of info for each subscription
    """

    subscriptions = {}

    youtube = build(
        serviceName=os.environ["YOUTUBE_API_SERVICE_NAME"],
        version=os.environ["YOUTUBE_API_VERSION"],
        developerKey=os.environ["DEVELOPER_KEY"],
    )

    pass

    try:
        # Retrieve list of channel subscriptions for the authenticated user
        response = (
            youtube.subscriptions()
            .list(part="snippet", mine=True, maxResults=100)
            .execute()
        )

        # Extract channel ID and title for each subscription
        for item in response["items"]:
            pass
            channel_id = item["snippet"]["resourceId"]["channelId"]
            channel_title = item["snippet"]["title"]
            subscriptions[channel_id] = {"title": channel_title}

    except HttpError as e:
        logger.error(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return subscriptions


def format_subscriptions(subscriptions):
    """
    Formats subscription info from API into dictionary
    """
    pass

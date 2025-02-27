import json
import os

from _logger import logger
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
SERVICE_ACCOUNT_FILE = "service_account.json"


def save_subscriptions(subscriptions, channel_id):
    """
    Save subscriptions to a local file
    """
    filename = f"subscriptions_{channel_id}.json"
    with open(filename, "w") as f:
        json.dump(subscriptions, f)


def load_subscriptions(channel_id):
    """
    Load subscriptions from a local file
    """
    filename = f"subscriptions_{channel_id}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}


def get_subscriptions(channel_id):
    """
    Retrieves the list of subscriptions for the specified channel ID
    1. Authenticate using service account
    2. Retrieve list of channel subscriptions for the specified channel ID
    3. Return dictionary of info for each subscription
    """

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    youtube = build(
        serviceName="youtube",
        version="v3",
        credentials=credentials,
    )

    subscriptions = {}

    try:
        # Retrieve list of channel subscriptions for the specified channel ID
        response = (
            youtube.subscriptions()
            .list(part="snippet", channelId=channel_id, maxResults=100)
            .execute()
        )

        # Extract channel ID, title, and description for each subscription
        for item in response["items"]:
            sub_channel_id = item["snippet"]["resourceId"]["channelId"]
            channel_title = item["snippet"]["title"]
            channel_description = item["snippet"]["description"]
            subscriptions[sub_channel_id] = {
                "title": channel_title,
                "description": channel_description,
            }

        # Save subscriptions to local file
        save_subscriptions(subscriptions, channel_id)

    except HttpError as e:
        logger.error(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        logger.error(f"Error details: {e}")
        # Load subscriptions from local file if API call fails
        subscriptions = load_subscriptions(channel_id)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # Load subscriptions from local file if API call fails
        subscriptions = load_subscriptions(channel_id)

    return subscriptions

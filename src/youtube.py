import json
import os
import pickle

from _logger import logger
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def save_subscriptions(subscriptions):
    """
    Save subscriptions to a local file
    """
    with open("subscriptions.json", "w") as f:
        json.dump(subscriptions, f)


def load_subscriptions():
    """
    Load subscriptions from a local file
    """
    if os.path.exists("subscriptions.json"):
        with open("subscriptions.json", "r") as f:
            return json.load(f)
    return {}


def get_subscriptions():
    """
    Retrieves the list of subscriptions for the authenticated user's channel
    1. Authenticate the user with OAuth 2.0
    2. Retrieve list of channel subscriptions for the authenticated user
    3. Return dictionary of info for each subscription
    """

    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=8080)

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    youtube = build(
        serviceName="youtube",
        version="v3",
        credentials=credentials,
    )

    subscriptions = {}

    try:
        # Retrieve list of channel subscriptions for the authenticated user
        response = (
            youtube.subscriptions()
            .list(part="snippet", mine=True, maxResults=100)
            .execute()
        )

        # Extract channel ID and title for each subscription
        for item in response["items"]:
            channel_id = item["snippet"]["resourceId"]["channelId"]
            channel_title = item["snippet"]["title"]
            subscriptions[channel_id] = {"title": channel_title}

        # Save subscriptions to local file
        save_subscriptions(subscriptions)

    except HttpError as e:
        logger.error(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        logger.error(f"Error details: {e}")
        # Load subscriptions from local file if API call fails
        subscriptions = load_subscriptions()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # Load subscriptions from local file if API call fails
        subscriptions = load_subscriptions()

    return subscriptions


def format_subscriptions(subscriptions):
    """
    Formats subscription info from API into dictionary
    """
    pass

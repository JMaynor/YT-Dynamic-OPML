import os

from dotenv import load_dotenv

load_dotenv()

import threading

from src.create_opml import create_opml, get_subscriptions
from src.serve_opml import serve_opml

if __name__ == "__main__":
    """
    Main entry point of program
    """

    # Create OPML
    subscriptions = get_subscriptions()
    create_opml(subscriptions)

    # Serve OPML
    thread = threading.Thread(target=serve_opml)
    thread.start()
    thread.join()

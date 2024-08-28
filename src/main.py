import os
import time

from dotenv import load_dotenv

load_dotenv()

import threading

from server import create_opml, serve_opml
from youtube import get_subscriptions


def refresh_opml(interval):
    """
    Periodically refresh the OPML file.
    """
    while True:
        subscriptions = get_subscriptions()
        if subscriptions:
            create_opml(subscriptions)
        time.sleep(interval)


if __name__ == "__main__":
    """
    Main entry point of program
    """

    # Start the thread for refreshing the OPML file
    refresh_thread = threading.Thread(
        target=refresh_opml, args=(int(os.environ["REFRESH_INTERVAL"]),)
    )
    refresh_thread.daemon = True  # Daemonize thread to exit when main program exits
    refresh_thread.start()

    # Start the HTTP server in the main thread
    serve_opml()

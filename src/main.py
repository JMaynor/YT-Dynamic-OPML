"""
Main FastAPI application
Serves youtube subscriptions of authenticated user in OPML format
"""

import xml.etree.ElementTree as ET
from datetime import datetime

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from youtube import get_subscriptions

load_dotenv()

# Create FastAPI app
app = FastAPI(
    docs_url=None,
    redoc_url=None,  # Disable docs (Swagger UI)  # Disable redoc
)


def subscriptions_to_opml(subscriptions):
    """
    Convert subscriptions dictionary to OPML format
    """
    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")
    title = ET.SubElement(head, "title")
    title.text = "YouTube Subscriptions"
    date_created = ET.SubElement(head, "dateCreated")
    date_created.text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
    body = ET.SubElement(opml, "body")
    outline = ET.SubElement(body, "outline", text="YouTube Subscriptions▶")

    for channel_id, info in subscriptions.items():
        ET.SubElement(
            outline,
            "outline",
            text=info["title"],
            title=info["title"],
            type="rss",
            xmlUrl=f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
            htmlUrl=f"https://www.youtube.com/channel/{channel_id}",
            description=info["description"],  # Add description field
        )
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    return (
        f"{xml_declaration}{ET.tostring(opml, encoding='utf-8', method='xml').decode()}"
    )


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/subscriptions/{channel_id}.opml")
def read_subscriptions(channel_id: str):
    """
    Serve OPML XML file with channel subscriptions
    """
    subscriptions = get_subscriptions(channel_id)
    opml_content = subscriptions_to_opml(subscriptions)
    return Response(content=opml_content, media_type="application/xml")


if __name__ == "__main__":
    """
    Main entry point of program
    """
    uvicorn.run(app, host="0.0.0.0", port=5000)

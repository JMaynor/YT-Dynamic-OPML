# YT-Dynamic-OPML

This project is intended for use with FreshRSS or other similar RSS programs. FreshRSS allows using a dynamic OPML file to populate a category of RSS feeds. The idea is to pull the list of subscriptions from the authenticated user's YouTube channel and return an OPML file with the corresponding RSS feeds. Allows YouTube to be the canonical list of one's subscriptions but also pull that list into an RSS app in an automatic way.

## Config

### Steps to Set Up Google Cloud Project and Service Account

1. **Create a Google Cloud Project**
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Click on the project drop-down and select `New Project`.
    - Enter a project name and click `Create`.

2. **Enable YouTube Data API**
    - In the Google Cloud Console, navigate to `APIs & Services` > `Library`.
    - Search for `YouTube Data API v3` and click on it.
    - Click `Enable` to enable the API for your project.

3. **Create a Service Account**
    - In the Google Cloud Console, navigate to `IAM & Admin` > `Service Accounts`.
    - Click `Create Service Account`.
    - Enter a service account name (e.g., `youtube-subscriptions-service`) and click `Create`.
    - Click `Done` to finish creating the service account.

4. **Create and Download Service Account Key**
    - In the `Service Accounts` page, click on the service account you created.
    - Go to the `Keys` tab and click `Add Key` > `Create new key`.
    - Select `JSON` as the key type and click `Create`.
    - The JSON key file will be downloaded to your computer. Save it as `service_account.json` in your project directory.

### Running the Application with Docker and Docker Compose

1. Build and run the Docker container using Docker Compose:

    ```sh
    docker compose up -d
    ```

2. Access the application at `http://127.0.0.1:5000/subscriptions/YOUR_CHANNEL_ID.opml`.

Replace `YOUR_CHANNEL_ID` with the actual channel ID you want to retrieve subscriptions for.

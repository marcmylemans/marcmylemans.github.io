---
layout: post
title: Convert Youtube Descriptions to Posts
categories: Python Script
tags: python scripts youtube
---

Here is an example of Python code that uses the YouTube Data API to retrieve the description of a video and then write it to a .md file:

```python
import os
import google.auth
from googleapiclient.discovery import build

# Set up the YouTube Data API
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

# Get credentials and create an API client
creds = google.auth.default(scopes=scopes)
youtube = build(api_service_name, api_version, credentials=creds)

# Get the video's description
video_id = "VIDEO_ID"
request = youtube.videos().list(part="snippet", id=video_id)
response = request.execute()
description = response["items"][0]["snippet"]["description"]

# Write the description to a .md file
with open("description.md", "w") as f:
    f.write(description)
```

You'll need to replace VIDEO_ID with the actual video id of the video you want to get the description of. Also, you need to have a client_secret.json file that contains the credentials for the project that you created in Google developer console.

Please keep in mind that it requires YouTube Data API v3 library, if you don't have it installed please use this command !pip install --upgrade google-api-python-client

Also, you'll need to enable the YouTube Data API on your Google Cloud Platform project and create credentials to use the API.
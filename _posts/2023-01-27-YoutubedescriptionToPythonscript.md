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
from datetime import datetime

# Set up the YouTube Data API
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

# Get credentials and create an API client
creds = google.auth.default(scopes=scopes)
youtube = build(api_service_name, api_version, credentials=creds)

# Get the channel ID
channel_name = "CHANNEL_NAME"
request = youtube.channels().list(part="snippet,contentDetails,statistics", forUsername=channel_name)
response = request.execute()
channel_id = response["items"][0]["id"]

# Get the most recent video uploaded to the channel
request = youtube.search().list(
    part="id,snippet",
    channelId=channel_id,
    maxResults=1,
    order='date'
)
response = request.execute()
video_id = response["items"][0]["id"]["videoId"]
title = response["items"][0]["snippet"]["title"]
publishedAt = response["items"][0]["snippet"]["publishedAt"]

# Get the video's description and tags
request = youtube.videos().list(part="snippet", id=video_id)
response = request.execute()
description = response["items"][0]["snippet"]["description"]
tags = response["items"][0]["snippet"]["tags"]

# Replace special characters with _ in the title
title = title.replace("\\", "_")
title = title.replace("/", "_")
title = title.replace(":", "_")
title = title.replace("*", "_")
title = title.replace("?", "_")
title = title.replace("\"", "_")
title = title.replace("<", "_")
title = title.replace(">", "_")
title = title.replace("|", "_")

# Write the description and tags to a .md file
date_object = datetime.strptime(publishedAt[:10], '%Y-%m-%d')
file_name = date_object.strftime('%Y-%m-%d') + '-' + title + '.md'
with open(file_name, "w") as f:
    f.write("---\nlayout: post\ntitle: " + title + "\ntags: " + str(tags) + "\n---\n" + '{% youtube "https://www.youtube.com/watch?v=' + video_id + '" %}\n' + description)
```

Also, you need to have a client_secret.json file that contains the credentials for the project that you created in Google developer console.

Please keep in mind that it requires YouTube Data API v3 library, if you don't have it installed please use this command !pip install --upgrade google-api-python-client

Also, you'll need to enable the YouTube Data API on your Google Cloud Platform project and create credentials to use the API.
---
layout: post
title: Convert Youtube Descriptions to Posts
categories: Python Script
tags: python scripts youtube
---


# Automate Youtube uploads to Posts!

## Introduction
To help me streamline the process of uploading a Youtube video and creating a new blogpost i'm using the power of Python.
You can save this for example as **c:\temp\convertyoutube_to_md.py**

## The Code

```python
import requests
import os
import re

def create_file(video_id, title, description, date):
    folder_path = "md_files"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    title2 = re.sub(r'[^\w\s]', '', title)
    title2 = title2.replace(" ", "_")
    filename = f"{folder_path}/{date}-{title2}.md"
    with open(filename, "w") as f:
        f.write(f"---\n")
        f.write(f"layout: post\n")
        f.write(f"title: {title}\n")
        f.write(f"---\n")
        f.write(f"{description}\n\n")
        f.write("{% youtube " + "https://www.youtube.com/watch?v=" + video_id + " %}\n")

def get_channel_videos(channel_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=50"
    response = requests.get(url)
    data = response.json()
    items = data["items"]

    video_ids = [item["id"]["videoId"] for item in items if "videoId" in item["id"]]
    return video_ids

def get_video_info(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    items = data["items"]

    title = items[0]["snippet"]["title"]
    description = items[0]["snippet"]["description"]
    date = items[0]["snippet"]["publishedAt"].split("T")[0]

    return title, description, date

def main(channel_id, api_key):
    video_ids = get_channel_videos(channel_id, api_key)
    for video_id in video_ids:
        title, description, date = get_video_info(video_id, api_key)
        create_file(video_id, title, description, date)

if __name__ == "__main__":
    channel_id = "channel_id"
    api_key = "api_key"
    main(channel_id, api_key)

```

Just replace channel_id and api_key with the appropriate values for your channel and API key, and run the script. Note that the API returns a maximum of 50 results per request, so if your channel has more than 50 videos, you'll need to modify the script to make multiple requests and retrieve all the videos.

Please keep in mind that it requires YouTube Data API v3 library, if you don't have it installed please use this command !pip install --upgrade google-api-python-client

Also, you'll need to enable the YouTube Data API on your Google Cloud Platform project and create credentials to use the API.

## Installing Python

You can download python on the official website. [Download Python](https://www.python.org/downloads/)

To install python you just have to go trough the installation wizard, for a written guide go to: [Using Python on Windows](https://docs.python.org/3/using/windows.html)

>Make sure to select "Add Python to PATH", this way you can run **python** from the commandline without adding the full path.
{: .prompt-warning }

## Running the script

After you saved the script you can run the script with the following command:

```
python c:\temp\convertyoutube_to_md.py
```
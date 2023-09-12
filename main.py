import os

import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())  # find_dotenv() is to find the .env

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ["YOUTUBE_API_KEY"]

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

request = youtube.commentThreads().list(
    part="snippet", videoId="O5AsvA9OGhM", maxResults=100
)
comments = []
response = request.execute()
for item in response["items"]:
    comment = item["snippet"]["topLevelComment"]["snippet"]

    comments.append(
        [
            comment["authorDisplayName"],
            comment["publishedAt"],
            comment["updatedAt"],
            comment["likeCount"],
            comment["textDisplay"],
        ]
    )

df = pd.DataFrame(
    comments, columns=["author", "published_at", "updated_at", "like_count", "text"]
)

print(df.head(10))

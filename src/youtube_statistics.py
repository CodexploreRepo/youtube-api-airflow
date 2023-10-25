import json

import requests


class YoutubeETL:
    def __init__(self, api_key: str, channel_id: str) -> None:
        self.api_key = api_key
        self.channel_id = channel_id

    @property
    def channel_statistics(self):
        url = (
            "https://www.googleapis.com/youtube/v3/channels?part=statistics"
            f"&key={self.api_key}&id={self.channel_id}"
        )

        data = self._send_get_request(url)
        try:
            return data["items"][0]["statistics"]
        except:
            return None

    def get_channel_video_data(self):
        # 1) get video ids
        video_ids = self._get_channel_videos(limit=50)
        # 2 get video statistics
        parts = ["snippet", "statistics", "contentDetails"]

    def _send_get_request(self, url: str) -> dict:
        response = requests.get(url=url)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None
    
    def _get_channel_videos(self, limit=None) -> list[str]:
        url = (
            "https://www.googleapis.com/youtube/v3/search?"
            f"key={self.api_key}&channelId={self.channel_id}&part=id&order=date"
        )

        if limit is not None and isinstance(limit, int):
            url += f"&maxResults={limit}"
        video_ids = []
        data = self._send_get_request(url)
        while data.get("nextPageToken") or data.get("prevPageToken"):
            items = data["items"]

            video_ids.extend(
                [
                    item["id"]["videoId"]
                    for item in items
                    if item["id"]["kind"] == "youtube#video"
                ]
            )
            try:
                next_url = f"{url}&pageToken={data['nextPageToken']}"
                data = self._send_get_request(next_url)
            except KeyError:
                break
        return video_ids


if __name__ == "__main__":
    import os

    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())
    yt_etl = YoutubeETL(
        os.environ["YOUTUBE_API_KEY"], "UCN03cDDMfrD6Iyxk20_dvmQ"
    )

    # print(yt_etl.channel_statistics)
    yt_etl.get_channel_video_data()

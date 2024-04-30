import asyncio
import os

from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
YoutubeTOKEN = os.getenv("YoutubeTOKEN")


# 유튜브 api 요청 코드
async def request_youtube_api(channel_id):

	youtube = build('youtube', 'v3', developerKey=YoutubeTOKEN)

	video_request = youtube.search().list(
		part="snippet, id",
		channelId=channel_id,
		maxResults=1,
		order="date"
	)
	video_response = video_request.execute()

	channel_request = youtube.channels().list(
		part="snippet",
		id=channel_id
	)
	channel_response = channel_request.execute()

	video_items = video_response.get("items", [])
	channel_items = channel_response.get("items", [])

	if video_items and channel_items:
		video = video_items[0]
		channel = channel_items[0]
		video_id = video["id"]["videoId"]
		snippet = video["snippet"]
		title = snippet["title"]
		published_at = snippet["publishedAt"]
		channel_title = snippet["channelTitle"]
		channel_profile_image = channel["snippet"]["thumbnails"]["default"]["url"]

		return {
			"videoId": video_id,
			"title": title,
			"published_at": published_at,
			"channel_title": channel_title,
			"channel_profile_image": channel_profile_image
		}
	else:
		print("No video or channel not found.")
		return None


async def youtube_test():
	channel_id = "[Input channel_id]"
	response = await request_youtube_api(channel_id)
	print(response)


loop = asyncio.get_event_loop()
loop.run_until_complete(youtube_test())
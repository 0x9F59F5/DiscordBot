import aiohttp
import json


async def getChannelLive(channel_id, is_live):
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://api.chzzk.naver.com/service/v2/channels/{channel_id}/live-detail",
		                       headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
		                       ) as response:
			response = await response.json()

			content = response.get('content')
			status = content.get('status', {})

			if status == "OPEN" and is_live == 0:
				# 방송이 켜졌으면 is_live를 1로 변경

				return {
					'channelId': content.get('channel', {}).get('channelId'),
					'liveTitle': content.get('liveTitle'),
					'channelImageUrl': content.get('channel', {}).get('channelImageUrl'),
					'openDate': content.get('openDate')
				}

			elif status == "CLOSE" and is_live == 1:
				# 방송이 꺼지면 is_live를 0으로 변경
				return None
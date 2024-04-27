import aiohttp
import asyncio


header = {
	"User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}


async def request_chzzk_channel(channel_id):
	async with aiohttp.ClientSession() as request:
		url = f"https://api.chzzk.naver.com/service/v2/channels/{channel_id}/live-detail"
		async with request.get(url, headers=header) as response:
			if response.status == 200:
				return await response.json()
			else:
				print(f"Error Status code: {response.status}")
				return None


# api 요청 테스트
async def main():
	channel_id = "3a2d2f4e9132d822423f6aa879e598c5"
	response = await request_chzzk_channel(channel_id)
	print(response)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
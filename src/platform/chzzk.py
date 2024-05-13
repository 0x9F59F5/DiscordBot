import time
import asyncio

from src.ApiRequest.RequestChzzk import getChannelLive


async def get_chzzk_channel():
	start_time = time.time()

	response = await getChannelLive("input channel_id", "input status 0 / 1")
	print(response)

	end_time = time.time()
	print("Total execution time:", end_time - start_time, "seconds")


if __name__ == "__main__":
	asyncio.run(get_chzzk_channel())
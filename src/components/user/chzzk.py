import aiohttp
import asyncio
import time
import pytz
import random

from datetime import datetime
from DiscordBot.src.postgresql.Database import DatabaseManager
from DiscordBot.src.utils.discordApiInstance import sendWebhook
from DiscordBot.src.tasks import chzzk_response


class Chzzk:

    def __init__(self):
        self.connection = DatabaseManager()
        self.session = aiohttp.ClientSession()

    async def getChannelLive(self, channelId, username, is_live):
        async with self.session.get(f"https://api.chzzk.naver.com/service/v2/channels/{channelId}/live-detail",
                               headers={'User-Agent': 'Mozilla/5.0'}) as response:
            response = await response.json()
            content = response.get('content', {})
            status = content.get('status', '')

            if status == "OPEN" and not is_live:
                await self.change_live_status(channelId, True)
                return {
                    'name': username,
                    'channelId': content.get('channel', {}).get('channelId'),
                    'liveTitle': content.get('liveTitle'),
                    'channelImageUrl': content.get('channel', {}).get('channelImageUrl'),
                    'openDate': datetime.strptime(content.get('openDate'), '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('Asia/Seoul'))
                }
            elif status == "CLOSE" and is_live:
                await self.change_live_status(channelId, False)
                return None

    async def change_live_status(self, channelId, is_live: bool):
        query = "UPDATE chzzk_channel SET is_live = $1 WHERE chzzk_channel_id = $2"
        params = (is_live, channelId)
        await self.connection.execute(query, params)

    async def get_channels_from_db(self):
        query = "SELECT * FROM chzzk_channel"
        channels = await self.connection.execute(query)

        channel_list = []
        for channel in channels:
            channel_info = {
                'chzzk_channel_id': channel['chzzk_channel_id'],
                'username': channel['name'],
                'is_live': channel['is_live']
            }
            channel_list.append(channel_info)

        return channel_list

    async def get_channel_subscribers_from_db(self, channelId):
        query = """
        SELECT 
            wt.webhook_id, 
            wt.webhook_token
        FROM 
            chzzk_channel cc 
            JOIN chzzk_sub dc ON cc.chzzk_channel_id = dc.chzzk_channel_id 
            JOIN webhook_table wt ON dc.discord_channel_id = wt.discord_channel_id
        WHERE
            cc.chzzk_channel_id = $1 AND dc.notification = True
        """
        params = (channelId,)
        return await self.connection.execute(query, params)

    async def send_notification(self, channel_id, embed):
        subscribers = await self.get_channel_subscribers_from_db(channel_id)
        tasks = []
        for subscriber in subscribers:
            task = asyncio.create_task(
                sendWebhook(self.session, subscriber['webhook_id'], subscriber['webhook_token'], embed))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def close(self):
        await self.session.close()


async def main():
    chzzk = Chzzk()
    try:
        while True:
            start = time.time()

            channels = await chzzk.get_channels_from_db()
            tasks = [chzzk.getChannelLive(channel['chzzk_channel_id'], channel['username'], channel['is_live']) for channel in channels]
            result = await asyncio.gather(*tasks)

            for results in result:
                if results:
                    embed = await chzzk_response(results['channelId'], results['name'], results['liveTitle'], results['channelImageUrl'], results['openDate'])
                    await chzzk.send_notification(results['channelId'], embed)

            print(result)

            end = time.time()
            print(f"{end - start:.5f} sec")
            await asyncio.sleep(random.randint(5, 14))
    finally:
        await chzzk.close()


if __name__ == "__main__":
    asyncio.run(main())

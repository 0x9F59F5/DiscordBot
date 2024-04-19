import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.messages = True

client = commands.Bot(command_prefix='/', intents=intents)


@client.event
async def on_ready():

	await client.change_presence(status=discord.Status.online)
	await client.add_cog()

	print("Slash Command " + str(len(synced)))


client.run(TOKEN)
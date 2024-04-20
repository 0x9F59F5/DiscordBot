import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from src.command.Commands import Commands

load_dotenv()
TOKEN = os.getenv("TOKEN")
guild_id = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.messages = True

client = commands.Bot(command_prefix='/', intents=intents)


@client.event
async def on_ready():

	await client.change_presence(status=discord.Status.online)
	await client.add_cog(Commands(client))

	synced = await client.tree.sync()
	await client.tree.sync(guild=discord.Object(id=GUILD_ID))
	print("Slash Command " + str(len(synced)))


client.run(TOKEN)
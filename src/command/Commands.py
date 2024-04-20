import discord
from discord.ext import commands


class Commands(commands.Cog):
	def __init__(self, client):
		self.client = client

	@discord.app_commands.command(name="start", description="알림을 받을 스트리머를 선택해주세요.")
	async def start(self, interaction: discord.Interaction):

		embed = discord.Embed(title="알림 설정", color=0xBDA3D0)
		embed.add_field(name="스트리머 선택", value="알림을 받을 스트리머를 선택해주세요.", inline=True)

		await interaction.response.send_message(embed=embed, view=view)
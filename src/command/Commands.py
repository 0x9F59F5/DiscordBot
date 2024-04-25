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

	@discord.app_commands.command(name="setting", description="알림을 받을 서비스를 선택해주세요")
	async def setting(self, interaction: discord.Interaction):
		if interaction.channel.name in ["쿠레나이_나츠키", "반님", "테리눈나", "스데공지봇"]:

			embed = discord.Embed(title="알림을 받을 서비스를 선택해주세요.", colour=0xBDA3D0)
			embed.add_field(name="알림 설정", value="알림을 받을 서비스를 선택해주세요.", inline=True)

			await interaction.response.send_message(embed=embed)
		else:
			await interaction.response.send_message(f'"{interaction.channel.name}"에서는 사용할 수 없습니다.')
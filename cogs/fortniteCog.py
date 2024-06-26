import discord
from discord import app_commands
from discord.ext import commands
from resources.fortnite import Fortnite, UserNotFound
from typing import Literal

class FortniteCog(commands.GroupCog,name='fortnite'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.describe(username="The Fortnite user you'd like to check")
	@app_commands.command(description="Gets someone's BattlePass level")
	async def level(self, interaction: discord.Interaction,username: str):
		try:
			info = await Fortnite.get_bp_level(username)
			await interaction.response.send_message(f"{username}'s BattlePass is at level {info['level']} (progress: {info['progress']})")
		except UserNotFound:
			await interaction.response.send_message(f"Username {username} not found")
	@app_commands.describe(username="The Fortnite user you'd like to check",
								time_window="Wheter to check lifetime stats or season stats",
								stat="The statistic to check",
								mode="The gamemode of the stat to check")
	@app_commands.command(description="Gets someone's specific Fortnite stat")
	async def stats(self, interaction: discord.Interaction,
				 username: str, time_window: Literal['lifetime','season'],
				 stat: Literal["score", "scoreperwin", "scorepermatch", "wins", "top3", "top5", "top6", "top10", "top12", "top25", "kills", "killspermin", "killspermatch", "deaths", "kd", "matches", "winrate", "minutesplayed", "playersoutlived"],
				 mode: Literal["overall", "solo", "duo", "squad", "ltm"]):
		try:
			embed = discord.Embed(
				title=f"Data for {username}",
				description=f"Mode: {mode}\nStatistic: {stat}\nValue: {await Fortnite.get_stats(username,time_window,stat,mode)}",
				colour=discord.Colour.green()
			)
			await interaction.response.send_message(embed=embed)
		except UserNotFound:
			await interaction.response.send_message(f"Username {username} not found")
		except KeyError:
			await interaction.response.send_message(f"Stat not found, most likely not compatible with the mode you selected")
	
	@app_commands.describe(username="The Fortnite username to check",time_window="Wheter to receive lifetime or season stats")
	@app_commands.command(description="Shows someone's Fortnite stats in an image")
	async def imgstats(self, interaction: discord.Interaction, username: str, time_window: Literal['lifetime','season']):
		try:
			await interaction.response.send_message(await Fortnite.get_img_stats(username,time_window))
		except UserNotFound:
			await interaction.response.send_message(f"Username {username} not found")

async def setup(bot: commands.Bot):
	await bot.add_cog(FortniteCog(bot))
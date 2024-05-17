import discord
from discord import app_commands
from discord.ext import commands
from resources.oss import Oss, UserNotFound

class OssCog(commands.GroupCog,name='osu'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.describe(username="The username to check")
	@app_commands.command(description="Shows you a list of someone's previous osu! names")
	@app_commands.checks.cooldown(2,5,key=lambda i: i.user.id)
	async def pastnames(self, interaction: discord.Interaction, username: str):
		try:
			info = await Oss.get_previous_usernames(username)
			embed = discord.Embed(
				title=f"{info['username']}'s previous usernames:",
				description='',
				colour=discord.Colour.green()
			)
			for name in info['past_usernames']:
				embed.description += f'{name}\n'
			await interaction.response.send_message(embed=embed)
		except (UserNotFound, KeyError):
			await interaction.response.send_message(f"Username {username} not found")
	@app_commands.describe(username="The username to check")
	@app_commands.command(description="Shows the country of an osu! user")
	@app_commands.checks.cooldown(2,5,key=lambda i: i.user.id)
	async def country(self, interaction: discord.Interaction, username: str):
		try:
			country = await Oss.get_country(username)
			embed = discord.Embed(
				title=country['country_name'],
				description=f"{country['username']} is registered on **{country['country_name']}** {country['country_code']['flag_emoji']}",
				colour=country['country_code']['hex_value'])
			await interaction.response.send_message(embed=embed)
		except (UserNotFound, KeyError):
			await interaction.response.send_message(f"Username {username} not found")
	@app_commands.describe(username="The username to check")
	@app_commands.command(description="Shows someone's osu! supporter details")
	@app_commands.checks.cooldown(2,5,key=lambda i: i.user.id)
	async def supporter(self, interaction: discord.Interaction, username: str):
		try:
			info = await Oss.get_supported_status(username)
			if info['is_supporter']:
				await interaction.response.send_message(f"{info['username']} has supporter")
			elif info['has_supported']:
				await interaction.response.send_message(f"{info['username']} does not have supporter but has supported at least once")
			else:
				await interaction.response.send_message(f"{info['username']} does not have supporter nor has ever supported")
		except (UserNotFound, KeyError):
			await interaction.response.send_message(f"Username {username} not found")
	@app_commands.describe(username="The username to check")
	@app_commands.command(description="Shows someone's osu! profile picture")
	@app_commands.checks.cooldown(2,5,key=lambda i: i.user.id)
	async def pfp(self, interaction: discord.Interaction, username: str):
		try:
			info = await Oss.get_pfp(username)
			embed=discord.Embed(
				title=f"{info['username']}'s pfp",
				colour=discord.Colour.green()
			)
			embed.set_image(url=info['url'])
			await interaction.response.send_message(embed=embed)
		except (UserNotFound, KeyError):
			await interaction.response.send_message(f"Username {username} not found")
	@app_commands.describe(username="The username to check")
	@app_commands.command(description="Shows someone's osu! rank")
	@app_commands.checks.cooldown(2,5,key=lambda i: i.user.id)
	async def rank(self, interaction: discord.Interaction, username: str):
		try:
			info = await Oss.get_rank(username)
			embed=discord.Embed(
				title=f"{info['username']}'s ranks",
				description=f"\N{EARTH GLOBE AMERICAS}Global rank: **#{info['global_rank']:,}**\n\N{WAVING WHITE FLAG}Country rank: **#{info['country_rank']:,}**",
				colour=discord.Colour.green()
			)
			await interaction.response.send_message(embed=embed)
		except (UserNotFound, KeyError):
			await interaction.response.send_message(f"Username {username} not found")
	@app_commands.describe(username="The username to check")
	@app_commands.command(description="Shows someone's highest osu! rank")
	@app_commands.checks.cooldown(2,5,key=lambda i: i.user.id)
	async def highestrank(self, interaction: discord.Interaction, username: str):
		try:
			info = await Oss.get_highest_rank(username)
			embed = discord.Embed(
				title=f"{info['username']}'s peak",
				description=f"{info['username']}'s highest rank: **#{info['rank']:,}**\nRecorded on: <t:{info['timestamp']}>",
				color=discord.Colour.green()
			)
			await interaction.response.send_message(embed=embed)
		except (UserNotFound, KeyError):
			await interaction.response.send_message(f"Username {username} not found")
	@app_commands.describe(username="The username to check")
	@app_commands.command(description="Shows someone's osu! accuracy")
	@app_commands.checks.cooldown(2,5,key=lambda i: i.user.id)
	async def acc(self, interaction: discord.Interaction, username: str):
		try:
			info = await Oss.get_acc(username)
			embed = discord.Embed(
				title=f"{info['username']}'s accuracy",
				description=f"{info['username']}'s accuracy: **{info['acc']}%**"
			)
			if info['acc'] >= 90:
				embed.colour = discord.Colour.green()
			elif info['acc'] >= 80:
				embed.colour = discord.Colour.yellow()
			else:
				embed.colour = discord.Colour.red()
			await interaction.response.send_message(embed=embed)
		except UserNotFound:
			await interaction.response.send_message(f"Username {username} not found")
	@app_commands.describe(username="The username to check")
	@app_commands.command(description="Shows someone's osu! pp")
	@app_commands.checks.cooldown(2,5,key=lambda i: i.user.id)
	async def pp(self, interaction: discord.Interaction, username: str):
		try:
			info = await Oss.get_pp(username)
			embed = discord.Embed(
				title=f"{info['username']}'s PP",
				description=f"{info['username']}'s performance points: **{info['pp']:,}**",
				colour = discord.Colour.green()
			)
			await interaction.response.send_message(embed=embed)
		except UserNotFound:
			await interaction.response.send_message(f"Username {username} not found")

	async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
		if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
			await interaction.response.send_message(f"Command on cooldown! Try again in {error.retry_after:.2f} seconds",ephemeral=True)
		else: raise error
		

async def setup(bot: commands.Bot):
	await bot.add_cog(OssCog(bot))
import discord
from discord import app_commands
from discord.ext import commands, tasks
from random import choice, randint
from resources import levels
from time import localtime, time
from asyncio import sleep
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from resources.utils import json_utils, perms
from resources import (
	botchangelog, bypassurl,
	illumes, randompass, tenor, virustotal
)

status = {"pepsi":"https://www.youtube.com/watch?v=nEHQiHGYZ0s",
					"tokaua":"https://www.youtube.com/watch?v=URBpbhH580k",
					"donovan":"https://www.youtube.com/watch?v=zdDeokVmgCE",
				 "twovb":"https://www.youtube.com/watch?v=9zH9NoTJClo"}

class MiscCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(self.bot.user,'running')
		self.change_status.start()
		async with levels.CD() as f:
			await f.make_table()
		async with levels.MiniGame() as mg:
			await mg.make_table()
		async with levels.CustomEmbed() as ce:
			await ce.make_table()

	@tasks.loop(minutes=5)
	async def change_status(self):
		name = choice(list(status))
		await self.bot.change_presence(activity = discord.Streaming(name=f"{name}'s videos",url=status[name]))

	@app_commands.command(description="Shows how many days have passed since HolyPvP died.")
	async def holydied(self, interaction: discord.Interaction):
		await interaction.response.send_message(f"A total of {int((time()-1696791600)/86400)} days have passed since HolyPvP died")
	@app_commands.command(description="Shows how many days have passed since ViperMC died")
	async def viperdied(self, interaction: discord.Interaction):
		await interaction.response.send_message(f"A total of {int((time()-1701297218)/86400)} days have passed since ViperMC died")
	@app_commands.command(description="Is it Christmas?")
	async def isitchristmas(self, interaction: discord.Interaction):
		if localtime()[1] == 12 and localtime()[2] == 25:
			await interaction.response.send_message("Yes! Merry Christmas! :tada:")
			return
		await interaction.response.send_message("No")
	@app_commands.command(description="GEOMETRY DASH")
	async def gd(self, interaction: discord.Interaction):
		await interaction.response.send_message("https://streamable.com/8kgjto GEOMETRY DASH BEOMMM")
	@app_commands.command(description="Chamoy")
	async def chamoy(self, interaction: discord.Interaction):
		await interaction.response.send_message("https://streamable.com/kzrd5r")

	@app_commands.command(description="Shows a random unsecured camera")
	async def randomcam(self, interaction: discord.Interaction):
		await interaction.response.defer()
		randNum= randint(1,9999)
		find=[]
		actual_time = time.time()
		async with ClientSession() as session:
			while True:
				await sleep(0)
				if time.time() - actual_time > 10:
					await interaction.followup.send("Took too long, try again",ephemeral=True)
					break
				async with session.get(f"http://www.opentopia.com/webcam/{randNum}") as resp:
					if resp.status != 200:
						continue
					soup = BeautifulSoup(await resp.text(encoding='latin1'),'html.parser')
					find = [soup.find("label",attrs={"class":"right country-name"}).text]
					try:
						find.append(soup.find("label",attrs={"class":"right region"}).text)
					except AttributeError:
						find.append("Not Found")
					try:
						find.append(soup.find("span",attrs={"class":"latitude"}).text)
						find.append(soup.find("span",attrs={"class":"longitude"}).text)
					except AttributeError:
						find.append("Not")
						find.append("Found")
					image_link = f"http://images.opentopia.com/cams/{randNum}/big.jpg"
					randNum= randint(1,9999)
					break
		embed = discord.Embed(
			title=f"Country: {find[0]}",
			description=f"State/Region: {find[1]}\nCoordinates: {find[2]}, {find[3]}",
			colour=discord.Colour.green()
		)
		embed.set_image(url=image_link)
		await interaction.followup.send(embed=embed)
	@app_commands.command(description="Is GeometryDash 2.2 out?")
	async def isgdout(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			async with session.get("https://api.steamcmd.net/v1/info/322170") as value:
				value = await value.json()
				if value['data']['322170']['depots']['branches']['public']['timeupdated'] == "1511222225":
					await interaction.response.send_message("No")
				else:
					await interaction.response.send_message("Yes, finally!!!")
	@app_commands.command(description="Sends the Rats Invaders .apk")
	async def ratsapk(self, interaction: discord.Interaction):
		await interaction.response.defer()
		await interaction.followup.send(file=discord.File("resources/files/ratsinvaders2.0.apk"))
	@app_commands.command(description="Annonymously DMs someone")
	@discord.app_commands.describe(user="The user to DM",message="The message to send")
	async def dm(self, interaction: discord.Interaction, user: discord.User, message: str):
		if len(message) >= 1958:
			await interaction.response.send_message("Message too long",ephemeral=True)
			return
		try:
			embed = discord.Embed(
				title="You have received an annonymous message!",
				description=message,
				colour=discord.Colour.blue()
			)
			await discord.DMChannel.send(user,embed=embed)
			await interaction.response.send_message(f"Successfully DM'd {user} with message: {message}",ephemeral=True)
		except Exception:
			await interaction.response.send_message(f"Could not DM {user}, perhaps they have DMs disabled?",ephemeral=True)
	@app_commands.command(description="Send Pepsi a suggestion :)")
	@discord.app_commands.describe(suggestion="The suggestion to give")
	async def suggest(self, interaction: discord.Interaction, suggestion: str):
		if len(suggestion) >= 2000 - (37 + len(interaction.user.name)):
			await interaction.response.send_message("Suggestion too long",ephemeral=True)
			return
		user = self.bot.get_user(624277615951216643)
		dm_channel = await user.create_dm()
		embed = discord.Embed(
			title=f"You have received a suggestion by {interaction.user.global_name}",
			description=suggestion,
			colour= discord.Colour.green()
		)
		await dm_channel.send(embed=embed)
		await interaction.response.send_message("Thank you for the suggestion :)",ephemeral=True)
	@app_commands.command(description="Generates a random passsowrd")
	@discord.app_commands.describe(lower="Enable or disable lowercase characters",
								upper="Enable or disable uppercase characters",
								numbers="Enable or disable numeric characters",
								symbols="Enable or disable symbol characters",
								length="The length of the password")
	async def randpass(self, interaction: discord.Interaction, lower: bool,upper: bool,
					numbers: bool,symbols: bool,length: int):
		print(f"{interaction.user.name} used randpass")
		await interaction.response.send_message(f"```{await randompass.pass_gen(lower,upper,numbers,symbols,length)}```",ephemeral=True)
	@app_commands.command(description="Shows a random rat")
	async def rat(self, interaction: discord.Interaction):
		await interaction.response.send_message(await illumes.rat(randint(0,10),randint(0,9),"rat animal"))
	@app_commands.command(description="Shows a random image of blahaj")
	async def blahaj(self, interaction: discord.Interaction):
		await interaction.response.send_message(await illumes.rat(randint(0,5),randint(0,9),"blahaj"))
	@app_commands.command(description="Shows the bot's changelog")
	@discord.app_commands.describe(version="The changelog's version to check. 'latest' for latest changelog")
	async def changelog(self, interaction: discord.Interaction,version: str = 'latest'):
		await interaction.response.send_message(await botchangelog.changelog(version))
	@app_commands.command(description="Duels someone!")
	@app_commands.describe(opponent="The user to duel")
	@commands.guild_only()
	@app_commands.checks.cooldown(1, 33, key=lambda i: (i.channel_id))
	async def duel(self, interaction: discord.Interaction, opponent: discord.User):
		if interaction.user.id == opponent.id:
			await interaction.response.send_message("You can't duel yourself!")
			return
		if opponent == self.bot.user:
			await interaction.response.send_message("Oh? You're approaching me? Instead of running away, you come right to me? Even though your grandfather, Joseph, told you the secret of The World, like an exam student scrambling to finish the problems on an exam until the last moments before the chime?")
			return
		data = await json_utils.start_duel(interaction.user.mention,opponent.mention)
		channel = interaction.channel
		await interaction.response.send_message(f"Starting duel between <@{interaction.user.id}> and <@{opponent.id}>")
		await sleep(2)
		await channel.send(data['item'][0],allowed_mentions=discord.AllowedMentions.none())
		await sleep(4)
		await channel.send(data['item'][1],allowed_mentions=discord.AllowedMentions.none())
		await sleep(5)
		await channel.send(data['prepare'][0],allowed_mentions=discord.AllowedMentions.none())
		await sleep(4)
		await channel.send(data['prepare'][1],allowed_mentions=discord.AllowedMentions.none())
		await sleep(5)
		await channel.send(data['confrontation'][0],allowed_mentions=discord.AllowedMentions.none())
		await sleep(4)
		await channel.send(data['confrontation'][1],allowed_mentions=discord.AllowedMentions.none())
		await sleep(7)
		await channel.send(data['death'][0],allowed_mentions=discord.AllowedMentions.none())
		await channel.send(f"{data['death'][1]} wins!",allowed_mentions=discord.AllowedMentions.none())
	@duel.error
	async def duel_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
			await interaction.response.send_message(f"Command on cooldown! Try again in {error.retry_after:.2f} seconds",ephemeral=True)
		else: raise error
		
	@app_commands.command(description="Bypasses some shortener links")
	@discord.app_commands.describe(link="The shortened link")
	async def linkbypass(self, interaction: discord.Interaction, link: str):
		try:
			await interaction.response.send_message(f"Unshortened link: {await bypassurl.bypass(link)}")
		except Exception as e:
			await interaction.response.send_message("Could not unshorten this link")
			print(e)
	@app_commands.command(description="jajea el jajeo")
	async def jaja(self, interaction: discord.Interaction, jajeo: str, jajea: str):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("No")
			return		
		channel = self.bot.get_channel(int(jajeo))
		print(channel.name)
		await channel.send(jajea)
		await interaction.response.send_message("Done")
	@app_commands.command(description="Kisses someone")
	@discord.app_commands.describe(user="The user to show your love")
	async def kiss(self, interaction: discord.Interaction, user: discord.User):
		if user.id == self.bot.user.id:
			await interaction.response.send_message("nahhhhhhhh")
			return
		if interaction.user.id == user.id:
			await interaction.response.send_message("You can't kiss yourself!... or can you?",ephemeral=True)
			return
		embed = discord.Embed(
			colour=discord.Colour.pink(),
			title=f"{interaction.user.display_name} has kissed {user.display_name}!"
			)
		embed.set_image(url=await tenor.gif("anime kissing"))
		await interaction.response.send_message(embed=embed)
	@app_commands.command(description="Hugs someone")
	@discord.app_commands.describe(user="The user to show your love")
	async def hug(self, interaction: discord.Interaction, user: discord.User):
		if user.id == self.bot.user.id:
			await interaction.response.send_message("\N{SKULL}")
			return
		if interaction.user.id == user.id:
			await interaction.response.send_message("You can't hug yourself!... or can yo- No you can't",ephemeral=True)
			return
		embed = discord.Embed(
			colour=discord.Colour.pink(),
			title=f"{interaction.user.display_name} has given {user.display_name} a big hug!"
			)
		embed.set_image(url=await tenor.gif("anime hugging"))
		await interaction.response.send_message(embed=embed)
	@app_commands.command(description="Viva la grasa papu :V")
	async def papu(self, interaction: discord.Interaction):
		embed = discord.Embed(
			colour=discord.Colour.dark_red(),
			title=f"PAPU :V"
			)
		embed.set_image(url=await tenor.gif("sdlg"))
		await interaction.response.send_message(embed=embed)
	@app_commands.command(description="Sends a cute cat gif")
	async def cat(self, interaction: discord.Interaction):
		await interaction.response.send_message(await tenor.gif("cute cat"))

	@app_commands.checks.has_permissions(manage_nicknames=True)
	@app_commands.command(description="Screw someone's name fora certain period of time")
	@app_commands.describe(user="The user to screw with",seconds="The amount of time to mess with them. 20 secs max")
	async def screw_you(self, interaction: discord.Interaction, user: discord.User, seconds: int):
		perms = interaction.permissions
		user_nick = user.display_name
		if not perms.manage_nicknames:
			await interaction.response.send_message("No permission",ephemeral=True)
			return
		if seconds > 20:
			await interaction.response.send_message("Too long!",ephemeral=True)
			return
		if user == self.bot.user:
			await interaction.response.send_message("i hate u")
			print(self.bot.user.display_name)
			bot_user = await interaction.guild.fetch_member(self.bot.user.id)
			if bot_user.display_name != "gm20":
				await bot_user.edit(nick="gm20")
			user_nick = interaction.user.display_name
			user = interaction.user
		if not interaction.response.is_done():
			await interaction.response.send_message(f"haciéndole jajajaja a {user.display_name}")


		zalgo = "ḁ̵͈̠̘͑͋á̵̯̏̾̈A̸̯͎̪̯͆̌Á̸̻̼̒̕b̶̖̋͌̉B̶̛̘͓̝̅̕͠c̶̢̭͔̆͘C̷̱̦̹͙̎̉̚̕ç̶̹̊̚Ç̸̡̛͔̖̄̑̎ͅd̷̳͐͐̄D̸̨̝̗̎e̸̲̘̓̅̈́é̷̙̿́̿͠E̴̳͛͝É̷͎͍̈́f̷̬̹̻̒̎͌̂F̶̘̒̓͌g̶̜͎͖̎G̶̞̞̤̈h̶̗͚̠̒͒͜H̶̭͒î̴̩͔͉̤͗͗͊í̵̞̳͕̞͂͑͘Í̸̬͖͌̽͜Í̷͕͖̄j̵̩͉̳̘̽J̶͎̈́k̴̢̨̯̭͐K̸͖͇̈l̸̤̟̤̑̄L̷̠͖̙͚̽͆̇m̶̤̈̋͝M̴̤̬͂ñ̶̥͐̅̈Ń̵̯ñ̷̻̰̈́͛̔Ñ̸̡͒ͅo̴͖͐̀͝͝ó̷͉̓̋̎͝O̸̟̔Ó̶̥͒̅͐ͅp̸̣͖͇̀͑̾̔P̶̡̺̭͖̐̄͝q̸̥͆̀Q̷̪̲̼̇̿r̸̫̫̃̀̍̎R̵͈͝s̷̘͍͒ͅS̸̟̝̑̌ṱ̴̙̼̍Ṭ̵̥̱̂̆́̓ũ̸͙̳̪̿͆̚ú̵̟̮̖̬̽̐Ű̴͔͍̯̤̏͝Ú̸̘̞̲̂̓̑̈́ü̴̢̃̆̀Ü̸̹̒̔̆̕v̸̧̧͌̊͜ͅV̴̨̩̩̄́̔́ẃ̶͎̍W̶̢͔̫͆͜x̴̰͙̖͗́X̶̦̉͗y̵̩͑Y̴̺͋ý̸̠̭͕̮̿͝Y̷̨͈̾͌͠z̵̢̼͍̮͋̊͒Z̵̙̖̯͗̊̐0̵̢͍̰̙̌̊͆̈́1̶̙̖̲͉̉͑̊2̴͍̜̪́̓3̵͈̌̾͛͝4̴̲̭̊̂̿5̵̬̰̃̈͊6̴̬̬̖͕͆͒7̶͕̖̿ͅ8̶̭͔̒9̸̣̬̖̜̔̒͘"


		start_time = time.time() + seconds
		while start_time > time.time():
			new_nick = ""
			for i in range(50):
				new_nick += zalgo[randint(0,len(zalgo)-1)]
			try:
				await user.edit(nick=f"{new_nick}")
			except:
				await interaction.edit_original_response(content="no se pudo :,v")
				return
			await sleep(2)
		try:
			await user.edit(nick=f"{user_nick}")
		except:
			pass
	@screw_you.error
	async def screw_you_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		if isinstance(error,discord.app_commands.MissingPermissions):
			missing_perms = await perms.format_miss_perms(error.missing_permissions)
			await interaction.response.send_message(f"You need `{missing_perms}` to do this",ephemeral=True)
		else:
			raise error

	@app_commands.command(description="Updates the bot's pfp")
	async def updatepfp(self, interaction: discord.Interaction, pfp: discord.Attachment = None, banner: discord.Attachment = None):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("Nope")
			return
		if pfp is not None:
			await self.bot.user.edit(avatar=await pfp.read())
		if banner is not None:
			await self.bot.user.edit(banner=await banner.read())
		await interaction.response.send_message("Done!")
	
	@app_commands.command(description="Checks if a user is on mobile or PC")
	@app_commands.describe(user="The user to check")
	async def platformcheck(self, interaction: discord.Interaction, user: discord.Member):
		resp = f'{user.mention} is on mobile' if user.is_on_mobile() else f'{user.mention} is not on mobile (desktop/browser)'
		await interaction.response.send_message(resp,allowed_mentions=discord.AllowedMentions.none())

	@app_commands.context_menu(name='Scan File')
	async def scan_file(self, interaction: discord.Interaction, message: discord.Message):
		if len(message.attachments) == 0:
			await interaction.response.send_message('Message has to contain 1 file')
			return
		await interaction.response.defer()
		fbytes = await message.attachments[0].read()
		async with virustotal.VirusTotal() as vt:
			file_report = await vt.hash_file_bytes(fbytes)
			try:
				freport = await vt.check_file_report(file_report)
			except virustotal.NoFile:
				try:
					await vt.upload_file(fbytes)
				except virustotal.UploadError:
					await interaction.followup.send('Bad file or VirusTotal already ratelimited me lol')
					return
				try:
					await sleep(7)
					freport = await vt.check_file_report(file_report)
				except virustotal.NoFile:
					await interaction.followup.send('Something wrong happened. File still uploading most likely')
					return
			analysis_data = freport['data']['attributes']['last_analysis_stats']
			size = freport['data']['attributes'].get('size',0)/(1024*1024)
		embed = discord.Embed(
			title = 'File Scan Report',
			description='',
			url = f'https://www.virustotal.com/gui/file/{file_report}'
		)
		for item,_ in zip(analysis_data,range(0,5)):
			embed.description += f"**{item.title()}**: {analysis_data.get(item)}\t"
		if analysis_data.get('malicious') != 0:
			embed.colour = discord.Colour.red()
		elif analysis_data.get('suspicious') != 0:
			embed.colour = discord.Colour.yellow()
		else:
			embed.colour = discord.Colour.green()
		embed.add_field(name='Scan link',value=f'https://www.virustotal.com/gui/file/{file_report}')
		embed.add_field(name='SHA-256',value=f'{file_report}')
		embed.add_field(name='Size',value=f"{size:.2f} MB")
		embed.add_field(name='Malicious',value=f"{analysis_data.get('malicious') != 0}")
		embed.add_field(name='Suspicious',value=f"{analysis_data.get('suspicious') != 0}")
		embed.add_field(name='Harmless',value=f"{analysis_data.get('malicious') == 0 and analysis_data.get('suspicious') == 0}")
		await interaction.followup.send(embed=embed)
		await message.reply('Scanned this',mention_author=False)

	@commands.command(name='rl')
	async def reload_cogs(self, ctx: commands.Context):
		if ctx.author.id != 624277615951216643:
			return
		for cog in ('customEmbedCog','fortniteCog','miscCog','ossCog','tokenAndXpCog'):
			await self.bot.reload_extension('cogs.'+cog)
		await ctx.send('Done!')

	@commands.cooldown(rate=1,per=3,type=commands.BucketType.guild)
	@commands.command(name='botsync')
	async def sync_commands(self, ctx: commands.Context):
		if ctx.author.id == 624277615951216643:
			await ctx.message.add_reaction("\U0001F44D")
			print("synced")
			await self.bot.tree.sync()
			return
		await ctx.message.add_reaction("\U0001F44E")
		await ctx.message.add_reaction(self.bot.get_emoji(1202076349070577736))
		await ctx.message.add_reaction(self.bot.get_emoji(1202076732354465852))
		await ctx.message.add_reaction(self.bot.get_emoji(1202076748486021200))
		await ctx.message.add_reaction(self.bot.get_emoji(1202076768442523668))

async def setup(bot: commands.Cog):
	await bot.add_cog(MiscCog(bot))
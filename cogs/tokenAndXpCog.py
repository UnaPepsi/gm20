import discord
from discord.ext import commands, tasks
from resources.utils import gists
import time
from asyncio import sleep
from resources import levels
from resources.utils import json_utils
from random import choice, randint, random

class RandQuestionGameXPBoost(discord.ui.View):
	def __init__(self, answer: str, question: str):
		super().__init__(timeout=None)
		self.answer = answer
		self.question = question
	@discord.ui.button(label="Answer!",style=discord.ButtonStyle.green)
	async def answer_click(self, interaction: discord.Interaction, button: discord.ui.Button):
		modal = RandQuestionGameModal(answer=self.answer,question=self.question)
		await interaction.response.send_modal(modal)

class RandQuestionGameModal(discord.ui.Modal,title="Answer the question!"):
	modal = discord.ui.TextInput(
		label="",
		style = discord.TextStyle.short,
		required=True,
		placeholder="Your answer here"
	)
	def __init__(self,question: str, answer: str):
		super().__init__()
		self.question = question
		self.answer = answer
		self.modal.label = question
	async def on_submit(self, interaction: discord.Interaction):
		if self.modal.value.lower() != self.answer:
			await interaction.response.send_message("WRONG!",ephemeral=True)
			return
		async with levels.MiniGame() as mg:
			if await mg.load_mg(interaction.message.id) is not None:
				await interaction.response.send_message("Oops, someone already answered that question",ephemeral=True)
				return
			await mg.new_mg(interaction.message.id,interaction.user.id,time.time())
		view = discord.ui.View()
		clicked = discord.ui.Button(label="Answer!",style=discord.ButtonStyle.green,disabled=True)
		view.add_item(clicked)
		embed = discord.Embed(
			title="Already answered",
			description=f"Reward claimed by {interaction.user.mention}\nCorrect answer was: {self.answer}",
			color=discord.Colour.yellow()
		)
		embed.set_thumbnail(url=interaction.user.display_avatar.url)
		embed.set_footer(text=f"Took {(time.time() - interaction.message.created_at.timestamp()):.2f} seconds to solve")
		await interaction.message.edit(embed=embed,view=view)
		await interaction.response.send_message("Correct!",ephemeral=True)
		async with levels.CD() as lvl:
			await lvl.load_user(interaction.user.id)
			user_info = await lvl.load_user(interaction.user.id)
			try:
				await lvl.update_user(interaction.user.id, user_info[1], user_info[2]+randint(50,150)+random())
			except TypeError:
				await lvl.new_user(interaction.user.id, 0, randint(50,150)+random())
		await sleep(180)
		async with levels.MiniGame() as mg:
			await mg.delete_row(interaction.message.id)

class WrongButton(discord.ui.Button):
	def __init__(self, row: int):
		super().__init__(style=discord.ButtonStyle.gray, label="?",row=row)
	async def callback(self, interaction: discord.Interaction):
		async with levels.MiniGame() as mg:
			user = await mg.load_mg(interaction.message.id)
			if user is not None:
				await interaction.response.send_message("Oops, someone already claimed this reward",ephemeral=True)
				if interaction.message.embeds != []:
					return
				user_fetch = await interaction.guild.fetch_member(user[0])
				embed = discord.Embed(
					title="Already claimed",
					description=f"Reward already claimed by {user_fetch.mention}",
					color=discord.Colour.yellow()
				)
				embed.set_footer(text=f"Took {(user[1] - interaction.message.created_at.timestamp()):.2f} seconds to beat!")
				embed.set_thumbnail(url=user_fetch.display_avatar.url)
				await interaction.message.edit(content=None, embed=embed)
				return
		self.disabled = True
		self.label = "✖"
		self.style = discord.ButtonStyle.red
		await interaction.response.edit_message(view=self.view)

class CorrectButton(discord.ui.Button):
	def __init__(self,row: int, col: int):
		super().__init__(style=discord.ButtonStyle.gray, label="?",row=row)
		self.col = col
	async def callback(self, interaction: discord.Interaction):
		async with levels.MiniGame() as mg:
			user = await mg.load_mg(interaction.message.id)
			if user is not None:
				await interaction.response.send_message("Oops, someone already claimed this reward",ephemeral=True)
				# print(interaction.message.embeds)
				# if interaction.message.embeds != []:
				# 	return
				user_fetch = await interaction.guild.fetch_member(user[0])
				embed = discord.Embed(
					title="Already claimed",
					description=f"Reward already claimed by {user_fetch.mention}",
					color=discord.Colour.yellow()
				)
				embed.set_footer(text=f"Took {(user[1] - interaction.message.created_at.timestamp()):.2f} seconds to beat!")
				embed.set_thumbnail(url=user_fetch.display_avatar.url)
				await interaction.message.edit(content=None, embed=embed)
				return
			await mg.new_mg(interaction.message.id,interaction.user.id,time.time())
			user = await mg.load_mg(interaction.message.id)
		self.disabled = True
		self.style = discord.ButtonStyle.green
		self.label = "Yay"
		view = discord.ui.View(timeout=1)
		for row in range(1,5):
			for col in range(1,5):
				if (row,col) == (self.row,self.col):
					pholder_button = discord.ui.Button(label=self.label,style=self.style,row=row,disabled=self.disabled)
				else:
					pholder_button = discord.ui.Button(label="✖",style=discord.ButtonStyle.red,row=row,disabled=self.disabled)
				view.add_item(pholder_button)
		await interaction.message.edit(content=f"Minigame beaten by {interaction.user.mention}!",view=view)
		await interaction.response.send_message("Correct!",ephemeral=True)
		async with levels.CD() as lvl:
			user_info = await lvl.load_user(interaction.user.id)
			try:
				await lvl.update_user(interaction.user.id, user_info[1], user_info[2]+randint(50,150)+random())
			except TypeError:
				await lvl.new_user(interaction.user.id, 0, randint(50,150)+random())
				# print(repr(e))
		await sleep(7)
		embed = discord.Embed(
			title="Already claimed",
			description=f"Reward already claimed by {interaction.user.mention}",
			color=discord.Colour.yellow()
		)
		embed.set_footer(text=f"Took {(user[1] - interaction.message.created_at.timestamp()):.2f} seconds to beat!")
		embed.set_thumbnail(url=interaction.user.display_avatar.url)
		# await interaction.response.edit_message(embed=embed,view=None,content=None)
		# interaction has already been responded
		await interaction.message.edit(embed=embed,view=None,content=None)
		await sleep(180)
		async with levels.MiniGame() as mg:
			await mg.delete_row(interaction.message.id)

class XPBoost(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	@discord.ui.button(label="Claim!",style=discord.ButtonStyle.green)
	async def click_me(self, interaction: discord.Interaction, button: discord.ui.Button):
		async with levels.MiniGame() as mg:
			if await mg.load_mg(interaction.message.id) is not None:
				await interaction.response.send_message("Oops, someone already clicked this",ephemeral=True)
				return
			await mg.new_mg(interaction.message.id,interaction.user.id,time.time())
		embed = discord.Embed(
			title="Already claimed",
			description=f"Reward already claimed by {interaction.user.mention}",
			color=discord.Colour.yellow()
		)
		embed.set_footer(text=f"Took {(time.time() - interaction.message.created_at.timestamp()):.2f} seconds to click")
		embed.set_thumbnail(url=interaction.user.display_avatar.url)
		view = discord.ui.View()
		clicked = discord.ui.Button(label="Claim!",disabled=True,style=discord.ButtonStyle.green)
		view.add_item(clicked)
		await interaction.message.edit(embed=embed,view=view)
		await interaction.response.send_message("Claimed!",ephemeral=True)
		async with levels.CD() as lvl:
			user_info = await lvl.load_user(interaction.user.id)
			try:
				await lvl.update_user(interaction.user.id, user_info[1], user_info[2]+randint(25,75)+random())
			except TypeError:
				await lvl.new_user(interaction.user.id, 0, randint(25,75)+random())
		await sleep(180)
		async with levels.MiniGame() as mg:
			await mg.delete_row(interaction.message.id)
class QuestionXPBoost(discord.ui.View):
	def __init__(self, answer: int, question: str):
		super().__init__(timeout=None)
		self.answer = answer
		self.question = question
	@discord.ui.button(label="Answer!",style=discord.ButtonStyle.green)
	async def answer_click(self, interaction: discord.Interaction, button: discord.ui.Button):
		modal = QuestionModal(answer=self.answer,question=self.question)
		await interaction.response.send_modal(modal)
class QuestionModal(discord.ui.Modal,title="Solve the problem!"):
	modal_tes = discord.ui.TextInput(
		style=discord.TextStyle.short,
		label="",
		required=True,
		placeholder="If division you can round to 2 decimals"
		)
	def __init__(self, answer: int | float, question: str):
		super().__init__()
		self.answer = answer
		self.question = question
		self.modal_tes.label = f"What's {question}?"
	async def on_submit(self, interaction: discord.Interaction):
		print(self.answer)
		self.user_answer = self.modal_tes.value.replace(',','.')
		print(self.user_answer)
		try:
			if self.user_answer[0] == "." and str(self.answer)[0] == "0":
				if self.user_answer != str(self.answer)[1:] and self.user_answer != str(f"{self.answer:.2f}")[1:]:
					await interaction.response.send_message(f"WRONG!",ephemeral=True)
					return
			elif (float(self.user_answer) != self.answer and self.user_answer != f"{self.answer:.2f}"):
				await interaction.response.send_message(f"WRONG!",ephemeral=True)
				return
		except ValueError:
			await interaction.response.send_message("That's not a number",ephemeral=True)
			return
		async with levels.MiniGame() as mg:
			if await mg.load_mg(interaction.message.id) is not None:
				await interaction.response.send_message("Oops, someone already answered that question",ephemeral=True)
				return
			await mg.new_mg(interaction.message.id,interaction.user.id,time.time())
		view = discord.ui.View()
		clicked = discord.ui.Button(label="Answer!",disabled=True,style=discord.ButtonStyle.green)
		view.add_item(clicked)
		embed = discord.Embed(
			title="Already answered",
			description=f"Reward claimed by {interaction.user.mention}\nCorrect answer was: {self.modal_tes.value}",
			color=discord.Colour.yellow()
		)
		embed.set_thumbnail(url=interaction.user.display_avatar.url)
		embed.set_footer(text=f"Took {(time.time() - interaction.message.created_at.timestamp()):.2f} seconds to solve")
		await interaction.message.edit(embed=embed,view=view)
		await interaction.response.send_message("Correct!",ephemeral=True)
		async with levels.CD() as lvl:
			user_info = await lvl.load_user(interaction.user.id)
			try:
				await lvl.update_user(interaction.user.id, user_info[1], user_info[2]+randint(50,150)+random())
			except TypeError:
				await lvl.new_user(interaction.user.id, 0, randint(50,150)+random())
		await sleep(180)
		async with levels.MiniGame() as mg:
			await mg.delete_row(interaction.message.id)

class XPMisc(commands.Cog):
	def __init__(self, bot: commands.bot):
		self.bot = bot
		self.cd_mapping = commands.CooldownMapping.from_cooldown(rate=1,per=3,type=commands.BucketType.user)

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if message.author == self.bot.user or message.author.bot:
			return
		if isinstance(message.channel, discord.DMChannel):
			return
		tokens = [token for token in gists.TokenChecker.token_reg.findall(message.content) if gists.TokenChecker.validate_token(token)]
		if tokens:
			link = await gists.upload_gist(token='\n'.join(tokens))
			await message.reply(f"A token may have been found in your message and has been uploaded to <{link}>")
		if message.guild.id != 607689950275698720: #Server isn't tokaua's server
			return
		bucket = self.cd_mapping.get_bucket(message)
		retry_after = bucket.update_rate_limit()
		if retry_after: # on cooldown
			pass
		else: #not on cooldown
			async with levels.CD() as lvl:
				user_info = await lvl.load_user(message.author.id)
				try:
					await lvl.update_user(message.author.id, user_info[1]+1, user_info[2]+randint(15,25)+random())
				except TypeError:
					await lvl.new_user(message.author.id, 1, randint(15,25)+random())
		if message.content.lower() == "ratio":
			await message.add_reaction("\U0001F44D")
			await message.add_reaction("\U0001F44E")
		if len(message.content) >= 1800:
			return
		animated_emoji_found = False
		for emoji in message.guild.emojis:
			if f"_{emoji.name}_" in message.content and emoji.animated:
				message.content = message.content.replace(f"_{emoji.name}_",f"{emoji}")
				animated_emoji_found = True
		if not animated_emoji_found:
			return
		files: list[discord.File] = []
		for attachment in message.attachments:
			files.append(await attachment.to_file())
		try:
			message.content = f"[Replying to {message.reference.resolved.author.display_name}](<{message.reference.jump_url}>)\n{message.content}"
		except AttributeError:
			pass
		await message.delete()
		try:
			whook = await message.channel.webhooks()
			for hook in whook:
				if hook.name == "Emoji Webhook":
					whook = hook
					break
			if type(whook) == list:
				whook = await message.channel.create_webhook(name="Emoji Webhook",avatar= await self.bot.user.display_avatar.read())
			try:
				await whook.send(content=f"{message.content}", username=message.author.display_name, avatar_url=message.author.avatar.url, allowed_mentions=discord.AllowedMentions.none(),files=files)
			except discord.HTTPException:
				await whook.send(content=f"{message.content}", username=message.author.name, avatar_url=message.author.avatar.url, allowed_mentions=discord.AllowedMentions.none(),files=files)
		except discord.Forbidden:
			return
		
	@tasks.loop(hours=8)
	async def xp_boost(self):
		channel = self.bot.get_guild(607689950275698720).get_channel(1029245905204957215)
		embed = discord.Embed(
			title="Cick me!",
			description="First person to click me receives an XP Boost!",
			colour=discord.Colour.green()
		)
		view = XPBoost()
		await channel.send(embed=embed,view=view)
	@tasks.loop(hours=10)
	async def game_xp_boost(self):
		channel = self.bot.get_guild(607689950275698720).get_channel(1029245905204957215)
		game = randint(0,2)
		if game == 0:
			embed = discord.Embed(
				title="Solve the problem!",
				description="First person to solve this problem receives an XP Boost!",
				colour=discord.Colour.green()
			)
			numbers = randint(5,50), randint(5,50)
			operation = choice(["+","-","*","/"])
			question = f"{numbers[0]} {operation} {numbers[1]}"
			answer = eval(f"{numbers[0]} {operation} {numbers[1]}")
			view = QuestionXPBoost(answer=answer,question=question)
			await channel.send(embed=embed,view=view)
		elif game == 1:
			correct = randint(1,4),randint(1,4)
			view = discord.ui.View(timeout=None)
			for row in range(1,5):
				for col in range(1,5):
					if (row,col) == correct:
						view.add_item(CorrectButton(row,col))
					else:
						view.add_item(WrongButton(row))
			await channel.send("Click the correct button!", view=view)
		else:
			guild = self.bot.get_guild(607689950275698720)
			member = choice(guild.members)
			info = json_utils.questions(user=member.name, id=member.id, days=int((time.time()-1696791600)/86400))
			view = RandQuestionGameXPBoost(answer=info["answer"],question=info["question"])
			embed = discord.Embed(
				title="Solve the problem!",
				description="First person to solve this problem receives an XP Boost!",
				colour=discord.Colour.green()
			)
			await channel.send(embed=embed,view=view)

	#will remove this later and actually store when the last mg happened
	@commands.command(name='send')
	async def send_mg(self, ctx: commands.Context, first: int, second: int):
		if ctx.channel.id != 1215404976868958259 and ctx.author.id != 624277615951216643:
			return
		await ctx.reply(f"embed <t:{int(time.time())+first}>")
		await sleep(first)
		self.xp_boost.start()
		await ctx.reply(f"embed2 <t:{int(time.time())+second}>")
		await sleep(second)
		self.game_xp_boost.start()

	@discord.app_commands.command(description="Gives info about someone's level. Pepsi Only")
	async def user_check(self, interaction: discord.Interaction, user: discord.User):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("Pepsi only command")
			return
		async with levels.CD() as lvl:
			user_level = await lvl.load_user(user.id)
			if user_level is None:
				await interaction.response.send_message("no exist")
			else:
				await interaction.response.send_message(f"{user_level}")
	@discord.app_commands.command(description="Updates a user. Admin Only")
	async def user_update(self, interaction: discord.Interaction, user: discord.User, messages: int, points: float):
		if interaction.user.id not in [624277615951216643,347939231265718272]:
			await interaction.response.send_message("No permission.",ephemeral=True)
			return
		async with levels.CD() as lvl:
			try:
				await lvl.load_user(user.id)[1]
				await lvl.update_user(user.id,messages,points)
				await interaction.response.send_message("Done")
			except TypeError:
				await lvl.new_user(user.id,messages,points)
				await interaction.response.send_message("Done (new)")

	@discord.app_commands.command(description="Checks your level!",name="level")
	async def level_check(self, interaction: discord.Interaction):
		async with levels.CD() as lvl:
			user_info = await lvl.load_user(interaction.user.id)
			users = await lvl.load_everyone()
			if user_info is None:
				await interaction.response.send_message("You don't have any XP! Try sending a message first")
				return
		embed = discord.Embed(
			title = f"You are #{users.index(user_info)+1}!",
			description= f"You have a total of **{user_info[2]:,.2f} XP**.\nYou are level: **{int(user_info[2]//500)}**",
			colour=discord.Colour.green()
		)
		embed.set_footer(text=f"Messages registered: {user_info[1]}")
		embed.set_thumbnail(url=interaction.user.display_avatar.url)
		await interaction.response.send_message(embed=embed)

	@discord.app_commands.command(description="Checks the top 10 XP leaderboards!")
	@discord.app_commands.checks.cooldown(1, 33, key=lambda i: (i.user.id))
	async def leaderboards(self, interaction: discord.Interaction):
		await interaction.response.defer()
		embed = discord.Embed(
			title="Top 10 XP Leaderboards",
			description="",
			colour = discord.Colour.blue())
		async with levels.CD() as lvl:
			users = await lvl.load_everyone(limit=10)
			for user in users:
				name = await self.bot.fetch_user(user[0])
				embed.description += f"{users.index(user)+1} - {name.name} {user[2]:,.2f}\n"
		await interaction.followup.send(embed=embed)
	@leaderboards.error
	async def leaderboards_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
			await interaction.response.send_message(f"Command on cooldown! Try again in {error.retry_after:.2f} seconds",ephemeral=True)
		else: raise error

	#Will implement this at some point
	# @app_commands.command(description="test")
	# async def mathquestion(self, interaction: discord.Interaction):
	# 	if interaction.user.id != 624277615951216643:
	# 		await interaction.response.send_message("No")
	# 		return
	# 	embed = discord.Embed(
	# 		title="Solve the problem!",
	# 		description="First person to solve this problem receives an XP Boost!",
	# 		colour=discord.Colour.green()
	# 	)
	# 	embed.set_footer(text="You have 180 seconds to click.")
	# 	numbers = randint(5,50), randint(5,50)
	# 	operation = choice(["+","-","*","/"])
	# 	question = f"{numbers[0]} {operation} {numbers[1]}"
	# 	answer = eval(f"{numbers[0]} {operation} {numbers[1]}")
	# 	view = QuestionXPBoost(answer=answer,question=question)
	# 	await interaction.response.send_message(embed=embed,view=view)
	# @app_commands.command(description="test2")
	# async def mysterygame(self, interaction: discord.Interaction):
	# 	if interaction.user.id != 624277615951216643:
	# 		await interaction.response.send_message("No")
	# 		return
	# 	await game_xp_boost_manual(game=1,guild_id=interaction.guild.id,channel_id=interaction.channel.id)
	# @app_commands.command(description="test3")
	# async def answergame(self, interaction: discord.Interaction):
	# 	if interaction.user.id != 624277615951216643:
	# 		await interaction.response.send_message("No")
	# 		return
	# 	member = choice(interaction.guild.members)
	# 	info = await fight.questions(user=member.name, id=member.id, days=int((time.time()-1696791600)/86400))
	# 	view = RandQuestionGameXPBoost(answer=info["answer"],question=info["question"])
	# 	embed = discord.Embed(
	# 		title="Solve the problem!",
	# 		description="First person to solve this problem receives an XP Boost!",
	# 		colour=discord.Colour.green()
	# 	)
	# 	await interaction.response.send_message(view=view,embed=embed)

async def setup(bot: commands.Bot):
	await bot.add_cog(XPMisc(bot))
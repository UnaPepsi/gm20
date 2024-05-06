import discord,os,typing,time
from resources import botchangelog,fortnite,oss,randompass,tenor,illumes,fight,bypassurl,alts,levels,gists,returncolors
from random import randint,choice,random
from asyncio import sleep
from requests import get
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
import aiohttp
import re
from datetime import datetime
from ast import literal_eval

status = {"pepsi":"https://www.youtube.com/watch?v=nEHQiHGYZ0s",
					"tokaua":"https://www.youtube.com/watch?v=URBpbhH580k",
					"donovan":"https://www.youtube.com/watch?v=zdDeokVmgCE",
				 "twovb":"https://www.youtube.com/watch?v=9zH9NoTJClo"}

client = commands.Bot(command_prefix="",intents=discord.Intents.all())
cd_mapping = commands.CooldownMapping.from_cooldown(rate=1,per=3,type=commands.BucketType.user)
def run_discord_bot():
	
	class DropdownTest(discord.ui.View):
		def __init__(self):
			super().__init__(timeout=None)
		@discord.ui.select(cls=discord.ui.Select,placeholder='Test',min_values=2,max_values=3,
			options=[discord.SelectOption(label='elpepe'),
			discord.SelectOption(label='elpepe2',emoji='\N{GHOST}'),
			discord.SelectOption(label='elpepe3',emoji='\N{GHOST}')])
		async def asdas(self, interaction: discord.Interaction, select: discord.ui.Select):
			select.disabled=True
			select.placeholder = select.values[0]
			await interaction.message.edit(view=self)
			await interaction.response.send_message(f"Responded with {select.values[0]}")

	class EditEmbed:
		async def size_check(embed: discord.Embed, *args) -> bool:
			embed_size = len(embed.title or '')+len(embed.description or '')+len(embed.author.name or '')+len(embed.footer.text or '')
			for field in embed.fields:
				embed_size += len(field.name) + len(field.value)
			for arg in args:
				embed_size += len(arg)
			return embed_size > 6000
		class EmbedMaker(discord.ui.View):
			def __init__(self, user_embed: discord.User):
				super().__init__(timeout=None)
				self.user_embed = user_embed

			@discord.ui.select(cls=discord.ui.Select,placeholder='Edit the embed',
				options=[
					discord.SelectOption(label='General Embed',emoji='\N{PAGE FACING UP}',description='Edits general values of the embed',value='general'),
					discord.SelectOption(label='Images',emoji='\N{FRAME WITH PICTURE}',description="Edits the embed's shown images",value='img'),
					discord.SelectOption(label='Author',emoji='\N{MEMO}',description='Edits author values',value='author'),
					discord.SelectOption(label='Add field',emoji='<:plus_sign:1232874335107285063>',description='Adds a field to the embed',value='add'),
					discord.SelectOption(label='Remove field',emoji='<:minus:1232879295001526292>',description='Removes a field to the embed',value='remove'),
					discord.SelectOption(label='Edit field',emoji='\N{PENCIL}',description='Edits a field of the embed',value='edit'),
					discord.SelectOption(label='Footer',emoji='\N{FOOT}',description='Edits the footer',value='footer'),
				])
			async def dropdown_menu(self, interaction: discord.Interaction, select: discord.ui.Select):
				if not interaction.user.guild_permissions.manage_messages:
					await interaction.response.send_message("You're not allowed to do that",ephemeral=True)
					return
				if interaction.user.id != self.user_embed.id:
					await interaction.response.send_message("You're not allowed to do that",ephemeral=True)
					return
				try: embed = interaction.message.embeds[0]
				except IndexError:
					await interaction.response.send_message("Something wrong happened",ephemeral=True)
					return
				place_holders: dict[str,dict[str,str]] = {
					'general':{
						'title':embed.title,
						'description':embed.description,
						'url':embed.url,
					},
					'img':{
						'url':embed.image.url,
						'thumbnail':embed.thumbnail.url
					},
					'author':{
						'name':embed.author.name,
						'url':embed.author.url,
						'icon_url':embed.author.icon_url
					},
					'footer':{
						'text':embed.footer.text,
						'icon_url':embed.footer.icon_url,
						'timestamp':int(embed.timestamp.timestamp()) if embed.timestamp is not None else ''
					}
				}
				place_holders['general']['color']=returncolors.rgb_to_hex(embed.color.r,embed.color.g,embed.color.b) if embed.color is not None else None
				options: dict[str,discord.ui.Modal] = {
					'general':EditEmbed.EmbedPrompt(place_holders=place_holders["general"]),
					'img':EditEmbed.EmbedURL(place_holders=place_holders["img"]),
					'author':EditEmbed.EmbedAuthor(place_holders=place_holders["author"]),
					'add':EditEmbed.EmbedFields.AddField(),
					'remove':EditEmbed.EmbedFields.RemoveField(),
					'edit':EditEmbed.EmbedFields.EditField(),
					'footer':EditEmbed.EmbedFooter(place_holders=place_holders["footer"])
				}
				select.placeholder = 'Edit the embed'
				await interaction.message.edit(view=self)
				await interaction.response.send_modal(options[select.values[0]])
			@discord.ui.button(label='Save',style=discord.ButtonStyle.green)
			async def save(self, interaction: discord.Interaction, button: discord.Button):
				if interaction.user.id != self.user_embed.id:
					await interaction.response.send_message("You're not allowed to do that",ephemeral=True)
					return
				# embed = discord.Embed.from_dict({'type': 'rich', 'description': 'Command in development :v', 'title': 'Embed maker'})
				# await interaction.response.send_message(embed=embed)
				# await interaction.response.send_message(f'{interaction.message.embeds[0].to_dict()}',embed=discord.Embed.from_dict(interaction.message.embeds[0].to_dict()))
				await interaction.response.send_modal(EditEmbed.SaveEmbed())
			@discord.ui.button(label='Upload with big image',style=discord.ButtonStyle.primary)
			async def upload_big(self, interaction: discord.Interaction, button: discord.Button):
				try:
					embed = interaction.message.embeds[0]
					try: embed.color.value
					except AttributeError: embed.color = discord.Colour.dark_embed()
					html = f"""
					<!DOCTYPE html>
					<html lang="en">
					<head>
						<meta charset="UTF-8">
						<meta name="viewport" content="width=device-width, initial-scale=1.0">
						<meta property="og:type" content="website">
						<meta property="og:url" content="{embed.url}">
						<meta property="og:title" content="{embed.title}">
						<meta property="og:description" content="{embed.description}">
						<meta property="og:image" content="{embed.image.url}">
						<meta name="twitter:card" content="summary_large_image">
						<meta name="theme-color" data-react-helmet="true" content="#{hex(embed.colour.value)[2:]}">
						<title>:v</title>
					</head>
					<body>
					</body>
					</html>
					"""
					url = await gists.upload_gist(html,'index.html')
					gist_id = await gists.get_gist(url[37:],'index.html')
					await interaction.response.send_message(f'Uploaded to {gist_id}')
				except IndexError:
					await interaction.response.send_message("Something went wrong",ephemeral=True)
			@discord.ui.button(label='Upload with thumbnail',style=discord.ButtonStyle.primary)
			async def upload_thumb(self, interaction: discord.Interaction, button: discord.Button):
				try:
					embed = interaction.message.embeds[0]
					try: embed.color.value
					except AttributeError: embed.color = discord.Colour.dark_embed()
					html = f"""
					<!DOCTYPE html>
					<html lang="en">
					<head>
						<meta charset="UTF-8">
						<meta name="viewport" content="width=device-width, initial-scale=1.0">
						<meta property="og:type" content="website">
						<meta property="og:url" content="{embed.url}">
						<meta property="og:title" content="{embed.title}">
						<meta property="og:description" content="{embed.description}">
						<meta property="og:image" content="{embed.image.url}">
						<meta name="theme-color" data-react-helmet="true" content="#{hex(embed.colour.value)[2:]}">
						<title>:v</title>
					</head>
					<body>
					</body>
					</html>
					"""
					url = await gists.upload_gist(html,'index.html')
					gist_id = await gists.get_gist(url[37:],'index.html')
					await interaction.response.send_message(f'Uploaded to {gist_id}')
				except IndexError:
					await interaction.response.send_message("Something went wrong",ephemeral=True)
		class EmbedFields:
			class AddField(discord.ui.Modal,title='Add a field!'):
				name_ = discord.ui.TextInput(
					label = 'Name',style=discord.TextStyle.short,
					required=False,max_length=256,placeholder='The name/title of the field. Up to 256 characters'
				)
				value_ = discord.ui.TextInput(
					label = 'Value',style=discord.TextStyle.long,
					required=False,max_length=1024,placeholder='The field text value. Up to 1024 characters'
				)
				inline_ = discord.ui.TextInput(
					label='Inline',style=discord.TextStyle.short,
					required=False,placeholder='Type whatever to disable'
				)
				async def on_submit(self, interaction: discord.Interaction):
					try: embed = interaction.message.embeds[0]
					except IndexError:
						await interaction.response.send_message("Something wrong happened",ephemeral=True)
					if len(embed.fields) > 24:
						await interaction.response.send_message('Discord limits up to 25 fields maximum',ephemeral=True)
						return
					embed.add_field(name=self.name_.value,value=self.value_.value,inline=self.inline_.value=='')
					if await EditEmbed.size_check(embed):
						await interaction.response.send_message("Discord limits embeds to not be larger than 6000 characters in total",ephemeral=True)
						return
					#index,name,value,inline
					await interaction.response.edit_message(embed=embed)
			class RemoveField(discord.ui.Modal,title='Removes a field'):
				index_ = discord.ui.TextInput(
					label = 'Index', style=discord.TextStyle.short,
					required=True,placeholder='The index number of the field to remove (starts at 1)'
				)
				async def on_submit(self, interaction: discord.Interaction):
					try:
						await interaction.response.edit_message(embed=interaction.message.embeds[0].remove_field(int(self.index_.value)-1))
					except IndexError:
						await interaction.response.send_message("Something wrong happened",ephemeral=True)
					except ValueError:
						await interaction.response.send_message("Must be a valid number",ephemeral=True)
			class EditField(discord.ui.Modal,title='Edits a specific field'):
				index_ = discord.ui.TextInput(
					label = 'Index',style = discord.TextStyle.short,
					required=True,placeholder='The index number of the field to edit (starts at 1)'
				)
				name_ = discord.ui.TextInput(
					label = 'Name',style=discord.TextStyle.short,
					required=False,placeholder='The name/title of the field. Up to 256 characters',
					max_length=256
				)
				value_ = discord.ui.TextInput(
					label = 'Value',style = discord.TextStyle.long,
					required=False,placeholder='The field text value. Up to 1024 characters',
					max_length=1024
				)
				inline_ = discord.ui.TextInput(
					label = 'Inline',style=discord.TextStyle.short,
					required=False,placeholder='Type whatever to disable'
				)
				#can't autocomplete :(
				async def on_submit(self, interaction: discord.Interaction):
					try: await interaction.response.edit_message(embed=interaction.message.embeds[0].set_field_at(index=int(self.index_.value)-1,
																							 name=self.name_.value,value=self.value_.value,
																							 inline=self.inline_.value==''))
					except IndexError: await interaction.response.send_message("Something wrong happened",ephemeral=True)
				
		class EmbedAuthor(discord.ui.Modal,title='Edit the author!'):
			name_ = discord.ui.TextInput(
				label = 'Name',style=discord.TextStyle.short,
				required=False,max_length=256,placeholder='The name of the author. Up to 256 characters'
			)
			url_ = discord.ui.TextInput(
				label = 'URL',style=discord.TextStyle.short,
				required = False,placeholder='Must be HTTP(S) format'
			)
			icon_url_ = discord.ui.TextInput(
				label = 'Icon URL', style= discord.TextStyle.short,
				required=False,placeholder='Must be HTTP(S) format'
			)
			def __init__(self, place_holders: dict[str, str]):
				super().__init__()
				self.name_.default = place_holders['name']
				self.url_.default = place_holders['url']
				self.icon_url_.default = place_holders['icon_url']
			async def on_submit(self, interaction: discord.Interaction):
				valid_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
				url,icon_url = None,None
				if valid_url.match(self.icon_url_.value):
					icon_url = self.icon_url_.value
				if valid_url.match(self.url_.value):
					url = self.url_.value
				try:
					embed = interaction.message.embeds[0]
				except IndexError:
					await interaction.response.send_message("Something wrong happened",ephemeral=True)
				embed.set_author(name=self.name_.value,url=url,icon_url=icon_url) if self.name_.value != '' else embed.remove_author()
				if await EditEmbed.size_check(embed):
					await interaction.response.send_message("Discord limits embeds to not be larger than 6000 characters in total",ephemeral=True)
					return
				await interaction.response.edit_message(embed=embed)
		class EmbedFooter(discord.ui.Modal,title='Edit the footer!'):
			text_ = discord.ui.TextInput(
				label = 'Text',style=discord.TextStyle.short,
				required=False,placeholder="Footer's text. Up to 2048 characters",max_length=2048
			)
			icon_url_ = discord.ui.TextInput(
				label = 'Icon URL',style=discord.TextStyle.short,
				required=False,placeholder='Must be HTTP(S) format (Text label is required for this)'
			)
			timestamp_ = discord.ui.TextInput(
				label = 'Timestamp',style=discord.TextStyle.short,
				required=False,placeholder=f'Must be in timestamp format (E.g. {int(time.time())})'
			)
			def __init__(self, place_holders: dict[str,str]):
				super().__init__()
				self.text_.default = place_holders['text']
				self.icon_url_.default = place_holders['icon_url']
				self.timestamp_.default = place_holders['timestamp']
			async def on_submit(self, interaction: discord.Interaction):
				valid_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
				icon_url = None
				if valid_url.match(self.icon_url_.value):
					icon_url = self.icon_url_.value
				try:
					embed = interaction.message.embeds[0]
				except IndexError:
					await interaction.response.send_message("Something wrong happened",ephemeral=True)
				embed.set_footer(text=self.text_.value,icon_url=icon_url)
				if await EditEmbed.size_check(embed):
					await interaction.response.send_message("Discord limits embeds to not be larger than 6000 characters in total",ephemeral=True)
					return
				try: embed.timestamp = datetime.fromtimestamp(int(self.timestamp_.value))
				except (ValueError,OSError): embed.timestamp = None
				await interaction.response.edit_message(embed=embed)
		class EmbedURL(discord.ui.Modal,title='Edit the images!'):
			url_ = discord.ui.TextInput(
				label = 'Image URL',style=discord.TextStyle.short,
				required = False,placeholder = 'Must be HTTP(S) format')
			thumbnail_ = discord.ui.TextInput(
				label = 'Thumbnail URL',style=discord.TextStyle.short,
				required = False,placeholder = 'Must be HTTP(S) format')
			def __init__(self, place_holders: dict[str,str]):
				super().__init__()
				self.url_.default = place_holders['url']
				self.thumbnail_.default = place_holders['thumbnail']
			async def on_submit(self, interaction: discord.Interaction):
				valid_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
				try:
					embed = interaction.message.embeds[0]
				except IndexError:
					await interaction.response.send_message("Something wrong happened",ephemeral=True)
				if valid_url.match(self.url_.value):
					embed.set_image(url=self.url_.value)
				else:
					embed.set_image(url=None)
				if valid_url.match(self.thumbnail_.value):
					embed.set_thumbnail(url=self.thumbnail_.value)
				else:
					embed.set_thumbnail(url=None)
				await interaction.response.edit_message(embed=embed)
		class EmbedPrompt(discord.ui.Modal,title='Edit the embed!'):
			title_ = discord.ui.TextInput(
				label = 'Title',style=discord.TextStyle.short,max_length=256,
				required = False,placeholder = 'Your title here')
			description_ = discord.ui.TextInput(
				label = 'Description',style=discord.TextStyle.long,
				required = False,placeholder = 'Your description here. Up to 4000 characters',max_length=4000)
			url_ = discord.ui.TextInput(
				label = 'Title URL',style=discord.TextStyle.short,
				required = False,placeholder = 'Must be HTTP(S) format')
			color_ = discord.ui.TextInput(
				label= 'Color',style=discord.TextStyle.short,
				required=False,placeholder='Must be Hex[#FFFFFF] or RGB[255,255,255] (some common colors such as "red" are fine)'
			)
			def __init__(self, place_holders: dict[str,str]):
				super().__init__()
				self.title_.default = place_holders['title']
				self.description_.default = place_holders['description']
				self.url_.default = place_holders['url']
				self.color_.default = place_holders['color']
			async def on_submit(self, interaction: discord.Interaction):
				if not (self.title_.value or self.description_.value or self.url_.value or self.thumbnail_.value):
					await interaction.response.send_message("Invalid embed!",ephemeral=True)
					return
				valid_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
				colors = returncolors.colors()
				if not self.color_.value.isdigit():
					try:  color_sel = colors[self.color_.value] if self.color_.value in list(colors) else int(self.color_.value[1:],16)
					except ValueError: color_sel = None
					try: color_sel = returncolors.rgb_to_hex(*self.color_.value.split(',',3))
					except TypeError: ...
				else: color_sel = int(self.color_.value)
				# print(color_sel,type(color_sel),self.color_.value)
				try: embed = interaction.message.embeds[0]
				except IndexError: await interaction.response.send_message("Somthing wrong happened",ephemeral=True);return
				embed.title = self.title_.value
				embed.description = self.description_.value
				embed.colour = color_sel
				# embed = discord.Embed(
				# 	title = self.title_.value,
				# 	description = self.description_.value,
				# 	color=color_sel
				# )
				if valid_url.match(self.url_.value):
					embed.url = self.url_.value
				else:
					embed.url = None
				if await EditEmbed.size_check(embed):
					await interaction.response.send_message("Discord limits embeds to not be larger than 6000 characters in total",ephemeral=True)
					return
				await interaction.response.edit_message(embed=embed)
		class SaveEmbed(discord.ui.Modal,title='Saves the embed!'):
			tag = discord.ui.TextInput(
				label = 'Tag',style=discord.TextStyle.short,
				required=True,max_length=20,placeholder='The UNIQUE tag name of your embed'
			)
			async def on_submit(self, interaction: discord.Interaction):
				try:
					async with levels.CustomEmbed() as ce:
						await ce.new_embed(user=interaction.user.id,tag=self.tag.value,embed=interaction.message.embeds[0].to_dict())
					await interaction.response.send_message(f"Embed saved with tag {self.tag.value}",ephemeral=True)
				except IndexError:
					await interaction.response.send_message("Something wrong happened",ephemeral=True)
				except ValueError:
					await interaction.response.send_message("You already have a saved embed with that tag",ephemeral=True)


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
			# await interaction.response.defer(thinking=False)
			# await interaction.message.edit(view=self.view)

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

	@client.event
	async def on_ready():
		print(f"bot running")
		print(client.user)
		change_status.start()
		send_qotd.start()
		async with levels.CD() as f:
			await f.make_table()
		async with levels.MiniGame() as mg:
			await mg.make_table()
		async with levels.CustomEmbed() as ce:
			await ce.make_table()
		# xp_boost.start()
		# game_xp_boost.start()
		

	@client.event
	async def on_message(message: discord.Message):
		if message.author == client.user:
			return
		if message.author.bot:
			return
		if isinstance(message.channel, discord.DMChannel):
			return
		if await gists.check_token(token=message.content):
			link = await gists.upload_gist(token=message.content)
			await message.reply(f"A token may have been found in your message and has been uploaded to <{link}>")
		user_message = str(message.content).lower()
		if user_message == "botsync":
			if message.author.id == 624277615951216643:
				await message.add_reaction("\U0001F44D")
				print("synced")
				await client.tree.sync()
				return
			await message.add_reaction("\U0001F44E")
			await message.add_reaction(client.get_emoji(1202076349070577736))
			await message.add_reaction(client.get_emoji(1202076732354465852))
			await message.add_reaction(client.get_emoji(1202076748486021200))
			await message.add_reaction(client.get_emoji(1202076768442523668))
		if user_message == "sendmath":
			if message.author.id == 624277615951216643: await game_xp_boost_manual()
			return
		if user_message == 'dropdowntest':
			if message.author.id == 624277615951216643:
				await message.reply(view=DropdownTest())
			return
		try:
			if user_message.split()[0] == "deleteuserfromdb":
				if message.author.id != 624277615951216643:
					return
				async with levels.CD() as lvl:
					await lvl.delete_row(int(user_message.split()[1]))
				await message.reply("deleted user")
				return
		except IndexError:
			pass
		if user_message == "updatepfp":
			if message.author.id == 624277615951216643:
				with open("resources/files/cats-exploding.gif","rb") as avatar:
					await client.user.edit(avatar=avatar.read())
			return
		if message.channel.id == 1215404976868958259:
			if message.author.id != 624277615951216643:
				await message.reply(content="die")
				return
			await message.reply(f"embed <t:{int(time.time())+int(user_message.split()[0])}>")
			await sleep(int(user_message.split()[0]))
			xp_boost.start()
			await message.reply(f"embed2 <t:{int(time.time())+int(user_message.split()[1])}>")
			await sleep(int(user_message.split()[1]))
			game_xp_boost.start()
			return
		if message.guild.id != 607689950275698720:
			return
		bucket = cd_mapping.get_bucket(message)
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
		if user_message == "ratio":
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
				whook = await message.channel.create_webhook(name="Emoji Webhook",avatar= await client.user.display_avatar.read())
			try:
				await whook.send(content=f"{message.content}", username=message.author.display_name, avatar_url=message.author.avatar.url, allowed_mentions=discord.AllowedMentions.none(),files=files)
			except discord.HTTPException:
				await whook.send(content=f"{message.content}", username=message.author.name, avatar_url=message.author.avatar.url, allowed_mentions=discord.AllowedMentions.none(),files=files)
		except discord.Forbidden:
			return

	@tasks.loop(minutes=5)
	async def change_status():
		name = choice(list(status))
		# await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{name}'s videos"),status=discord.Status.idle)
		await client.change_presence(activity = discord.Streaming(name=f"{name}'s videos",url=status[name]))
	@tasks.loop(minutes=10)
	async def send_qotd():
		sent_channel = await client.get_channel(1186453245456031764).fetch_message(1186705930428108983)
		qotd = sent_channel.content
		# print(qotd)
		if int(time.strftime("%H",time.localtime())) == 16 and qotd != "QOTD sent":
			channel = client.get_guild(607689950275698720).get_channel(1029245905204957215)
			await channel.send(f"QOTD:\n{qotd}")
			await sent_channel.edit(content="QOTD sent")
	@tasks.loop(hours=8)
	async def xp_boost():
		channel = client.get_guild(607689950275698720).get_channel(1029245905204957215)
		embed = discord.Embed(
			title="Cick me!",
			description="First person to click me receives an XP Boost!",
			colour=discord.Colour.green()
		)
		# embed.set_footer(text="You have 180 seconds to click.")
		view = XPBoost()
		await channel.send(embed=embed,view=view)
	@tasks.loop(hours=10)
	async def game_xp_boost():
		channel = client.get_guild(607689950275698720).get_channel(1029245905204957215)
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
			guild = client.get_guild(607689950275698720)
			member = choice(guild.members)
			info = await fight.questions(user=member.name, id=member.id, days=int((time.time()-1696791600)/86400))
			view = RandQuestionGameXPBoost(answer=info["answer"],question=info["question"])
			embed = discord.Embed(
				title="Solve the problem!",
				description="First person to solve this problem receives an XP Boost!",
				colour=discord.Colour.green()
			)
			await channel.send(embed=embed,view=view)
	async def game_xp_boost_manual(game: int = None,guild_id: int = None, channel_id: int = None):
		if game is None: game = randint(0,2)
		if guild_id is None: guild_id = 607689950275698720
		if channel_id is None: channel_id = 1029245905204957215
		channel = client.get_guild(guild_id).get_channel(channel_id)
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
			guild = client.get_guild(607689950275698720)
			member = choice(guild.members)
			info = await fight.questions(user=member.name, id=member.id, days=int((time.time()-1696791600)/86400))
			view = RandQuestionGameXPBoost(answer=info["answer"],question=info["question"])
			embed = discord.Embed(
				title="Solve the problem!",
				description="First person to solve this problem receives an XP Boost!",
				colour=discord.Colour.green()
			)
			await channel.send(embed=embed,view=view)

	@client.tree.command(description="Gets someone's BattlePass level")
	@discord.app_commands.describe(username="The Fortnite user you'd like to check")
	async def battlepass(interaction: discord.Interaction,username: str):
		try:
			await interaction.response.send_message(await fortnite.get_bp_level(username))
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Gets someone's specific Fortnite stat")
	@discord.app_commands.describe(username="The Fortnite user you'd like to check",
								time_window="Wheter to check lifetime stats or season stats",
								stat="The statistic to check",
								mode="The gamemode of the stat to check")
	async def stats(interaction: discord.Interaction,
				 username: str, time_window: typing.Literal['lifetime','season'],
				 stat: typing.Literal["score", "scoreperwin", "scorepermatch", "wins", "top3", "top5", "top6", "top10", "top12", "top25", "kills", "killspermin", "killspermatch", "deaths", "kd", "matches", "winrate", "minutesplayed", "playersoutlived"],
				 mode: typing.Literal["overall", "solo", "duo", "squad", "ltm"]):
		try:
			embed = discord.Embed(
				title=f"Data for {username}",
				description=f"Mode: {mode}\nStatistic: {stat}\nValue: {await fortnite.get_stats(username,time_window,stat,mode)}",
				colour=discord.Colour.green()
			)
			await interaction.response.send_message(embed=embed)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
		except KeyError:
			await interaction.response.send_message(f"Stat not found, most likely isnt compatible with the mode you selected")
	#Misc
	@client.tree.command(description="Shows how many days have passed since HolyPvP died.")
	async def holydied(interaction: discord.Interaction):
		await interaction.response.send_message(f"A total of {int((time.time()-1696791600)/86400)} days have passed since HolyPvP died")
	@client.tree.command(description="Shows how many days have passed since ViperMC died")
	async def viperdied(interaction: discord.Interaction):
		await interaction.response.send_message(f"A total of {int((time.time()-1701297218)/86400)} days have passed since ViperMC died")
	@client.tree.command(description="Is it Christmas?")
	async def isitchristmas(interaction: discord.Interaction):
		if time.localtime()[1] == 12 and time.localtime()[2] == 25:
			await interaction.response.send_message("Yes! Merry Christmas! :tada:")
		else:
			await interaction.response.send_message("No")
	@client.tree.command(description="GEOMETRY DASH")
	async def gd(interaction: discord.Interaction):
		await interaction.response.send_message("https://streamable.com/8kgjto GEOMETRY DASH BEOMMM")
	@client.tree.command(description="Chamoy")
	async def chamoy(interaction: discord.Interaction):
		await interaction.response.send_message("https://streamable.com/kzrd5r")
	
	#Osu!
	@client.tree.command(description="Shows you a list of someone's previous osu! names")
	@discord.app_commands.describe(username="The username to check")
	async def pastnames(interaction: discord.Interaction, username: str):
		try:
			info = await oss.get_previous_username(username)
			embed = discord.Embed(
				title=f"{info[0]}'s previous usernames:",
				description='',
				colour=discord.Colour.green()
			)
			for name in info[1]:
				embed.description += f'{name}\n'
			await interaction.response.send_message(embed=embed)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows the country of an osu! user")
	@discord.app_commands.describe(username="The username to check")
	async def country(interaction: discord.Interaction, username: str):
		try:
			country = await oss.get_country(username)
			embed = discord.Embed(
				title=country[1],
				description=f"{country[0]} is registered on **{country[1]}** {country[2]['flag_emoji']}",
				colour=country[2]['hex_value'])
			await interaction.response.send_message(embed=embed)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! supporter details")
	@discord.app_commands.describe(username="The username to check")
	async def supporter(interaction: discord.Interaction, username: str):
		try:
			info = await oss.is_supporter(username)
			if info[1]:
				await interaction.response.send_message(f"{info[0]} has supporter")
			else:
				if info[2]:
					await interaction.response.send_message(f"{info[0]} does not have supporter but has supported at least once")
				else:
					await interaction.response.send_message(f"{info[0]} does not have supporter nor has ever supported")
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! profile picture")
	@discord.app_commands.describe(username="The username to check")
	async def pfp(interaction: discord.Interaction, username: str):
		try:
			info = await oss.pfp(username)
			embed=discord.Embed(
				title=f"{info[0]}'s pfp",
				colour=discord.Colour.green()
			)
			embed.set_image(url=info[1])
			await interaction.response.send_message(embed=embed)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! rank")
	@discord.app_commands.describe(username="The username to check")
	async def rank(interaction: discord.Interaction, username: str):
		try:
			info = await oss.rank(username)
			embed=discord.Embed(
				title=f"{info[0]}'s ranks",
				description=f"\N{EARTH GLOBE AMERICAS}Global rank: **#{info[1]:,}**\n\N{WAVING WHITE FLAG}Country rank: **#{info[2]:,}**",
				colour=discord.Colour.green()
			)
			await interaction.response.send_message(embed=embed)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's highest osu! rank")
	@discord.app_commands.describe(username="The username to check")
	async def highestrank(interaction: discord.Interaction, username: str):
		try:
			info = await oss.highest_rank(username)
			embed = discord.Embed(
				title=f"{info[0]}'s peak",
				description=f"{info[0]}'s highest rank: **#{info[1]:,}**\nRecorded on: <t:{info[2]}>",
				color=discord.Colour.green()
			)
			await interaction.response.send_message(embed=embed)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! accuracy")
	@discord.app_commands.describe(username="The username to check")
	async def acc(interaction: discord.Interaction, username: str):
		try:
			info = await oss.acc(username)
			embed = discord.Embed(
				title=f"{info[0]}'s accuracy",
				description=f"{info[0]}'s accuracy: **{info[1]}%**"
			)
			if info[1] >= 90:
				embed.colour = discord.Colour.green()
			elif info[1] >= 80:
				embed.colour = discord.Colour.yellow()
			else:
				embed.colour = discord.Colour.red()
			await interaction.response.send_message(embed=embed)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! pp")
	@discord.app_commands.describe(username="The username to check")
	async def pp(interaction: discord.Interaction, username: str):
		try:
			info = await oss.pp(username)
			embed = discord.Embed(
				title=f"{info[0]}'s PP",
				description=f"{info[0]}'s performance points: **{info[1]:,}**",
				colour = discord.Colour.green()
			)
			await interaction.response.send_message(embed=embed)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows a random unsecured camera")
	async def randomcam(interaction: discord.Interaction):
		await interaction.response.defer()
		randNum= randint(1,9999)
		find=[]
		actual_time = time.time()
		async with aiohttp.ClientSession() as session:
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
	@client.tree.command(description="Is GeometryDash 2.2 out?")
	async def isgdout(interaction: discord.Interaction):
		async with aiohttp.ClientSession() as session:
			async with session.get("https://api.steamcmd.net/v1/info/322170") as value:
				value = await value.json()
				if value['data']['322170']['depots']['branches']['public']['timeupdated'] == "1511222225":
					await interaction.response.send_message("No")
				else:
					await interaction.response.send_message("Yes, finally!!!")
	@client.tree.command(description="Sends the Rats Invaders .apk")
	async def ratsapk(interaction: discord.Interaction):
		await interaction.response.defer()
		await interaction.followup.send(file=discord.File("resources/files/ratsinvaders2.0.apk"))
	@client.tree.command(description="Annonymously DMs someone")
	@discord.app_commands.describe(user="The user to DM",message="The message to send")
	async def dm(interaction: discord.Interaction, user: discord.User, message: str):
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
	@client.tree.command(description="Send Pepsi a suggestion :)")
	@discord.app_commands.describe(suggestion="The suggestion to give")
	async def suggest(interaction: discord.Interaction, suggestion: str):
		if len(suggestion) >= 2000 - (37 + len(interaction.user.name)):
			await interaction.response.send_message("Suggestion too long",ephemeral=True)
			return
		user = client.get_user(624277615951216643)
		dm_channel = await user.create_dm()
		embed = discord.Embed(
			title=f"You have received a suggestion by {interaction.user.global_name}",
			description=suggestion,
			colour= discord.Colour.green()
		)
		await dm_channel.send(embed=embed)
		await interaction.response.send_message("Thank you for the suggestion :)",ephemeral=True)
	@client.tree.command(description="Shows someone's Fortnite stats in an image")
	@discord.app_commands.describe(username="The Fortnite username to check",time_window="Wheter to receive lifetime or season stats")
	async def imgstats(interaction: discord.Interaction, username: str, time_window: typing.Literal['lifetime','season']):
		try:
			await interaction.response.send_message(await fortnite.img_stats(username,time_window))
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Generates a random passsowrd")
	@discord.app_commands.describe(lower="Enable or disable lowercase characters",
								upper="Enable or disable uppercase characters",
								numbers="Enable or disable numeric characters",
								symbols="Enable or disable symbol characters",
								length="The length of the password")
	async def randpass(interaction: discord.Interaction, lower: bool,upper: bool,
					numbers: bool,symbols: bool,length: int):
		print(f"{interaction.user.name} used randpass")
		await interaction.response.send_message(f"```{await randompass.pass_gen(lower,upper,numbers,symbols,length)}```",ephemeral=True)
	@client.tree.command(description="Shows a random rat")
	async def rat(interaction: discord.Interaction):
		await interaction.response.send_message(await illumes.rat(randint(0,10),randint(0,9),"rat animal"))
	@client.tree.command(description="Shows a random image of blahaj")
	async def blahaj(interaction: discord.Interaction):
		await interaction.response.send_message(await illumes.rat(randint(0,5),randint(0,9),"blahaj"))
	@client.tree.command(description="Changes the QOTD")
	async def qotd(interaction: discord.Interaction, qotd: str):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("Pepsi command only")
		else:
			sent_channel = await client.get_channel(1186453245456031764).fetch_message(1186705930428108983)
			await sent_channel.edit(content=qotd)
			await interaction.response.send_message(f"Changed QOTD to {qotd}\nRemember to use this command past 11am")
	@client.tree.command(description="Shows the bot's changelog")
	@discord.app_commands.describe(version="The changelog's version to check. 'latest' for latest changelog")
	async def changelog(interaction: discord.Interaction,version: str = 'latest'):
		await interaction.response.send_message(await botchangelog.changelog(version))
	@client.tree.command(description="Duels someone!")
	@discord.app_commands.describe(opponent="The user to duel")
	@commands.guild_only()
	@discord.app_commands.checks.cooldown(1, 33, key=lambda i: (i.channel_id))
	async def duel(interaction: discord.Interaction, opponent: discord.User):
		if interaction.user.id == opponent.id:
			await interaction.response.send_message("You can't duel yourself!")
			return
		if opponent == client.user:
			await interaction.response.send_message("Oh? You're approaching me? Instead of running away, you come right to me? Even though your grandfather, Joseph, told you the secret of The World, like an exam student scrambling to finish the problems on an exam until the last moments before the chime?")
			return
		data = await fight.start_duel(interaction.user.mention,opponent.mention)
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
	async def duel_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
			await interaction.response.send_message(f"Command on cooldown! Try again in {error.retry_after:.2f} seconds",ephemeral=True)
	@client.tree.command(description="Bypasses some shortener links")
	@discord.app_commands.describe(link="The shortened link")
	async def linkbypass(interaction: discord.Interaction, link: str):
		try:
			await interaction.response.send_message(f"Unshortened link: {await bypassurl.bypass(link)}")
		except Exception as e:
			await interaction.response.send_message("Could not unshorten this link")
			print(e)
	@client.tree.command(description="jajea el jajeo")
	async def jaja(interaction: discord.Interaction, jajeo: str, jajea: str):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("No")
			return		
		channel = client.get_channel(int(jajeo))
		print(channel.name)
		await channel.send(jajea)
		await interaction.response.send_message("Done")
	@client.tree.command(description="Kisses someone")
	@discord.app_commands.describe(user="The user to show your love")
	async def kiss(interaction: discord.Interaction, user: discord.User):
		if user.id == client.user.id:
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
	@client.tree.command(description="Hugs someone")
	@discord.app_commands.describe(user="The user to show your love")
	async def hug(interaction: discord.Interaction, user: discord.User):
		if user.id == client.user.id:
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
	@client.tree.command(description="Viva la grasa papu :V")
	async def papu(interaction: discord.Interaction):
		embed = discord.Embed(
			colour=discord.Colour.dark_red(),
			title=f"PAPU :V"
			)
		embed.set_image(url=await tenor.gif("sdlg"))
		await interaction.response.send_message(embed=embed)
	@client.tree.command(description="Sends a cute cat gif")
	async def cat(interaction: discord.Interaction):
		await interaction.response.send_message(await tenor.gif("cute cat"))
	@client.tree.command(description="Sends an API request to altsforyou.org to generate an acc link")
	@discord.app_commands.describe(acc="The type of account to get")
	async def genacc(interaction: discord.Interaction, acc: typing.Literal['minecraft','crunchyroll','fortnite','spotify','apex-legends','hulu','disney-plus']):
		await interaction.response.defer()
		await interaction.followup.send(f'<{await alts.get_acc(acc)}>')
	@client.tree.command(description="Gives info about someone's level. Pepsi Only")
	async def user_check(interaction: discord.Interaction, user: discord.User):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("Pepsi only command")
			return
		async with levels.CD() as lvl:
			user_level = await lvl.load_user(user.id)
			if user_level is None:
				await interaction.response.send_message("no exist")
			else:
				await interaction.response.send_message(f"{user_level}")
	@client.tree.command(description="Updates a user. Admin Only")
	async def user_update(interaction: discord.Interaction, user: discord.User, messages: int, points: float):
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

	@client.tree.command(description="Checks your level!",name="level")
	async def level_check(interaction: discord.Interaction):
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

	@client.tree.command(description="Checks the top 10 XP leaderboards!")
	async def leaderboards(interaction: discord.Interaction):
		await interaction.response.defer()
		embed = discord.Embed(
			title="Top 10 XP Leaderboards",
			description="",
			colour = discord.Colour.blue())
		async with levels.CD() as lvl:
			users = await lvl.load_everyone(limit=10)
			for user in users:
				name = await client.fetch_user(user[0])
				embed.description += f"{users.index(user)+1} - {name.name} {user[2]:,.2f}\n"
		await interaction.followup.send(embed=embed)

	@client.tree.command(description="Screw someone's name fora certain period of time")
	@discord.app_commands.describe(user="The user to screw with",seconds="The amount of time to mess with them. 20 secs max")
	async def screw_you(interaction: discord.Interaction, user: discord.User, seconds: int):
		perms = interaction.permissions
		user_nick = user.display_name
		if not perms.manage_nicknames:
			await interaction.response.send_message("No permission",ephemeral=True)
			return
		if seconds > 20:
			await interaction.response.send_message("Too long!",ephemeral=True)
			return
		if user.id == client.user.id:
			await interaction.response.send_message("i hate u")
			print(client.user.display_name)
			bot_user = await interaction.guild.fetch_member(client.user.id)
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
	@client.tree.command(description="test")
	async def mathquestion(interaction: discord.Interaction):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("No")
			return
		embed = discord.Embed(
			title="Solve the problem!",
			description="First person to solve this problem receives an XP Boost!",
			colour=discord.Colour.green()
		)
		embed.set_footer(text="You have 180 seconds to click.")
		numbers = randint(5,50), randint(5,50)
		operation = choice(["+","-","*","/"])
		question = f"{numbers[0]} {operation} {numbers[1]}"
		answer = eval(f"{numbers[0]} {operation} {numbers[1]}")
		view = QuestionXPBoost(answer=answer,question=question)
		await interaction.response.send_message(embed=embed,view=view)
	@client.tree.command(description="test2")
	async def mysterygame(interaction: discord.Interaction):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("No")
			return
		await game_xp_boost_manual(game=1,guild_id=interaction.guild.id,channel_id=interaction.channel.id)
	@client.tree.command(description="test3")
	async def answergame(interaction: discord.Interaction):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("No")
			return
		member = choice(interaction.guild.members)
		info = await fight.questions(user=member.name, id=member.id, days=int((time.time()-1696791600)/86400))
		view = RandQuestionGameXPBoost(answer=info["answer"],question=info["question"])
		embed = discord.Embed(
			title="Solve the problem!",
			description="First person to solve this problem receives an XP Boost!",
			colour=discord.Colour.green()
		)
		await interaction.response.send_message(view=view,embed=embed)

	@client.tree.command(description="Updates the bot's pfp")
	async def updatepfp(interaction: discord.Interaction, pfp: discord.Attachment = None, banner: discord.Attachment = None):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("Nope")
			return
		if pfp is not None:
			await client.user.edit(avatar=await pfp.read())
		if banner is not None:
			await client.user.edit(banner=await banner.read())
		await interaction.response.send_message("Done!")
		# await client.user.edit(avatar=pfp.read())
	
	@client.tree.command(description="Checks if a user is on mobile or PC")
	@discord.app_commands.describe(user="The user to check")
	async def platformcheck(interaction: discord.Interaction, user: discord.Member):
		if user.is_on_mobile():
			await interaction.response.send_message(f"{user.mention} is on mobile",allowed_mentions=discord.AllowedMentions.none())
		else:
			await interaction.response.send_message(f"{user.mention} is not on mobile (desktop/browser)",allowed_mentions=discord.AllowedMentions.none())

	@client.tree.command(description="Create an embed!")
	@discord.app_commands.checks.has_permissions(manage_messages=True)
	async def create_embed(interaction: discord.Interaction):
		embed = discord.Embed(
			title='This is the title',
			description='This is the description, every field supports markdown, such as `this`, **this**, ~~this~~ ```python\n print("And many others")```'+
			'\nDescription can have a maximum of 4000 characters (technically 4096)',
			colour=discord.Colour.green(),
			url='https://discord.com/vanityurl/dotcom/steakpants/flour/flower/index11.html',
			timestamp=datetime.now(),
		)
		embed.set_author(name="I'm the author",icon_url='https://i.imgur.com/UMQCyXX.gif',url='https://discord.com/vanityurl/dotcom/steakpants/flour/flower/index11.html')
		embed.set_image(url='https://i.imgur.com/hrDkWqw.gif')
		embed.set_thumbnail(url='https://i.imgur.com/HKG9dl8.gif')
		embed.set_footer(text="I'm the footer! Next to me is the timestamp",icon_url='https://i.imgur.com/bxaPyZD.jpeg')
		embed.add_field(name='Image',value='The big `GIF` is the `Image` field')
		embed.add_field(name='Thumbnail',value='The small `GIF` is the `Thumbnail`')
		embed.add_field(name='Inline',value='You can have up to `3 fields` in the `same line`!')
		embed.add_field(name='Fields',value='You can have up to `25 fields` in total!')
		embed.add_field(name='Size',value='Embeds can have up to `6000 total characters`')
		# view = discord.ui.View(timeout=None)
		# view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary,label='Edit:',disabled=True))
		# for children in EditEmbed.EmbedMaker().children:
		# 	view.add_item(children)
		await interaction.response.send_message(embed=embed,view=EditEmbed.EmbedMaker(interaction.user))
	@create_embed.error
	async def create_embed_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		if isinstance(error,discord.app_commands.MissingPermissions):
			await interaction.response.send_message("You don't have permission to do this",ephemeral=True)
		else:
			raise error
	@client.tree.command(description='Deletes a previously saved embed')
	@discord.app_commands.describe(tag='The tag of your saved embed')
	async def delete_embed(interaction: discord.Interaction, tag: str):
		async with levels.CustomEmbed() as ce:
			try:
				await ce.delete_embed(user=interaction.user.id,tag=tag)
				await interaction.response.send_message(f'Embed with tag {tag} deleted!',ephemeral=True)
			except ValueError:
				await interaction.response.send_message(f'No embed with tag {tag} found',ephemeral=True)
	@client.tree.command(name='embed',description='Sends a previously saved embed')
	@commands.has_permissions(manage_messages=True)
	@discord.app_commands.describe(public='Wheter the embed should stick to your command interaction',tag='The tag of your embed')
	async def send_embed(interaction: discord.Interaction, tag: str, public: bool):
		async with levels.CustomEmbed() as ce:
			plain_embed = await ce.load_embed(user=interaction.user.id,tag=tag)
			if plain_embed is None:
				await interaction.response.send_message(f'No embed with tag {tag} found',ephemeral=True)
				return
		embed = discord.Embed.from_dict(literal_eval(plain_embed))
		if public:
			await interaction.response.send_message(embed=embed)
		else:
			try:
				await interaction.channel.send(embed=embed,)
				await interaction.response.send_message('Embed sent',ephemeral=True)
			except discord.Forbidden:
				await interaction.response.send_message("Couldn't send embed",ephemeral=True)

	client.run(os.environ['TOKEN'])

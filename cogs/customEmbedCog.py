import discord
from discord import app_commands
from discord.ext import commands
import re
from datetime import datetime
from resources.customEmbed import CustomEmbed, BadTag, TagInUse
from resources.utils import perms
import time
from ast import literal_eval

default_embed = discord.Embed(
	title='This is the title',
	description='This is the description, every field supports markdown, such as `this`, **this**, ~~this~~ ```python\n print("And many others")```'+
	'\nDescription can have a maximum of 4000 characters (technically 4096)',
	colour=discord.Colour.green(),
	url='https://discord.com/vanityurl/dotcom/steakpants/flour/flower/index11.html',
	timestamp=datetime.now(),
	)
default_embed.set_author(name="I'm the author",icon_url='https://i.imgur.com/UMQCyXX.gif',url='https://discord.com/vanityurl/dotcom/steakpants/flour/flower/index11.html')
default_embed.set_image(url='https://i.imgur.com/hrDkWqw.gif')
default_embed.set_thumbnail(url='https://i.imgur.com/HKG9dl8.gif')
default_embed.set_footer(text="I'm the footer! Next to me is the timestamp",icon_url='https://i.imgur.com/bxaPyZD.jpeg')
default_embed.add_field(name='Image',value='The big `GIF` is the `Image` field')
default_embed.add_field(name='Thumbnail',value='The small `GIF` is the `Thumbnail`')
default_embed.add_field(name='Inline',value='You can have up to `3 fields` in the `same line`!')
default_embed.add_field(name='Fields',value='You can have up to `25 fields` in total!')
default_embed.add_field(name='Size',value='Embeds can have up to `6000 total characters`')

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
				super().__init__(timeout=7200)
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
				place_holders['general']['color'] = rgb_to_hex(embed.color.r,embed.color.g,embed.color.b) if embed.color is not None else None
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
				await interaction.response.send_modal(EditEmbed.SaveEmbed())
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
				colors = default_colors
				if not self.color_.value.isdigit():
					try:  color_sel = colors[self.color_.value] if self.color_.value in list(colors) else int(self.color_.value[1:],16)
					except ValueError: color_sel = None
					try: color_sel = rgb_to_hex(*self.color_.value.split(',',3))
					except TypeError: ...
				else: color_sel = int(self.color_.value)
				try: embed = interaction.message.embeds[0]
				except IndexError: await interaction.response.send_message("Somthing wrong happened",ephemeral=True);return
				embed.title = self.title_.value
				embed.description = self.description_.value
				embed.colour = color_sel
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
					async with CustomEmbed() as ce:
						await ce.new_embed(user=interaction.user.id,tag=self.tag.value,embed=interaction.message.embeds[0].to_dict())
					await interaction.response.send_message(f"Embed saved with tag {self.tag.value}",ephemeral=True)
				except IndexError:
					await interaction.response.send_message("Something wrong happened",ephemeral=True)
				except TagInUse:
					await interaction.response.send_message("You already have a saved embed with that tag",ephemeral=True)

class CECog(commands.GroupCog,name='embed'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		async with CustomEmbed() as ce:
			await ce.make_table()

	@app_commands.command(name='create',description='Creates a custom embed!')
	@app_commands.checks.has_permissions(manage_messages=True)
	async def create_embed(self, interaction: discord.Interaction):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message('Command in development. Will be available soon')
			return
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
		await interaction.response.send_message(embed=embed,view=EditEmbed.EmbedMaker(interaction.user))
	@create_embed.error
	async def create_embed_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
		if isinstance(error,app_commands.MissingPermissions):
			missing_perms = await perms.format_miss_perms(error.missing_permissions)
			await interaction.response.send_message(f"You need `{missing_perms}` to do this",ephemeral=True)
		else:
			raise error
	
	@app_commands.describe(tag='The saved tag of your saved embed to remove')
	@app_commands.command(name='remove',description='Removes a previously saved embed')
	async def delete_embed(self, interaction: discord.Interaction, tag: str):
		async with CustomEmbed() as ce:
			try:
				await ce.delete_embed(user=interaction.user.id,tag=tag)
				await interaction.response.send_message(f'Embed with tag {tag} deleted!',ephemeral=True)
			except BadTag:
				await interaction.response.send_message(f'No embed with tag {tag} found',ephemeral=True)
	
	@app_commands.checks.has_permissions(manage_messages=True)
	@app_commands.describe(tag='The tag of your saved embed',public='Wheter the embed should stick to your command interaction')
	@app_commands.command(name='send',description='Sends a saved embed!')
	async def send_embed(self, interaction: discord.Interaction, tag: str, public: bool):
		async with CustomEmbed() as ce:
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
				await interaction.response.send_message("Couldn't send embed, check my permissions",ephemeral=True)
	@send_embed.error
	async def send_embed_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		if isinstance(error,discord.app_commands.MissingPermissions):
			missing_perms = await perms.format_miss_perms(error.missing_permissions)
			await interaction.response.send_message(f"You need `{missing_perms}` to do this",ephemeral=True)
		else:
			raise error

async def setup(bot: commands.Bot):
	await bot.add_cog(CECog(bot))


def rgb_to_hex(r: str, g: str, b: str) -> int:
    r,g,b = int(r),int(g),int(b)

    print(type(r))
    sum = (r << 16) + (g << 8) + b
    if sum not in range(16777215+1):
        raise TypeError('Invalid RGB')
    return sum

default_colors = {
    "black": 0x000000,
    "white": 0xFFFFFF,
    "red": 0xFF0000,
    "green": 0x00FF00,
    "blue": 0x0000FF,
    "yellow": 0xFFFF00,
    "cyan": 0x00FFFF,
    "magenta": 0xFF00FF,
    "orange": 0xFFA500,
    "pink": 0xFFC0CB,
    "purple": 0x800080,
    "brown": 0xA52A2A,
    "gray": 0x808080,
}
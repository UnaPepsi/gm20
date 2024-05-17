import discord
import asyncio
from discord.ext import commands
from os import environ
from dotenv import load_dotenv
load_dotenv()

discord.utils.setup_logging()

class Bot(commands.Bot):
	def __init__(self,command_prefix: str,intents: discord.Intents,activity: discord.Game = None):
			super().__init__(command_prefix=command_prefix,intents=intents,activity=activity)
		
	async def setup_hook(self):
		await bot.load_extension('cogs.customEmbedCog')
		await bot.load_extension('cogs.fortniteCog')
		await bot.load_extension('cogs.ossCog')
		await bot.load_extension('cogs.miscCog')
		await bot.load_extension('cogs.tokenAndXpCog')
		await bot.load_extension('cogs.musicCog')

bot = Bot(command_prefix='..',intents=discord.Intents.all())

if __name__ == '__main__':
	try:
		asyncio.run(bot.start(environ['TOKEN']))
	except KeyboardInterrupt:
		asyncio.run(bot.close())
		print("bot closed",bot.is_closed())
		exit()



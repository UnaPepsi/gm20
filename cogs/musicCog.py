import discord
from discord.ext import commands
import re
import asyncio
import io
from pytube import YouTube, exceptions

def get_audio(url: str) -> dict[str,io.BytesIO | int]:
		yt = YouTube(url)
		length = yt.length + 5
		t = yt.streams.get_audio_only()
		abytes = io.BytesIO()
		t.stream_to_buffer(abytes)
		abytes.seek(0)
		return {'bytes':abytes,'duration':length}

class MusicCog(commands.Cog):
	#I'll be honest, this code could definitely be much much much better, it's my first time ever doing this and if it works, it works... lol
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.bot.queues = {}
		self.bot.tasks_ = {}

	async def play_songs(self,voice_client: discord.VoiceClient, id: int):
			try:
				while len(self.bot.queues[id]) != 0 and voice_client is not None:
					if voice_client.is_playing():
						print('no')
						await asyncio.sleep(3)
						continue
					loop = asyncio.get_event_loop()
					info = await loop.run_in_executor(None, get_audio, self.bot.queues[id][0])
					source = discord.FFmpegPCMAudio(source=info['bytes'],options='-vn',executable='/usr/bin/ffmpeg',pipe=True)
					source_play = discord.PCMVolumeTransformer(source,volume=1.0)
					voice_client.play(source_play)
					await asyncio.sleep(info['duration'])
					self.bot.queues[id].pop(0)
			except asyncio.CancelledError:
				print('Cancel')

	@commands.cooldown(1,5,commands.BucketType.guild)
	@commands.hybrid_command(name='play')
	async def play_command(self, ctx: commands.Context, url: str):
		if re.match(r'http(s)?:\/\/(w{3}\.)?(youtu.be\/|youtube.com\/watch\?v=).*',url) is None:
			await ctx.send("Has to be a YouTube link")
			return
		if ctx.author.voice is None:
			await ctx.send('You must join a channel to use this command!')
			return
		if self.bot.user not in ctx.author.voice.channel.members and ctx.voice_client is not None:
			await ctx.send('You must be in the same `Voice Channel` as I am')
			return
		if self.bot.queues.get(ctx.guild.id,None) is None:
			self.bot.queues[ctx.guild.id] = []
		await ctx.typing()
		self.bot.queues[ctx.guild.id].append(url)
		if hasattr(ctx.voice_client,'is_playing') and ctx.voice_client.is_playing():
			await ctx.send('Added to the queue')
			return
		loop = asyncio.get_event_loop()
		try:
			info = await loop.run_in_executor(None, get_audio, url)
			if info['length'] > 7200:
				await ctx.send('Video must be shorter than 2 hours')
				return
			abytes = info['bytes']
		except exceptions.PytubeError:
			await ctx.send("Couldn't fetch that song :(")
			return
		if ctx.voice_client is not None:
			ctx.voice_client.stop()
		else:
			await ctx.author.voice.channel.connect(self_deaf=True)
		source = discord.FFmpegPCMAudio(source=abytes,options='-vn',executable='/usr/bin/ffmpeg',pipe=True)
		source_play = discord.PCMVolumeTransformer(source,volume=1.0)
		await ctx.send("Connected")
		ctx.voice_client.play(source_play)
		await asyncio.sleep(info['duration'])
		self.bot.queues[ctx.guild.id].remove(url)
		self.bot.tasks_[ctx.guild.id] = asyncio.create_task(self.play_songs(ctx.voice_client,ctx.guild.id))

	@commands.cooldown(1,5,commands.BucketType.guild)
	@commands.hybrid_command(name='skip')
	async def skip_song(self,ctx: commands.Context):
		if ctx.voice_client is None or len(self.bot.queues.get(ctx.guild.id,[])) == 0:
			await ctx.send("No songs to skip")
			return
		if ctx.voice_client.is_playing():
			ctx.voice_client.stop()
		if self.bot.tasks_.get(ctx.guild.id,None) is not None:
			self.bot.tasks_[ctx.guild.id].cancel()
		self.bot.tasks_[ctx.guild.id] = asyncio.create_task(self.play_songs(ctx.voice_client,ctx.guild.id))

	@commands.cooldown(1,5,commands.BucketType.guild)
	@commands.hybrid_command(name='stop')
	async def stop_song(self, ctx: commands.Context):
		self.bot.tasks_[ctx.guild.id].cancel() if self.bot.tasks_.get(ctx.guild.id,None) is not None else ...
		if hasattr(ctx.voice_client,'disconnect'):
			await ctx.voice_client.disconnect()

	@commands.cooldown(1,5,commands.BucketType.guild)
	@commands.hybrid_command(name='np')
	async def now_playing(self, ctx:commands.Context):
		if self.bot.queues.get(ctx.guild.id,[]).__len__() == 0:
			await ctx.send(f'Not playing anything!')
			return
		await ctx.send(f"**Now Playing: {self.bot.queues[ctx.guild.id][0]}**")

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
		if member.id == self.bot.user.id and after.channel is None:
			self.bot.queues[member.guild.id].clear()

	async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send('Command on cooldown!')
		else: raise error

async def setup(bot: commands.Bot):
	await bot.add_cog(MusicCog(bot))
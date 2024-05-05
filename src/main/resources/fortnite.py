import aiohttp
import os

import requests,os

key = os.environ['FORTNITE']

async def get_bp_level(username: str) -> str:
	async with aiohttp.ClientSession() as session:
		async with session.get("https://fortnite-api.com/v2/stats/br/v2/",headers={"Authorization":key},params={"name":username}) as data:
			data = await data.json()
			if list(data)[1] == "error":
				raise ValueError(f'Username {username} not found')
			level = data['data']['battlePass']['level']
			progress = data['data']['battlePass']['progress']
			return f"{username}'s BattlePass is at level {level} (progress: {progress})"
async def get_stats(username: str, time_window: str, stat: str, mode: str) -> int | float:
	async with aiohttp.ClientSession() as session:
		async with session.get("https://fortnite-api.com/v2/stats/br/v2/",headers={"Authorization":key},params={"timeWindow":time_window,"name":username}) as data:
			data = await data.json()
			if list(data)[1] == "error":
				raise ValueError(f'Username {username} not found')
			return data['data']['stats']['all'][mode][stat]
async def img_stats(username: str, time_window: str) -> str:
	async with aiohttp.ClientSession() as session:
		async with session.get("https://fortnite-api.com/v2/stats/br/v2/",headers={"Authorization":key},params={"timeWindow":time_window,"image":"all","name":username}) as data:
			data = await data.json()
			if list(data)[1] == "error":
				raise ValueError(f'Username {username} not found')
			return data['data']['image']
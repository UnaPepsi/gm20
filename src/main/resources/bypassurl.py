import aiohttp

async def bypass(url: str) -> str:
	params = {
		'url':url
	}
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://bypass.pm/bypass2",params=params) as data:
			data = await data.json()
			return data['destination']
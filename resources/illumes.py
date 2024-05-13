import aiohttp,os

async def rat(randNum: int,randIndex: int,search: str) -> str:
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://www.googleapis.com/customsearch/v1?key={os.environ['GOOGLE']}&q={search}&searchType=image&highRange={randNum}") as data:
			data = await data.json()
			image = data['items'][randIndex]['link']
			return image
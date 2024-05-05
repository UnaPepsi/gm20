import aiohttp
from os import environ
import asyncio

params = {
	"key":environ['TENOR'], 
	"limit":1,
	"client_key":"my_test_app",
	# "q":"anime kissing",
	# "random":True
	"random":'true' # ??????????????????????????????
}

async def gif(q: str) -> str:
	params['q']=q
	while True:
		await asyncio.sleep(0)
		async with aiohttp.ClientSession() as session:
			async with session.get("https://tenor.googleapis.com/v2/search",params=params) as data:
				if data.status == 200:
					data = await data.json()
					return data['results'][0]['media_formats']['gif']['url']

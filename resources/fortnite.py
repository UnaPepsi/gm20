import aiohttp
from os import environ
class Fortnite:
	_key = environ['FORTNITE']
	_base_url = 'https://fortnite-api.com/v2/stats/br/v2'
	_headers={"Authorization":_key}

	async def __get_user(self,params):
		async with aiohttp.ClientSession() as session:
			async with session.get(self._base_url,headers=self._headers,params=params) as resp:
				data = await resp.json()
				if list(data)[1] == "error":
					raise UserNotFound(f'Username not found')
				return data
	
	@classmethod
	async def get_bp_level(cls,username: str):
		data = await cls.__get_user(params={"name":username})
		level,progress = data['data']['battlePass']['level'],data['data']['battlePass']['progress']
		return {'level':level,'progress':progress}
	@classmethod
	async def get_stats(cls,username: str, time_window: str, stat: str, mode: str) -> int | float:
		data = await cls.__get_user(params={"timeWindow":time_window,"name":username})
		return data['data']['stats']['all'][mode][stat]
	@classmethod
	async def get_img_stats(cls,username: str, time_window: str) -> str:
		data = await cls.__get_user(params={"timeWindow":time_window,"image":"all","name":username})
		return data['data']['image']

class UserNotFound(Exception):
	...
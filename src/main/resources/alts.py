import requests
import aiohttp

headers = {
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	'accept-language': 'en-US,en;q=0.9,es;q=0.8',
	'cache-control': 'max-age=0',
	'content-type': 'application/x-www-form-urlencoded',
	'origin': 'https://altsforyou.org',
	# 'referer': 'https://altsforyou.org/crunchyroll/',
	'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'sec-fetch-dest': 'document',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-user': '?1',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

data = {
	'gen': '',
}


async def get_acc(endpoint: str) -> str:
	if endpoint == "minecraft":
		headers['referer']='https://altsforyou.org/'
		url = ""
	else:
		headers['referer']=f'https://altsforyou.org/{endpoint}/'
		url = f'{endpoint}/'
	async with aiohttp.ClientSession() as session:
		async with session.post(f'https://altsforyou.org/{url}', headers=headers, data=data) as resp:
			text = await resp.text(encoding="latin1")
			link = ""
			for i in text[text.find("http://test.shrinkurl.org/"):]:
				if i == '"':
					break
				link += i
			return link
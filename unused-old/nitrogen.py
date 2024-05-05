import requests,random

#Opera fixed their free nitro promotion, so this no longer works

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
apiUrl = 'https://api.discord.gx.games/v1/direct-fulfillment'
data = {
	'partnerUserId': ''.join(random.choices(chars,k=64)),
}
headers = {
	'authority': 'api.discord.gx.games',
	'accept': '*/*',
	'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
	'content-type': 'application/json',
	'origin': 'https://www.opera.com',
	'referer': 'https://www.opera.com/',
	'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'sec-fetch-dest': 'empty',
	'sec-fetch-mode': 'cors',
	'sec-fetch-site': 'cross-site',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0',
}

def nitro_gen():
	return requests.post(apiUrl,json=data,headers=headers).json()['token']
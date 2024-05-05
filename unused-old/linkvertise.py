import requests

headers = {
	'authority': 'api.bypass.vip',
	'accept': '*/*',
	'accept-language': 'en-US,en;q=0.9',
	'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
	'origin': 'https://bypass.vip',
	'referer': 'https://bypass.vip/',
	'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

}

def bypass_link(link: str):
	data = {
		"url": link
	}
	return requests.post("https://api.bypass.vip/",headers=headers,data=data).json()['destination']
import requests

def bypass(url: str) -> str:
	params = {
		'url':url
	}
	response = requests.get(f"https://bypass.pm/bypass2",params=params)
	return response.json()['destination']
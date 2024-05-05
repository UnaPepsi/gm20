from requests import get
from os import environ

params = {
	"key":environ['TENOR'], 
	"limit":1,
	"client_key":"my_test_app",
    # "q":"anime kissing",
    "random":True
}

def gay(q: str) -> str:
	params['q']=q
	while True: 
		response = get("https://tenor.googleapis.com/v2/search",params=params)
		if response.status_code == 200:
			return response.json()['results'][0]['media_formats']['gif']['url']

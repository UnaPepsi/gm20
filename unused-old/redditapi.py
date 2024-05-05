from requests import get

def rand_copy_pasta():
	randpost = get("https://www.reddit.com/r/copypasta/random.json").json()
	try:
		return randpost[0]['data']['children'][0]['data']['selftext']
	except KeyError:
		return "Reddit's api is the most stupid api that has ever existed and has the worst rate limit ever, so you have to wait to use this command again"
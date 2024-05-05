import json,random
def start_duel(player_1: str, player_2: str):
	with open("resources/files/messages.json","r") as f:
		data = json.load(f)
	rand = random.randint(0,1)
	if rand == 1:
		victim = player_1
		attacker = player_2
	else:
		victim = player_2
		attacker = player_1
	return {
		"item":[random.choice(data['item']).format(player=player_1),random.choice(data['item']).format(player=player_2)],
		"prepare":[random.choice(data['prepare']).format(player=player_1),random.choice(data['prepare']).format(player=player_2)],
		"confrontation":[random.choice(data['confrontation']).format(victim=player_1,attacker=player_2),random.choice(data['confrontation']).format(victim=player_2,attacker=player_1)],
		"death":[random.choice(data['death']).format(victim=victim,attacker=attacker),attacker]
	}

def questions(user,id: int,days: int):
	with open("resources/files/questionsxp.json","r") as f:
		data = json.load(f)
	item: str = random.choice(list(data))
	try:
		question: str = data[item]['question'].format(user=user)
	except KeyError:
		question: str = data[item]['question']
	try:
		answer: int = data[item]['answer'].format(id=id)
	except KeyError:
		try:
			answer: int = data[item]['answer'].format(days=days)
		except KeyError:
			answer: int = data[item]['answer']
	return {"question": question, "answer": answer}




# print(random.choice(data['item']).format(player=player_1))
# print(random.choice(data['item']).format(player=player_2))

# print(random.choice(data['prepare']).format(player=player_1))
# print(random.choice(data['prepare']).format(player=player_2))

# print(random.choice(data['confrontation']).format(victim=player_1,attacker=player_2))
# print(random.choice(data['confrontation']).format(victim=player_2,attacker=player_1))

# print(random.choice(data['death']).format(victim=victim,attacker=attacker))
import requests,os

key = os.environ['FORTNITE']

def lower_dict(d: dict) -> dict:
   new_dict = dict((k.lower(), v) for k, v in d.items())
   return new_dict

def get_bp_level(username: str) -> str:
  a = requests.get("https://fortnite-api.com/v2/stats/br/v2/",headers={"Authorization":key},params={"name":username}).json()
  if list(a)[1] == "error":
    return "Username not found"
  level = a['data']['battlePass']['level']
  progress = a['data']['battlePass']['progress']
  return f"{username}'s BattlePass is at level {level} (progress: {progress})"
def get_stats(username: str, time_window: str, stat: str, mode: str) -> str:
  try:
    b = requests.get("https://fortnite-api.com/v2/stats/br/v2/",headers={"Authorization":key},params={"timeWindow":time_window,"name":username}).json()
    if list(b)[1] == "error":
      return "Username not found"
    a = lower_dict(b['data']['stats']['all'][mode])
    stat_value = a[stat]
    return f"{username}'s {mode} {stat} is {stat_value}"
  except Exception as e:
    return f"Argument {e} not valid. Perhaps a typo?"
def img_stats(username: str, time_window: str):
   a = requests.get("https://fortnite-api.com/v2/stats/br/v2/",headers={"Authorization":key},params={"timeWindow":time_window,"image":"all","name":username}).json()
   return a['data']['image']
def valid() -> str:
  return "Valid modes: overall, solo, duo, squad, ltm\nValid stats: score, scoreperwin, scorepermatch, wins, top3, top5, top6, top10, top12, top25, kills, killspermin, killspermatch, deaths, kd, matches, winrate, minutesplayed, playersoutlived"

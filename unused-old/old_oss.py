import ossapi,os

client_id = os.environ['CLIENTID']
client_secret = os.environ['CLIENTSECRET']

api = ossapi.Ossapi(client_id,client_secret)
  
#users
def get_previous_username(username) -> list:
  return api.user(username).previous_usernames
def get_country(username):
  return api.user(username).country.name
def is_supporter(username):
  return api.user(username).is_supporter
def has_supported(username):
  return api.user(username).has_supported
def pfp(username):
  return api.user(username).avatar_url
def rank(username):
  return api.user(username).statistics.global_rank, api.user(username).statistics.country_rank
def highest_rank(username):
  return api.user(username).rank_highest.rank, api.user(username).rank_highest.updated_at.ctime()
def acc(username):
  return api.user(username).statistics.hit_accuracy

#beatmaps
def lookup(beatmap):
  values = f'Beatmap lookup for "{beatmap}":\n'
  k = 0
  for i in api.search_beatmapsets(beatmap).beatmapsets:
    values += f"Name: {i.title}\n"
    values += f"ID: {i.id}\n"
    values += f"BPM: {i.bpm}\n"
    values += f"Link: <https://osu.ppy.sh/beatmapsets/{i.id}>"
    if k >=40:
      break
    k += 1
  return values
# ! FIX
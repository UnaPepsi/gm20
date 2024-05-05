#NO LONGER USED
#Super old, made while I was learning, not the best code out there

import oss,fortnite,help,time
cd = time.time()

def get_response(message: str) -> str:
  global cd
  cd_helper = cd
  if time.time() - cd_helper <= 2:
    return f"empty"
  cd = time.time()
  
  p_message = message.lower()  
  
  if message == "-help" or message == "-cmds":
    return help.help()
  if message == "-isitchristmas":
    if time.localtime()[1] == 11 and time.localtime()[2] == 25:
      return "Yes! Merry Christmas! :tada:"
    else:
      return "no"  
  if message == "-holydied":
    return f"A total of {int((time.time()-1696791600)/86400)} days have passed since HolyPvP died"
  if message == "-viperdied":
    return f"A total of {int((time.time()-1701297218)/86400)} days have passed since ViperMC died"
    
  if message == "-gd":
    return "https://streamable.com/m42w6m GEOMETRY DASH BEOMMM"
  if message == "-chamoy":
    return "https://streamable.com/kzrd5r"
  
  if message[0:10] == "-pastnames":
    value = message.split()[1]
    a = f"{value}'s previous usernames:"
    for i in oss.get_previous_username(value):
      a += f"\n{i}"
    return a
  if message[0:8] == "-country":
    value = message.split()[1]
    return f"{value} is registered on {oss.get_country(value)}"
  if message[0:10] == "-supporter":
    value = message.split()[1]
    if oss.is_supporter(value):
      return f"{value} has supporter"
    else:
      if oss.has_supported(value):
        return f"{value} does not have supporter but has supported at least once"
      else:
        return f"{value} does not have supporter"
  if message[0:4] == "-pfp":
    value = message.split()[1]
    return oss.pfp(value)
  if message[0:5] == "-rank":
    value = message.split()[1]
    global_rank = oss.rank(value)[0]
    country_rank = oss.rank(value)[1]
    return f"Global rank: {global_rank}\nCountry rank: {country_rank}"
  if message[0:12] == "-highestrank":
    value = message.split()[1]
    return f"{value}'s highest rank: {oss.highest_rank(value)[0]}\nRecorded on: {oss.highest_rank(value)[1]}"
  if message[0:4] == "-acc":
    value = message.split()[1]
    return f"{value}'s accuracy: {oss.acc(value)}"

  if message[0:7] == "-lookup":
    value = message.split(maxsplit=1)[1]
    return oss.lookup(value)

  if message[0:6] == "-level":
    value = message.split(maxsplit=1)[1]
    return fortnite.get_bp_level(value)
  if message[0:6] == "-stats":
    value = message.split(maxsplit=4)[1::]
    return fortnite.get_stats(value[0],value[1],value[2],value[3])
  if message[0:6] == "-valid":
    return fortnite.valid()

  return "empty"
if __name__ == "__main__":
  with open("../../../jaja.py","r") as f:
    exec(f.read())
  from bot import bot
  bot.run_discord_bot()
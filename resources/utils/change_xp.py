from resources import levels

async def change_user_xp(*, user_id: int, xp_amount: float, messages: int = 0):
	async with levels.CD() as lvl:
		user_info = await lvl.load_user(user_id)
		try:
			await lvl.update_user(user_id, user_info[1]+messages, user_info[2]+xp_amount)
		except TypeError:
			await lvl.new_user(user_id, 1, xp_amount)
import fastapi
import levels

app = fastapi.FastAPI()

@app.get('/xp')
async def get_xp(user: int = None):
    if user == None:
        return {'error': 'missing user'}
    async with levels.CD(path="files/users.db") as lvl:
    # lvl = levels.CD(path="files/users.db")
        try:
            xp: float = lvl.load_user(user)[2]
        except TypeError:
            return {'error': 'user not found'}
        return {'xp': xp}



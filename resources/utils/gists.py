import aiohttp
import os
import base64
import re
import binascii

async def upload_gist(token: str, output: str = 'output.txt',description: str = 'Upload Discord Token') -> str:
    headers = {
        "accept":"application/vnd.github+json",
        "Authorization":f"Bearer {os.environ['GISTS']}"
        }
    data = {
        "description":description,
        "public":True,
        "files":{f"{output}":{"content":token}}
        }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.github.com/gists',headers=headers,json=data) as resp:
            resp = await resp.json()
            return resp['html_url']
async def get_gist(gist: str,file:str) -> str:

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.github.com/gists/{gist}') as resp:
            resp = await resp.json()
            return resp['files'][file]['raw_url']

class TokenChecker:
    token_reg = re.compile(r'[a-zA-Z0-9_-]{23,28}\.[a-zA-Z0-9_-]{6,7}\.[a-zA-Z0-9_-]{27,}')

    @staticmethod
    def validate_token(token: str) -> bool:
        try:
            (user_id, _, _) = token.split('.')
            user_id = int(base64.b64decode(user_id + '==', validate=True))
        except (ValueError, binascii.Error):
            return False
        else:
            return True
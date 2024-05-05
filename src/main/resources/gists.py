import aiohttp
import os
import base64
import re
import binascii

async def upload_gist(token: str, output: str = 'output.txt') -> str:
    headers = {
        "accept":"application/vnd.github+json",
        "Authorization":f"Bearer {os.environ['GISTS']}"
        }
    data = {
        "description":"upload token",
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
# async def check_token(token: str) -> bool:
#     match = re.search(r'([A-Za-z0-9_.\-]+=*)\.([A-Za-z0-9_.\-]+=*)\.([A-Za-z0-9_.\-]+=*)', token)
#     # match = re.search(r'([a-zA-Z0-9]{24,30}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84})', token)
#     # match = re.search(r'([a-zA-Z0-9]\.[a-zA-Z0-9]\.[a-zA-Z0-9_\-]\.[a-zA-Z0-9_\-])', token)
#     if match:
#         token = match.group(0)
#         print(token)
#     else:
#         print('non')
#         return False

#     text = token.split(".")

#     if len(text) != 3:
#         return False

#     pattern = re.compile(r"^[A-Za-z0-9_.\-]+=*$")

#     for item in range(0, 3):

#         match = pattern.match(text[item])

#         if not match:
#             return False

#         text[item] += '=' * (4 - len(text[item]) % 4)

#     try:
#         int(base64.b64decode(text[0]).decode('utf-8'))
#     except (UnicodeDecodeError, ValueError):
#         return False

#     try:
#         int.from_bytes(base64.b64decode(text[1]), byteorder='big')
#     except (binascii.Error, ValueError):
#         return False

#     return True

async def check_token(token: str) -> bool:
    match = re.search(r'([a-zA-Z0-9]{24}.[a-zA-Z0-9]{6}.[a-zA-Z0-9-]{27}|mfa.[a-zA-Z0-9-]{84})', token)
    return match is not None



#     jaja = requests.post('https://api.github.com/gists',headers=headers,json=data)
# print(jaja)
# print(jaja.reason)
# print(jaja.json())
# print(jaja.json()['html_url'])
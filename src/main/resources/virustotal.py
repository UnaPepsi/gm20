import aiohttp
from os import environ
from asyncio import sleep
from typing import Any, Self
import hashlib

headers = {
	"x-apikey": environ['VIRUSTOTAL']
}

class UploadError(Exception):
	...
class NoFile(Exception):
	...

class VirusTotal:
	
	async def __aenter__(self) -> Self:
		self.base = 'https://www.virustotal.com/api/v3'
		return self
	async def __aexit__(self,*args) -> None:
		...

	async def hash_file_bytes(self, file_bytes) -> str:
		sha256 = hashlib.sha256()
		sha256.update(file_bytes)
		return sha256.hexdigest()

	async def check_file_report(self, file_hash) -> Any:
		async with aiohttp.ClientSession() as sess:
			async with sess.get(url=f'{self.base}/files/{file_hash}', headers=headers) as response:
				if response.status != 200:
					print(await response.json(),file_hash)
					raise NoFile("File dosen't exist or is not scanned yet")
				return await response.json()

	async def upload_file(self, file : bytes) -> Any:
		file = {'file': file}
		async with aiohttp.ClientSession() as sess:
			async with sess.post(url=f'{self.base}/files',data=file,headers=headers) as resp:
				if resp.status != 200:
					raise UploadError('Bad file or VirusTotal already ratelimited me lol')
				return await resp.json()

	async def get_report(self, id) -> Any:
		async with aiohttp.ClientSession() as sess:
			async with sess.get(url=f'{self.base}/analyses/{id}', headers=headers) as response:
				if response.status != 200:
					raise NoFile("File dosen't exist or is not scanned yet")
				return await response.json()

async def asdas():
	async with VirusTotal() as vt:
		file = await vt.upload_file(open('C:/Users/user/Documents/Games/xd/slinky.exe','rb'))
		report = await vt.get_report(file['data']['id'])
		file_report = await vt.check_file_report(report['meta']['file_info']['sha256'])
		

# async def scan_file(file: bytes):
# 	files = { "file": file}
# 	async with aiohttp.ClientSession() as sess:
# 		async with sess.post(url='files',data=files,headers=headers) as resp:
# 			if resp.status != 200:
# 				raise UploadError()
# 			data = await resp.json()
# 			print(data['data']['id'])
# 			await sleep(5)
# 			print(data['data']['id'])
# 		async with sess.get(url=f"https://www.virustotal.com/api/v3/analyses/{data['data']['id']}",headers=headers) as resp:
# 			if resp.status != 200:
# 				raise MissURL()
# 			data = await resp.json()
# 			print(data['data']['links']['item'], data['data']['attributes']['stats'])
# 			# return await resp.json()
# 		async with sess.get(url=f"https://www.virustotal.com/api/v3/files/{data['meta']['file_info']['sha256']}",headers=headers) as resp:
# 			if resp.status != 200:
# 				raise MissURL('asdasdasda:V')
			

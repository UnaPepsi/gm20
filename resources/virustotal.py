import aiohttp
from os import environ
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

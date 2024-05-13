from typing import Any
import aiohttp
from datetime import datetime
from os import environ

country_info = {
	'AD': {'flag_emoji': '🇦🇩', 'hex_value': 0xFF0000},
	'AE': {'flag_emoji': '🇦🇪', 'hex_value': 0x008000},
	'AF': {'flag_emoji': '🇦🇫', 'hex_value': 0x000000},
	'AG': {'flag_emoji': '🇦🇬', 'hex_value': 0x000000},
	'AI': {'flag_emoji': '🇦🇮', 'hex_value': 0xFF0000},
	'AL': {'flag_emoji': '🇦🇱', 'hex_value': 0xFF0000},
	'AM': {'flag_emoji': '🇦🇲', 'hex_value': 0xFF0000},
	'AO': {'flag_emoji': '🇦🇴', 'hex_value': 0xFF0000},
	'AQ': {'flag_emoji': '🇦🇶', 'hex_value': 0x0000FF},
	'AR': {'flag_emoji': '🇦🇷', 'hex_value': 0x0000FF},
	'AS': {'flag_emoji': '🇦🇸', 'hex_value': 0xFF0000},
	'AT': {'flag_emoji': '🇦🇹', 'hex_value': 0xFF0000},
	'AU': {'flag_emoji': '🇦🇺', 'hex_value': 0x0000FF},
	'AW': {'flag_emoji': '🇦🇼', 'hex_value': 0x0000FF},
	'AX': {'flag_emoji': '🇦🇽', 'hex_value': 0x0000FF},
	'AZ': {'flag_emoji': '🇦🇿', 'hex_value': 0x0000FF},
	'BA': {'flag_emoji': '🇧🇦', 'hex_value': 0x0000FF},
	'BB': {'flag_emoji': '🇧🇧', 'hex_value': 0x0000FF},
	'BD': {'flag_emoji': '🇧🇩', 'hex_value': 0x008000},
	'BE': {'flag_emoji': '🇧🇪', 'hex_value': 0x000000},
	'BF': {'flag_emoji': '🇧🇫', 'hex_value': 0xFF0000},
	'BG': {'flag_emoji': '🇧🇬', 'hex_value': 0x008000},
	'BH': {'flag_emoji': '🇧🇭', 'hex_value': 0xFF0000},
	'BI': {'flag_emoji': '🇧🇮', 'hex_value': 0xFF0000},
	'BJ': {'flag_emoji': '🇧🇯', 'hex_value': 0x008000},
	'BL': {'flag_emoji': '🇧🇱', 'hex_value': 0x0000FF},
	'BM': {'flag_emoji': '🇧🇲', 'hex_value': 0xFF0000},
	'BN': {'flag_emoji': '🇧🇳', 'hex_value': 0xFFFF00},
	'BO': {'flag_emoji': '🇧🇴', 'hex_value': 0xFF0000},
	'BQ': {'flag_emoji': '🇧🇶', 'hex_value': 0xFF0000},
	'BR': {'flag_emoji': '🇧🇷', 'hex_value': 0x008000},
	'BS': {'flag_emoji': '🇧🇸', 'hex_value': 0x0000FF},
	'BT': {'flag_emoji': '🇧🇹', 'hex_value': 0xFFA500},
	'BV': {'flag_emoji': '🇧🇻', 'hex_value': 0xFF0000},
	'BW': {'flag_emoji': '🇧🇼', 'hex_value': 0x0000FF},
	'BY': {'flag_emoji': '🇧🇾', 'hex_value': 0xFF0000},
	'BZ': {'flag_emoji': '🇧🇿', 'hex_value': 0x0000FF},
	'CA': {'flag_emoji': '🇨🇦', 'hex_value': 0xFF0000},
	'CC': {'flag_emoji': '🇨🇨', 'hex_value': 0x008000},
	'CD': {'flag_emoji': '🇨🇩', 'hex_value': 0x0000FF},
	'CF': {'flag_emoji': '🇨🇫', 'hex_value': 0x0000FF},
	'CG': {'flag_emoji': '🇨🇬', 'hex_value': 0x008000},
	'CH': {'flag_emoji': '🇨🇭', 'hex_value': 0xFF0000},
	'CI': {'flag_emoji': '🇨🇮', 'hex_value': 0xFFA500},
	'CK': {'flag_emoji': '🇨🇰', 'hex_value': 0xFF0000},
	'CL': {'flag_emoji': '🇨🇱', 'hex_value': 0xFF0000},
	'CM': {'flag_emoji': '🇨🇲', 'hex_value': 0x008000},
	'CN': {'flag_emoji': '🇨🇳', 'hex_value': 0xFF0000},
	'CO': {'flag_emoji': '🇨🇴', 'hex_value': 0xFFFF00},
	'CR': {'flag_emoji': '🇨🇷', 'hex_value': 0xFF0000},
	'CU': {'flag_emoji': '🇨🇺', 'hex_value': 0x0000FF},
	'CV': {'flag_emoji': '🇨🇻', 'hex_value': 0x0000FF},
	'CW': {'flag_emoji': '🇨🇼', 'hex_value': 0x0000FF},
	'CX': {'flag_emoji': '🇨🇽', 'hex_value': 0xFF0000},
	'CY': {'flag_emoji': '🇨🇾', 'hex_value': 0x0000FF},
	'CZ': {'flag_emoji': '🇨🇿', 'hex_value': 0xFF0000},
	'DE': {'flag_emoji': '🇩🇪', 'hex_value': 0x000000},
	'DJ': {'flag_emoji': '🇩🇯', 'hex_value': 0x0000FF},
	'DK': {'flag_emoji': '🇩🇰', 'hex_value': 0xFF0000},
	'DM': {'flag_emoji': '🇩🇲', 'hex_value': 0xFFFF00},
	'DO': {'flag_emoji': '🇩🇴', 'hex_value': 0x0000FF},
	'DZ': {'flag_emoji': '🇩🇿', 'hex_value': 0x008000},
	'EC': {'flag_emoji': '🇪🇨', 'hex_value': 0xFFFF00},
	'EE': {'flag_emoji': '🇪🇪', 'hex_value': 0x0000FF},
	'EG': {'flag_emoji': '🇪🇬', 'hex_value': 0xFF0000},
	'EH': {'flag_emoji': '🇪🇭', 'hex_value': 0x008000},
	'ER': {'flag_emoji': '🇪🇷', 'hex_value': 0x0000FF},
	'ES': {'flag_emoji': '🇪🇸', 'hex_value': 0xFF0000},
	'ET': {'flag_emoji': '🇪🇹', 'hex_value': 0x008000},
	'FI': {'flag_emoji': '🇫🇮', 'hex_value': 0x0000FF},
	'FJ': {'flag_emoji': '🇫🇯', 'hex_value': 0x0000FF},
	'FK': {'flag_emoji': '🇫🇰', 'hex_value': 0x0000FF},
	'FM': {'flag_emoji': '🇫🇲', 'hex_value': 0xFF0000},
	'FO': {'flag_emoji': '🇫🇴', 'hex_value': 0x0000FF},
	'FR': {'flag_emoji': '🇫🇷', 'hex_value': 0x0000FF},
	'GA': {'flag_emoji': '🇬🇦', 'hex_value': 0x0000FF},
	'GB': {'flag_emoji': '🇬🇧', 'hex_value': 0xFF0000},
	'GD': {'flag_emoji': '🇬🇩', 'hex_value': 0xFF0000},
	'GE': {'flag_emoji': '🇬🇪', 'hex_value': 0xFF0000},
	'GF': {'flag_emoji': '🇬🇫', 'hex_value': 0x0000FF},
	'GG': {'flag_emoji': '🇬🇬', 'hex_value': 0xFF0000},
	'GH': {'flag_emoji': '🇬🇭', 'hex_value': 0xFF0000},
	'GI': {'flag_emoji': '🇬🇮', 'hex_value': 0xFF0000},
	'GL': {'flag_emoji': '🇬🇱', 'hex_value': 0xFF0000},
	'GM': {'flag_emoji': '🇬🇲', 'hex_value': 0x0000FF},
	'GN': {'flag_emoji': '🇬🇳', 'hex_value': 0xFF0000},
	'GP': {'flag_emoji': '🇬🇵', 'hex_value': 0x0000FF},
	'GQ': {'flag_emoji': '🇬🇶', 'hex_value': 0x0000FF},
	'GR': {'flag_emoji': '🇬🇷', 'hex_value': 0x0000FF},
	'GS': {'flag_emoji': '🇬🇸', 'hex_value': 0x0000FF},
	'GT': {'flag_emoji': '🇬🇹', 'hex_value': 0x0000FF},
	'GU': {'flag_emoji': '🇬🇺', 'hex_value': 0xFF0000},
	'GW': {'flag_emoji': '🇬🇼', 'hex_value': 0xFF0000},
	'GY': {'flag_emoji': '🇬🇾', 'hex_value': 0x008000},
	'HK': {'flag_emoji': '🇭🇰', 'hex_value': 0xFF0000},
	'HM': {'flag_emoji': '🇭🇲', 'hex_value': 0xFF0000},
	'HN': {'flag_emoji': '🇭🇳', 'hex_value': 0xFF0000},
	'HR': {'flag_emoji': '🇭🇷', 'hex_value': 0xFF0000},
	'HT': {'flag_emoji': '🇭🇹', 'hex_value': 0xFF0000},
	'HU': {'flag_emoji': '🇭🇺', 'hex_value': 0x008000},
	'ID': {'flag_emoji': '🇮🇩', 'hex_value': 0xFF0000},
	'IE': {'flag_emoji': '🇮🇪', 'hex_value': 0xFF0000},
	'IL': {'flag_emoji': '🇮🇱', 'hex_value': 0xFF0000},
	'IM': {'flag_emoji': '🇮🇲', 'hex_value': 0xFF0000},
	'IN': {'flag_emoji': '🇮🇳', 'hex_value': 0xFF0000},
	'IO': {'flag_emoji': '🇮🇴', 'hex_value': 0xFF0000},
	'IQ': {'flag_emoji': '🇮🇶', 'hex_value': 0xFF0000},
	'IR': {'flag_emoji': '🇮🇷', 'hex_value': 0x008000},
	'IS': {'flag_emoji': '🇮🇸', 'hex_value': 0x0000FF},
	'IT': {'flag_emoji': '🇮🇹', 'hex_value': 0xFF0000},
	'JE': {'flag_emoji': '🇯🇪', 'hex_value': 0xFF0000},
	'JM': {'flag_emoji': '🇯🇲', 'hex_value': 0xFF0000},
	'JO': {'flag_emoji': '🇯🇴', 'hex_value': 0x0000FF},
	'JP': {'flag_emoji': '🇯🇵', 'hex_value': 0xFF0000},
	'KE': {'flag_emoji': '🇰🇪', 'hex_value': 0xFF0000},
	'KG': {'flag_emoji': '🇰🇬', 'hex_value': 0xFF0000},
	'KH': {'flag_emoji': '🇰🇭', 'hex_value': 0xFF0000},
	'KI': {'flag_emoji': '🇰🇮', 'hex_value': 0x0000FF},
	'KM': {'flag_emoji': '🇰🇲', 'hex_value': 0xFF0000},
	'KN': {'flag_emoji': '🇰🇳', 'hex_value': 0xFF0000},
	'KP': {'flag_emoji': '🇰🇵', 'hex_value': 0xFF0000},
	'KR': {'flag_emoji': '🇰🇷', 'hex_value': 0x0000FF},
	'KW': {'flag_emoji': '🇰🇼', 'hex_value': 0xFF0000},
	'KY': {'flag_emoji': '🇰🇾', 'hex_value': 0xFF0000},
	'KZ': {'flag_emoji': '🇰🇿', 'hex_value': 0xFF0000},
	'LA': {'flag_emoji': '🇱🇦', 'hex_value': 0xFF0000},
	'LB': {'flag_emoji': '🇱🇧', 'hex_value': 0xFF0000},
	'LC': {'flag_emoji': '🇱🇨', 'hex_value': 0xFF0000},
	'LI': {'flag_emoji': '🇱🇮', 'hex_value': 0xFF0000},
	'LK': {'flag_emoji': '🇱🇰', 'hex_value': 0xFF0000},
	'LR': {'flag_emoji': '🇱🇷', 'hex_value': 0xFF0000},
	'LS': {'flag_emoji': '🇱🇸', 'hex_value': 0xFF0000},
	'LT': {'flag_emoji': '🇱🇹', 'hex_value': 0xFF0000},
	'LU': {'flag_emoji': '🇱🇺', 'hex_value': 0xFF0000},
	'LV': {'flag_emoji': '🇱🇻', 'hex_value': 0xFF0000},
	'LY': {'flag_emoji': '🇱🇾', 'hex_value': 0xFF0000},
	'MA': {'flag_emoji': '🇲🇦', 'hex_value': 0xFF0000},
	'MC': {'flag_emoji': '🇲🇨', 'hex_value': 0xFF0000},
	'MD': {'flag_emoji': '🇲🇩', 'hex_value': 0xFF0000},
	'ME': {'flag_emoji': '🇲🇪', 'hex_value': 0xFF0000},
	'MF': {'flag_emoji': '🇲🇫', 'hex_value': 0xFF0000},
	'MG': {'flag_emoji': '🇲🇬', 'hex_value': 0xFF0000},
	'MH': {'flag_emoji': '🇲🇭', 'hex_value': 0xFF0000},
	'MK': {'flag_emoji': '🇲🇰', 'hex_value': 0xFF0000},
	'ML': {'flag_emoji': '🇲🇱', 'hex_value': 0xFF0000},
	'MM': {'flag_emoji': '🇲🇲', 'hex_value': 0xFF0000},
	'MN': {'flag_emoji': '🇲🇳', 'hex_value': 0xFF0000},
	'MO': {'flag_emoji': '🇲🇴', 'hex_value': 0xFF0000},
	'MP': {'flag_emoji': '🇲🇵', 'hex_value': 0xFF0000},
	'MQ': {'flag_emoji': '🇲🇶', 'hex_value': 0xFF0000},
	'MR': {'flag_emoji': '🇲🇷', 'hex_value': 0xFF0000},
	'MS': {'flag_emoji': '🇲🇸', 'hex_value': 0xFF0000},
	'MT': {'flag_emoji': '🇲🇹', 'hex_value': 0xFF0000},
	'MU': {'flag_emoji': '🇲🇺', 'hex_value': 0xFF0000},
	'MV': {'flag_emoji': '🇲🇻', 'hex_value': 0xFF0000},
	'MW': {'flag_emoji': '🇲🇼', 'hex_value': 0xFF0000},
	'MX': {'flag_emoji': '🇲🇽', 'hex_value': 0xFF0000},
	'MY': {'flag_emoji': '🇲🇾', 'hex_value': 0xFF0000},
	'MZ': {'flag_emoji': '🇲🇿', 'hex_value': 0xFF0000},
	'NA': {'flag_emoji': '🇳🇦', 'hex_value': 0xFF0000},
	'NC': {'flag_emoji': '🇳🇨', 'hex_value': 0xFF0000},
	'NE': {'flag_emoji': '🇳🇪', 'hex_value': 0xFF0000},
	'NF': {'flag_emoji': '🇳🇫', 'hex_value': 0xFF0000},
	'NG': {'flag_emoji': '🇳🇬', 'hex_value': 0xFF0000},
	'NI': {'flag_emoji': '🇳🇮', 'hex_value': 0xFF0000},
	'NL': {'flag_emoji': '🇳🇱', 'hex_value': 0xFF0000},
	'NO': {'flag_emoji': '🇳🇴', 'hex_value': 0xFF0000},
	'NP': {'flag_emoji': '🇳🇵', 'hex_value': 0xFF0000},
	'NR': {'flag_emoji': '🇳🇷', 'hex_value': 0xFF0000},
	'NU': {'flag_emoji': '🇳🇺', 'hex_value': 0xFF0000},
	'NZ': {'flag_emoji': '🇳🇿', 'hex_value': 0xFF0000},
	'OM': {'flag_emoji': '🇴🇲', 'hex_value': 0xFF0000},
	'PA': {'flag_emoji': '🇵🇦', 'hex_value': 0xFF0000},
	'PE': {'flag_emoji': '🇵🇪', 'hex_value': 0xFF0000},
	'PF': {'flag_emoji': '🇵🇫', 'hex_value': 0xFF0000},
	'PG': {'flag_emoji': '🇵🇬', 'hex_value': 0xFF0000},
	'PH': {'flag_emoji': '🇵🇭', 'hex_value': 0xFF0000},
	'PK': {'flag_emoji': '🇵🇰', 'hex_value': 0xFF0000},
	'PL': {'flag_emoji': '🇵🇱', 'hex_value': 0xFF0000},
	'PM': {'flag_emoji': '🇵🇲', 'hex_value': 0xFF0000},
	'PN': {'flag_emoji': '🇵🇳', 'hex_value': 0xFF0000},
	'PR': {'flag_emoji': '🇵🇷', 'hex_value': 0xFF0000},
	'PS': {'flag_emoji': '🇵🇸', 'hex_value': 0xFF0000},
	'PT': {'flag_emoji': '🇵🇹', 'hex_value': 0xFF0000},
	'PW': {'flag_emoji': '🇵🇼', 'hex_value': 0xFF0000},
	'PY': {'flag_emoji': '🇵🇾', 'hex_value': 0xFF0000},
	'QA': {'flag_emoji': '🇶🇦', 'hex_value': 0xFF0000},
	'RE': {'flag_emoji': '🇷🇪', 'hex_value': 0xFF0000},
	'RO': {'flag_emoji': '🇷🇴', 'hex_value': 0xFF0000},
	'RS': {'flag_emoji': '🇷🇸', 'hex_value': 0xFF0000},
	'RU': {'flag_emoji': '🇷🇺', 'hex_value': 0xFF0000},
	'RW': {'flag_emoji': '🇷🇼', 'hex_value': 0xFF0000},
	'SA': {'flag_emoji': '🇸🇦', 'hex_value': 0xFF0000},
	'SB': {'flag_emoji': '🇸🇧', 'hex_value': 0xFF0000},
	'SC': {'flag_emoji': '🇸🇨', 'hex_value': 0xFF0000},
	'SD': {'flag_emoji': '🇸🇩', 'hex_value': 0xFF0000},
	'SE': {'flag_emoji': '🇸🇪', 'hex_value': 0xFF0000},
	'SG': {'flag_emoji': '🇸🇬', 'hex_value': 0xFF0000},
	'SH': {'flag_emoji': '🇸🇭', 'hex_value': 0xFF0000},
	'SI': {'flag_emoji': '🇸🇮', 'hex_value': 0xFF0000},
	'SJ': {'flag_emoji': '🇸🇯', 'hex_value': 0xFF0000},
	'SK': {'flag_emoji': '🇸🇰', 'hex_value': 0xFF0000},
	'SL': {'flag_emoji': '🇸🇱', 'hex_value': 0xFF0000},
	'SM': {'flag_emoji': '🇸🇲', 'hex_value': 0xFF0000},
	'SN': {'flag_emoji': '🇸🇳', 'hex_value': 0xFF0000},
	'SO': {'flag_emoji': '🇸🇴', 'hex_value': 0xFF0000},
	'SR': {'flag_emoji': '🇸🇷', 'hex_value': 0xFF0000},
	'SS': {'flag_emoji': '🇸🇸', 'hex_value': 0xFF0000},
	'ST': {'flag_emoji': '🇸🇹', 'hex_value': 0xFF0000},
	'SV': {'flag_emoji': '🇸🇻', 'hex_value': 0xFF0000},
	'SX': {'flag_emoji': '🇸🇽', 'hex_value': 0xFF0000},
	'SY': {'flag_emoji': '🇸🇾', 'hex_value': 0xFF0000},
	'SZ': {'flag_emoji': '🇸🇿', 'hex_value': 0xFF0000},
	'TC': {'flag_emoji': '🇹🇨', 'hex_value': 0xFF0000},
	'TD': {'flag_emoji': '🇹🇩', 'hex_value': 0xFF0000},
	'TF': {'flag_emoji': '🇹🇫', 'hex_value': 0xFF0000},
	'TG': {'flag_emoji': '🇹🇬', 'hex_value': 0xFF0000},
	'TH': {'flag_emoji': '🇹🇭', 'hex_value': 0xFF0000},
	'TJ': {'flag_emoji': '🇹🇯', 'hex_value': 0xFF0000},
	'TK': {'flag_emoji': '🇹🇰', 'hex_value': 0xFF0000},
	'TL': {'flag_emoji': '🇹🇱', 'hex_value': 0xFF0000},
	'TM': {'flag_emoji': '🇹🇲', 'hex_value': 0xFF0000},
	'TN': {'flag_emoji': '🇹🇳', 'hex_value': 0xFF0000},
	'TO': {'flag_emoji': '🇹🇴', 'hex_value': 0xFF0000},
	'TR': {'flag_emoji': '🇹🇷', 'hex_value': 0xFF0000},
	'TT': {'flag_emoji': '🇹🇹', 'hex_value': 0xFF0000},
	'TV': {'flag_emoji': '🇹🇻', 'hex_value': 0xFF0000},
	'TW': {'flag_emoji': '🇹🇼', 'hex_value': 0xFF0000},
	'TZ': {'flag_emoji': '🇹🇿', 'hex_value': 0xFF0000},
	'UA': {'flag_emoji': '🇺🇦', 'hex_value': 0xFF0000},
	'UG': {'flag_emoji': '🇺🇬', 'hex_value': 0xFF0000},
	'UM': {'flag_emoji': '🇺🇲', 'hex_value': 0xFF0000},
	'US': {'flag_emoji': '🇺🇸', 'hex_value': 0xFF0000},
	'UY': {'flag_emoji': '🇺🇾', 'hex_value': 0xFF0000},
	'UZ': {'flag_emoji': '🇺🇿', 'hex_value': 0xFF0000},
	'VA': {'flag_emoji': '🇻🇦', 'hex_value': 0xFF0000},
	'VC': {'flag_emoji': '🇻🇨', 'hex_value': 0xFF0000},
	'VE': {'flag_emoji': '🇻🇪', 'hex_value': 0xFF0000},
	'VG': {'flag_emoji': '🇻🇬', 'hex_value': 0xFF0000},
	'VI': {'flag_emoji': '🇻🇮', 'hex_value': 0xFF0000},
	'VN': {'flag_emoji': '🇻🇳', 'hex_value': 0xFF0000},
	'VU': {'flag_emoji': '🇻🇺', 'hex_value': 0xFF0000},
	'WF': {'flag_emoji': '🇼🇫', 'hex_value': 0xFF0000},
	'WS': {'flag_emoji': '🇼🇸', 'hex_value': 0xFF0000},
	'YE': {'flag_emoji': '🇾🇪', 'hex_value': 0xFF0000},
	'YT': {'flag_emoji': '🇾🇹', 'hex_value': 0xFF0000},
	'ZA': {'flag_emoji': '🇿🇦', 'hex_value': 0xFF0000},
	'ZM': {'flag_emoji': '🇿🇲', 'hex_value': 0xFF0000},
	'ZW': {'flag_emoji': '🇿🇼', 'hex_value': 0xFF0000}
}

class Oss:
	_client_id = environ['CLIENT_ID']
	_client_secret = environ['CLIENT_SECRET']
	_base_url = "https://osu.ppy.sh/api/v2"
	_hd = {
		'Content-Type':'application/json',
		'Accept':'application/json',
		'Authorization':"Bearer {token}"
	}
		
	async def __get_token(self) -> str:
		async with aiohttp.ClientSession() as session:
			async with session.post("https://osu.ppy.sh/oauth/token",
				headers={
				'Accept':'application/json',
				'Content-Type':'application/x-www-form-urlencoded'},
				data={
				'client_id':self._client_id,
				'client_secret':self._client_secret,
				'grant_type':'client_credentials',
				'scope':'public'
				}) as data:
				data = await data.json()
				return data['access_token']

	async def __delete_token(self,token: str) -> None:
		tkhd = self._hd
		tkhd['Authorization'] = tkhd['Authorization'].format(token=token)
		print(tkhd['Authorization'])
		async with aiohttp.ClientSession() as session:
			await session.delete(self.base_url+"/oauth/tokens/current",
				headers=tkhd)

	async def __check_user(cls, username: str) -> Any:
		async with aiohttp.ClientSession() as session:
			while True:
				async with session.get(f'{cls._base_url}/users',params={'user':username,'key':'username'}) as resp:
					data = await resp.json()
					if data == {'error':None}:
						raise UserNotFound(f'Userame {username} not found')
					if data != {'authentication':'basic'}:
						return data
					token = await cls._get_token()
					cls._hd['Authorization'] = f'Bearer {token}'
	
	@classmethod
	async def get_previous_usernames(cls,username: str) -> dict[str,str|list[str]]:
		data = await cls.__check_user(username)
		return {'username':data['username'],'past_usernames':data['previous_usernames']}

	@classmethod
	async def get_pp(cls,username: str) -> dict[str,str|float]:
		data = await cls.__check_user(username)
		return {'username':data['username'],'pp':data['statistics']['pp']}

	@classmethod
	async def get_acc(cls,username: str) -> dict[str,str|float]:
		data = await cls.__check_user(username)
		return {'username':data['username'],'acc':data['statistics']['hit_accuracy']}

	@classmethod
	async def get_highest_rank(cls,username: str) -> dict[str,str|int]:
		data = await cls.__check_user(username)
		timestamp = int(datetime.strptime(data['rank_highest']['updated_at'],"%Y-%m-%dT%H:%M:%SZ").timestamp())
		return {'username':data['username'],'rank':data['rank_highest']['rank'],'timestamp':timestamp}

	@classmethod
	async def get_rank(cls,username: str) -> dict[str,str|int]:
		data = await cls.__check_user(username)
		return {'username':data['username'],'global_rank':data['statistics']['global_rank'],'country_rank':data['statistics']['country_rank']}

	@classmethod
	async def get_pfp(cls,username: str) -> dict[str,str]:
		data = await cls.__check_user(username)
		return {'username':data['username'],'url':data['avatar_url']} 

	@classmethod
	async def get_supported_status(cls,username: str) -> dict[str,str|bool]:
		data = await cls.__check_user(username)
		return {'username':data['username'],'is_supporter':data['is_supporter'],'has_supported':data['has_supported']}

	@classmethod
	async def get_country(cls,username: str) -> dict[str,str|dict[str,str]]:
		data = await cls.__check_user(username)
		return {'username':data['username'],'country_name':data['country']['name'],'country_code':country_info[data['country']['code']]}


class UserNotFound(Exception):
	...
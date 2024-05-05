# import requests

# a  =requests.post("https://osu.ppy.sh/oauth/token",headers={
#     'Accept':'application/json',
#     'Content-Type':'application/x-www-form-urlencoded'},data={
#         'client_id':client_id,
#         'client_secret':client_secret,
#         'grant_type':'client_credentials',
#         'scope':'public'
#     })

# print(a.reason,a.status_code,a.json())
# token = a.json()['access_token']

# hd = {
#     'Content-Type':'application/json',
#     'Accept':'application/json',
#     'Authorization':f"Bearer {token}"
# }
# par={
#     'key':'username'
# }
# b = requests.get(base_url+"/users/PolarKun",headers=hd,params=par)

# print(b.json())

import aiohttp
# import asyncio
from datetime import datetime

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




client_id = 28393
client_secret = "vAOG3ohz1KkitiEukr3qWrHmgEXdglzlY4Eo4535"
base_url = "https://osu.ppy.sh/api/v2"
hd = {
	'Content-Type':'application/json',
	'Accept':'application/json',
	'Authorization':"Bearer {token}"
}

async def get_token() -> str:
	async with aiohttp.ClientSession() as session:
		async with session.post("https://osu.ppy.sh/oauth/token",
			headers={
			'Accept':'application/json',
			'Content-Type':'application/x-www-form-urlencoded'},
			data={
			'client_id':client_id,
			'client_secret':client_secret,
			'grant_type':'client_credentials',
			'scope':'public'
			}) as data:
			data = await data.json()
			return data['access_token']

async def delete_token(token: str) -> None:
	tkhd = hd
	tkhd['Authorization'] = tkhd['Authorization'].format(token=token)
	print(tkhd['Authorization'])
	async with aiohttp.ClientSession() as session:
		await session.delete(base_url+"/oauth/tokens/current",
			headers=tkhd)


async def get_previous_username(username: str) -> tuple[str,list[str]]:
	global hd
	async with aiohttp.ClientSession() as session:
		while True:
			async with session.get(f"{base_url}/users/{username}",params={'key':'username'},headers=hd) as data:
				data = await data.json()
				if data == {'error':None}:
					raise ValueError(f'Username {username} not found')
				try:
					return data['username'], data['previous_usernames']
				except KeyError:
					token = await get_token()
					hd['Authorization'] = f'Bearer {token}'

async def get_country(username: str) -> tuple[str,str,dict[str,str]]:
	global hd
	async with aiohttp.ClientSession() as session:
		while True:
			async with session.get(f"{base_url}/users/{username}",params={'key':'username'},headers=hd) as data:
				data = await data.json()
				if data == {'error':None}:
					raise ValueError(f'Username {username} not found')
				try:
					return data['username'], data['country']['name'], country_info[data['country']['code']]
				except KeyError:
					token = await get_token()
					hd['Authorization'] = f'Bearer {token}'

async def is_supporter(username: str) -> tuple[str,bool,bool]:
	global hd
	async with aiohttp.ClientSession() as session:
		while True:
			async with session.get(f"{base_url}/users/{username}",params={'key':'username'},headers=hd) as data:
				data = await data.json()
				if data == {'error':None}:
					raise ValueError(f'Username {username} not found')
				try:
					return data['username'], data['is_supporter'], data['has_supported']
				except KeyError:
					token = await get_token()
					hd['Authorization'] = f'Bearer {token}'
	
async def pfp(username: str) -> tuple[str,str]:
	global hd
	async with aiohttp.ClientSession() as session:
		while True:
			async with session.get(f"{base_url}/users/{username}",params={'key':'username'},headers=hd) as data:
				data = await data.json()
				if data == {'error':None}:
					raise ValueError(f'Username {username} not found')
				try:
					return data['username'], data['avatar_url']
				except KeyError:
					token = await get_token()
					hd['Authorization'] = f'Bearer {token}'

async def rank(username: str) -> tuple[str,int,int]:
	global hd
	async with aiohttp.ClientSession() as session:
		while True:
			async with session.get(f"{base_url}/users/{username}",params={'key':'username'},headers=hd) as data:
				data = await data.json()
				if data == {'error':None}:
					raise ValueError(f'Username {username} not found')
				try:
					return data['username'], data['statistics']['global_rank'], data['statistics']['country_rank']
				except KeyError:
					token = await get_token()
					hd['Authorization'] = f'Bearer {token}'

async def highest_rank(username: str) -> tuple[str,int,int]:
	global hd
	async with aiohttp.ClientSession() as session:
		while True:
			async with session.get(f"{base_url}/users/{username}",params={'key':'username'},headers=hd) as data:
				data = await data.json()
				if data == {'error':None}:
					raise ValueError(f'Username {username} not found')
				try:
					data['rank_highest']['updated_at'] = int(datetime.strptime(data['rank_highest']['updated_at'],"%Y-%m-%dT%H:%M:%SZ").timestamp())
					return data['username'], data['rank_highest']['rank'], data['rank_highest']['updated_at']
				except KeyError:
					token = await get_token()
					hd['Authorization'] = f'Bearer {token}'

async def acc(username: str) -> tuple[str,float]:
	global hd
	async with aiohttp.ClientSession() as session:
		while True:
			async with session.get(f"{base_url}/users/{username}",params={'key':'username'},headers=hd) as data:
				data = await data.json()
				if data == {'error':None}:
					raise ValueError(f'Username {username} not found')
				try:
					return data['username'], data['statistics']['hit_accuracy']
				except KeyError:
					token = await get_token()
					hd['Authorization'] = f'Bearer {token}'

async def pp(username: str) -> tuple[str,float]:
	global hd
	async with aiohttp.ClientSession() as session:
		while True:
			async with session.get(f"{base_url}/users/{username}",params={'key':'username'},headers=hd) as data:
				data = await data.json()
				if data == {'error':None}:
					raise ValueError(f'Username {username} not found')
				try:
					return data['username'], data['statistics']['pp']
				except KeyError:
					token = await get_token()
					hd['Authorization'] = f'Bearer {token}'
# async def main():
# 	# print(await has_supported('jvxm'))
# 	print(await pp('ash8ydghas8dhja8s'))

# asyncio.run(main())



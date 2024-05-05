# import sqlite3
from typing import Any, Self
import aiosqlite
class CD:

	def __init__(self,path: str = "resources/files/users.db"):
		self.path = path
	# self.connection.autocommit
	# -> 'CD'
	async def __aenter__(self) -> 'CD':
		self.connection = await aiosqlite.connect(database=self.path)
		self.cursor = await self.connection.cursor()
		return self

	async def __aexit__(self, *args):
		await self.cursor.close()
		await self.connection.close()

	async def make_table(self) -> None:
		await self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS usuarios (
			user INTEGER,
            messages INTEGER,
			points REAL
		)
		""")

	async def new_user(self, user: int, messages: int, points: float) -> None:
		await self.cursor.execute(f"""
		INSERT INTO usuarios VALUES
		(?, ?, ?)
		""",(user,messages,points))
		await self.connection.commit()

	async def load_user(self, user: int) -> tuple:
		await self.cursor.execute(f"""
		SELECT * FROM usuarios
		WHERE user = ?
		""",(user,))
		
		return await self.cursor.fetchone()

	async def load_everyone(self, limit: int = -1) -> list[tuple]:
		await self.cursor.execute(f"""
		SELECT * FROM usuarios ORDER BY points DESC LIMIT ?
		""",(limit,))
		return await self.cursor.fetchall()
		
	async def update_user(self, user: int, new_messages: int, new_points: float) -> None:
		await self.cursor.execute(f"""
		UPDATE usuarios
		SET messages = ?,
		    points = ? WHERE user = ?
		""",(new_messages,new_points,user))
		await self.connection.commit()

	async def delete_row(self, user: int) -> None:
		await self.cursor.execute(f"""
		DELETE from usuarios where user = ?
		""",(user,))
		await self.connection.commit()

	async def manual_query(self, query: str) -> None:
		await self.cursor.execute(query)
		await self.connection.commit()


class MiniGame:

	def __init__(self,path: str = "resources/files/mg.db"):
		self.path = path
	# self.connection.autocommit
	
	async def __aenter__(self) -> 'MiniGame':
		self.connection = await aiosqlite.connect(database=self.path)
		self.cursor = await self.connection.cursor()
		return self

	async def __aexit__(self, *args):
		await self.cursor.close()
		await self.connection.close()

	async def make_table(self) -> None:
		await self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS mg (
			id INTEGER,
			user INTEGER,
			timestamp REAL
		)
		""")

	async def new_mg(self, id: int, user: int, timestamp: float) -> None:
		await self.cursor.execute(f"""
		INSERT INTO mg VALUES
		(?, ?, ?)
		""",(id,user,timestamp))
		await self.connection.commit()

	async def load_mg(self, id: int) -> tuple[int, int] | None:
		await self.cursor.execute(f"""
		SELECT user, timestamp FROM mg
		WHERE id = ?
		""",(id,))
		result = await self.cursor.fetchone()
		return (int(result[0]),int(result[1])) if result is not None else None #braindead
		
	async def update_mg(self, id: int, user: int, timestamp: float) -> None:
		await self.cursor.execute(f"""
		UPDATE mg
		SET id = ?, user = ?, timestamp = ?
		WHERE id = ?
		""",(id,user,timestamp,id))
		await self.connection.commit()

	async def delete_row(self, id: int) -> None:
		await self.cursor.execute(f"""
		DELETE FROM mg WHERE id = ?
		""",(id,))
		await self.connection.commit()

	async def manual_query(self, query: str) -> None:
		await self.cursor.execute(query)
		await self.connection.commit()

class CustomEmbed:
	def __init__(self, path: str = 'resources/files/ce.db'):
		self.path = path
	
	async def __aenter__(self):
		self.connection = await aiosqlite.connect(database=self.path)
		self.cursor = await self.connection.cursor()
		return self
	async def __aexit__(self, *args):
		await self.cursor.close()
		await self.connection.close()
	async def make_table(self) -> None:
		await self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS ce (
			user INTEGER,
			tag TEXT,
			embed TEXT
		)
		""")
	async def new_embed(self,user: int, tag: str, embed: dict[Any,Any]) -> None:
		if await self.load_embed(user=user,tag=tag) is not None:
			raise ValueError('Tag already in use')
		await self.cursor.execute("""
		INSERT INTO ce VALUES
		(?, ?, ?)
		""",(user,tag,str(embed)))
		await self.connection.commit()
	async def load_embed(self,user: int, tag: str) -> str | None:
		await self.cursor.execute("""
		SELECT embed FROM ce
		WHERE user = ? AND tag = ?
		""",(user,tag))
		result = await self.cursor.fetchone()
		return result[0] if result is not None else None
	async def delete_embed(self,user: int,tag: str) -> None:
		if await self.load_embed(user=user,tag=tag) is None:
			raise ValueError('No tag found')
		await self.cursor.execute("""
		DELETE FROM ce WHERE user = ? AND tag = ?
		""",(user,tag))
		await self.connection.commit()

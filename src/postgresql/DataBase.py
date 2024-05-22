import asyncpg
import asyncio


class PostgresTransaction:

	def __init__(self):
		self.pool = None

	async def create_pool(self):
		self.pool = await asyncpg.create_pool(
			host='localhost',
			database='',
			user='postgres',
			password=''
		)

	async def execute_query(self, query, params=None, commit=False):
		if self.pool is None:
			await self.create_pool()

		try:
			async with self.pool.acquire() as connection:
				# 트랜잭션 시작
				async with connection.transaction():
					if params:
						result = await connection.fetch(query, *params)
					else:
						result = await connection.fetch(query)
					if commit:
						await connection.execute(query, params)
					return result
		except Exception as e:
			print(f"Error executing query: {e}")
			return None

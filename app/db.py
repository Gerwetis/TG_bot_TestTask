import asyncpg
from datetime import datetime

class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn)

    async def close(self):
        await self.pool.close()

    # Users

    async def add_user(self, tg_id, username):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "INSERT INTO users (tg_id, username) VALUES ($1, $2) ON CONFLICT (tg_id) DO NOTHING RETURNING *",
                tg_id, username
            )

    async def is_authorized(self, tg_id):
        async with self.pool.acquire() as conn:
            user = await conn.fetchrow("SELECT * FROM users WHERE tg_id=$1", tg_id)
            return bool(user)

    async def delete_user(self, tg_id):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM users WHERE tg_id=$1", tg_id)

    # Storage

    async def add_file(self, tg_id, filename, path, file_type):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO storage (tg_id, filename, path, file_type, uploaded_at) VALUES ($1,$2,$3,$4,$5)",
                tg_id, filename, path, file_type, datetime.now()
            )

    async def get_files(self, tg_id):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM storage WHERE tg_id=$1", tg_id)

    async def delete_file(self, file_id):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM storage WHERE id=$1", file_id)

    # Logs
    
    async def add_log(self, tg_id, action):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO logs (tg_id, action, timestamp) VALUES ($1,$2,$3)",
                tg_id, action, datetime.now()
            )

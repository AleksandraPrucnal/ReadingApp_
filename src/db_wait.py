import asyncpg
import asyncio

async def wait_for_db(host: str, port: int, user: str, password: str, database: str, timeout: int = 60):
    deadline = asyncio.get_event_loop().time() + timeout
    last_err = None
    while asyncio.get_event_loop().time() < deadline:
        try:
            conn = await asyncpg.connect(
                host=host, port=port, user=user, password=password, database=database
            )
            await conn.close()
            return
        except Exception as e:
            last_err = e
            await asyncio.sleep(1.5)
    raise RuntimeError(f"Database not ready after {timeout}s") from last_err
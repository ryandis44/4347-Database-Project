import os
import aiomysql
import asyncio
import dns.resolver
from dotenv import load_dotenv
load_dotenv()

try:
    IP = dns.resolver.resolve(os.getenv('REMOTE_DOMAIN'), 'A').rrset[0].to_text()
except dns.resolver.NoAnswer:
    IP = "No answer"

# IP = "192.168.0.12"

POOL = None
async def connect_db() -> None:
    global POOL

    print(f">>> Attempting database pool connection via Cloudflare...")
    try:
        POOL = await aiomysql.create_pool(
                host=IP,
                port=3306,
                user=os.getenv('DATABASE_USERNAME'),
                password=os.getenv('DATABASE_PASSWORD'),
                db=os.getenv('DATABASE'),
                loop=asyncio.get_event_loop(),
                autocommit=True
        )
        print(">>> Database pool connected via Cloudflare!\n")
    except Exception as e:
        print(f"\n##### FAILED TO CONNECT TO DATABASE! #####\n{e}\n")

async def check_pool() -> None:
    global POOL
    if POOL is None:
        await connect_db()
    if POOL.closed:
        print(f"\n\n####### DATABASE POOL CONNECTION LOST! Attempting to reconnect... #######")
        await connect_db()


class Database:

    def __init__(self, file):
        self.file = file

    async def execute(self, exec_cmd: str, p=False) -> str|int|float|list:
        if p or os.getenv('DATABASE_DEBUG') == 1: print(exec_cmd)
        global POOL
        for attempt in range(1,6):
            try:
                async with POOL.acquire() as conn:
                    cursor = await conn.cursor()
                    await cursor.execute(exec_cmd)
                    conn.close()
            except Exception as e:
                if attempt < 5:
                    if os.getenv('DATABASE_DEBUG') != "1": await asyncio.sleep(5)
                    await check_pool()
                    continue
                else:
                    if p or os.getenv('DATABASE_DEBUG') == 1:
                        print(f"\nASYNC DATABASE ERROR! [{self.file}] Could not execute: \"{exec_cmd}\"\n{e}")
            break
        
        if exec_cmd.startswith("SELECT"):
            val = await cursor.fetchall()
            await cursor.close()
            if len(val) == 1:
                if len(val[0]) == 1:
                    return val[0][0]
            return val if val != () else []
        await cursor.close()
        return
    
    def exists(self, rows) -> bool:
        return rows > 0
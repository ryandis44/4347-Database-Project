import asyncio

from Database.DatabaseConnector import connect_db
from example import database_interaction_example



async def main() -> None:
    await connect_db()
    await database_interaction_example()
    
    

asyncio.run(main())
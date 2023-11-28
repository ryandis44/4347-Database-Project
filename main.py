import asyncio
# from Database.DataSort import insert_into_db

from Database.DatabaseConnector import connect_db
from Database.DatabaseSearch import search_database
from example import database_interaction_example
from Database.BookLoans import Borrower

l = Borrower(card_id=4)

async def main() -> None:
    await connect_db()
    
    
    # await l.check_out(isbn13=9780452264465)
    
    val = await search_database("9780452264465")
    print(val)
    
    
    

asyncio.run(main())
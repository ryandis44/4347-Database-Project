import asyncio
# from Database.DataSort import insert_into_db

from Database.DatabaseConnector import connect_db
from Database.DatabaseSearch import loan_search, search_database
from Database.BookLoans import Borrower
from Database.Fines import Fines

l = Borrower(card_id=4)

async def main() -> None:
    await connect_db()
    
    
    # await l.check_out(isbn13=9780452264465)
    
    val = await loan_search("9780452264465")
    # fine = Fines(val[0])
    # await fine.ainit()
    # print(fine.fine_amt)
    # print(fine.loan_id)
    print(val)
    
    
    

asyncio.run(main())
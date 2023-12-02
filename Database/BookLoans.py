import time
from Database.DatabaseConnector import Database
from datetime import datetime

db = Database("Database.BookLoans.py")


class Borrower:
    
    def __init__(self, card_id: int):
        self.card_id = card_id
    
    def __epoch_to_datetime(self, epoch):
        return datetime.fromtimestamp(epoch).strftime("%A, %B %d, %Y %I:%M:%S")
    
    async def id_check(self) -> bool:
        val = await db.execute(
            "SELECT COUNT(*) FROM BORROWER WHERE "
            f"card_id='{self.card_id}'"
        )
        if val > 0:
            return True
        else:
            return False
    
    async def check_out(self, isbn13: str) -> [bool, str]:
        val = await db.execute(
            "SELECT COUNT(*) FROM BOOK_LOANS WHERE "
            f"date_in IS NULL AND isbn13='{isbn13}'"
        )
        if val > 0:
            return [False, "Book already checked out."]
        
        val = await db.execute(
            "SELECT COUNT(*) FROM BOOK_LOANS WHERE "
            f"card_id='{self.card_id}' AND date_in IS NULL"
        )
        if val >= 3:
            return [False, "Checkout limit of 3 reached."]
        
        
        date_out = int(time.time())
        due_date = date_out + (604800 * 2)
        
        
        # Insert record into database
        await db.execute(
            "INSERT INTO BOOK_LOANS (card_id, isbn13, date_out, due_date) VALUES "
            f"('{self.card_id}', '{isbn13}', '{date_out}', '{due_date}')"
        )
        
        
        # Return loan ID to calling code
        loan_id = await db.execute(
            "SELECT loan_id FROM BOOK_LOANS WHERE "
            f"card_id='{self.card_id}' AND isbn13='{isbn13}' AND date_out='{date_out}'"
        )
        return [True, f"Loan ID: {loan_id}, Due Date: {self.__epoch_to_datetime(due_date)}"]
    
    async def check_in(self, loan: list) -> None:
        # select from loan search
        date_in = int(time.time())
        due_date = loan[4]

        await db.execute(
            "UPDATE BOOK_LOANS "
            f"SET date_in='{date_in}' "
            f"WHERE loan_id='{loan[0]}'"
        )

        # if date_in >= due_date: await self.__handle_fines(loan=loan)

    
    async def __handle_fines(self, loan: list) -> None:
        pass
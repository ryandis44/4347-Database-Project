import aiomysql
import asyncio
import time

from Database.DatabaseConnector import Database
from Database.BookLoans import Borrower
from datetime import datetime

db = Database("fines.py")


class Fines:
    
    def __init__(self, loan: list) -> None:
        self.loan = loan
    
    async def calculate_fine(self) -> None:
        due_date = self.loan[4]
        date_in = int(time.time())
        
        if date_in <= due_date:
            return  # No fine for on-time returns
        
        difference_in_days = (date_in - due_date) // (24 * 3600)
        fine_amt = round(difference_in_days * 0.25, 2)
        
        await self.__update_or_create_fine(self.loan, fine_amt)
    
    async def __update_or_create_fine(self, fine_amt: float) -> None:
        card_id = self.loan[1]
        existing_fine = await db.execute(
            "SELECT fine_amt, paid FROM FINES WHERE "
            f"loan_id='{self.loan[0]}'"
        )
        
        if existing_fine:
            if not existing_fine[1]:  # If not paid
                if existing_fine[0] != fine_amt:
                    await db.execute(
                        "UPDATE FINES SET fine_amt = "
                        f"'{fine_amt}' WHERE loan_id='{self.loan[0]}'"
                    )
        else:
            await db.execute(
                "INSERT INTO FINES (loan_id, fine_amt, paid) VALUES "
                f"('{self.loan[0]}', '{fine_amt}', '0')"
            )
    
    async def get_fine_amt(self) -> int:
        pass
    
    async def pay_fine(self, loan_id: str) -> None:
        loan = await db.execute(
            "SELECT * FROM BOOK_LOANS WHERE "
            f"loan_id='{loan_id}'"
        )
        if not loan or loan[5]:  # If loan not found or already returned
            return
        
        await db.execute(
            "UPDATE FINES SET paid = '1' WHERE "
            f"loan_id='{loan_id}'"
        )
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
    
    async def ainit(self) -> None:
        await self.calculate_fine()
    
    @property
    def fine_amt(self) -> float:
        difference_in_days = (int(time.time()) - self.loan[4]) // (24 * 3600)
        amt = round(difference_in_days * 0.25, 2)
        return amt if amt > 0 else 0.0

    @property
    def loan_id(self) -> str: return self.loan[0]
    
    async def calculate_fine(self) -> None:
        due_date = self.loan[4]
        date_in = int(time.time())
        
        if date_in <= due_date:
            return  # No fine for on-time returns
        
        await self.__update_or_create_fine()
    
    async def __update_or_create_fine(self) -> None:
        existing_fine = await db.execute(
            "SELECT fine_amt, paid FROM FINES WHERE "
            f"loan_id='{self.loan[0]}'"
        )
        
        if existing_fine != []:
            if existing_fine[0][1] == "0":  # If not paid
                if existing_fine[0][0] != self.fine_amt:
                    await db.execute(
                        "UPDATE FINES SET fine_amt = "
                        f"'{self.fine_amt}' WHERE loan_id='{self.loan[0]}'"
                    )
        else:
            await db.execute(
                "INSERT INTO FINES (loan_id, fine_amt, paid) VALUES "
                f"('{self.loan[0]}', '{self.fine_amt}', '0')"
            )
    
    async def pay_fine(self) -> None:
        await db.execute(
            "UPDATE FINES SET paid = '1' WHERE "
            f"loan_id='{self.loan_id}'"
        )
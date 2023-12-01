# Initial data import file

import xlwings as xw
import asyncio
from Database.DatabaseConnector import Database
db = Database("DataSort.py")

def sanitize_name(name) -> str|None:
    if name is None: return None
    return str(name).replace("'", "''").strip()


async def insert_into_db():

    ws = xw.Book("borrowers.csv").sheets['borrowers']
    ids = ws.range("A2:A1001").value
    firsts = ws.range("C2:C1001").value
    lasts = ws.range("D2:D1001").value
    addresses = ws.range("F2:F1001").value
    citys = ws.range("G2:G1001").value
    states = ws.range("H2:H1001").value
    phones = ws.range("I2:I1001").value
    ssns = ws.range("B2:B1001").value
    
    
    
    for i, id in enumerate(ids):
        
        id = int(id[2:])
        print(id)
        
        bname = f"{firsts[i]} {lasts[i]}"
        print(bname)
        
        address = f"{addresses[i]}, {citys[i]} {states[i]}"
        print(address)
        
        phone = phones[i]
        print(phone)
        
        ssn = ssns[i]
        print(ssn)
        
        await db.execute(
            "INSERT INTO BORROWER (card_id, ssn, bname, address, phone) VALUES "
            f"('{id}', '{ssn}', '{bname}', '{address}', '{phone}')"
        )
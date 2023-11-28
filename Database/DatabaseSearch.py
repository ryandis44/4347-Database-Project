from Database.DatabaseConnector import Database

db = Database("Database.DatabaseSearch.py")


# Returns book and FALSE if book is NOT available or TRUE if it is
async def search_database(query: str) -> list:
    
    val = await db.execute(
        "SELECT B.isbn13, B.title, A.name FROM BOOKS AS B "
        "INNER JOIN BOOK_AUTHORS AS BA ON BA.ISBN13 = B.ISBN13 "
        "INNER JOIN AUTHORS AS A ON A.AUTHOR_ID = BA.AUTHOR_ID WHERE ("
        f"B.isbn13 LIKE '%{query}%' OR "
        f"B.title LIKE '%{query}%' OR "
        f"A.name LIKE '%{query}%')"
        "LIMIT 50"
    )
    
    if val == []: return [None]
    
    books = []
    for book in val:
        book_loan = await db.execute(
            "SELECT COUNT(*) FROM BOOK_LOANS WHERE "
            f"isbn13='{book[0]}'"
        )
        books.append(
            [
                book,
                False if book_loan > 0 else True
            ]
        )
        
    return books

async def loan_search(query: str) -> list:
    
    val = await db.execute(
        "SELECT * FROM BOOK_LOANS AS BA "
        "INNER JOIN BORROWER AS B ON BA.card_id = B.card_id WHERE "
        f"BA.isbn13 LIKE '%{query}%' OR "
        f"BA.card_id LIKE '%{query}%' OR "
        f"B.bname LIKE '%{query}%' "
        "LIMIT 50"
    )
    
    if val == []: return [None]
    return val

async def create_borrower(ssn: str, bname: str, address: str, phone: str) -> [str, bool]:
    
    val = await db.execute(
        "SELECT COUNT(*) FROM BORROWER WHERE "
        f"ssn='{ssn}'"
    )
    if val > 0: return ["SSN already exists", False]
    
    await db.execute(
        "INSERT INTO BORROWER (ssn, baname, address, phone) VALUES "
        f"('{ssn}', '{bname}', '{address}', '{phone}')"
    )
    
    card_id = await db.execute(
        "SELECT card_id FROM BORROWER WHERE "
        f"ssn='{ssn}'"
    )
    return [card_id, True]
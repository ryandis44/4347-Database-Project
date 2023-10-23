from Database.DatabaseConnector import Database

db = Database("example.py")

async def database_interaction_example() -> None:
    
    departments = await db.execute("SELECT * FROM DEPARTMENT")
    print(f"{departments}\n\n")
    for item in departments:
        print(item)
    
    print("\n")
    
    employees = await db.execute("SELECT * FROM EMPLOYEE")
    for employee in employees:
        print(employee)
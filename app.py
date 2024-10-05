from database_functions import database_worker

userDatabase = database_worker("user.db")

clothingDatabase = database_worker("clothing.db")

def create_database():
    db = userDatabase
    query_user = '''CREATE table if not exists user (
        id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        email TEXT,
        password TEXT
    )'''


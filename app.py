from database_functions import database_worker

def create_database():
    db = database_worker("clothing.db")
    query_user = '''CREATE table if not exists user (
        id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        email TEXT,
        password TEXT
    )'''
    query_clothing = '''CREATE TABLE IF NOT EXISTS clothing (
        id INTEGER PRIMARY KEY,
        owner TEXT,
        category TEXT,
        subtype TEXT,
        colour TEXT,
        occasion TEXT,
        FOREIGN KEY (user_id) REFERENCES user(id) on delete cascade
    )
    '''

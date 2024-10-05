import sqlite3

class database_worker:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

# creates and connects with database

    def search(self, query):
        result = self.cursor.execute(query).fetchall()
        return result

# searches for items in database

    def run_save(self, query):
        self.cursor.execute(query)
        self.connection.commit()

# save changes made in database

    def close(self):
        self.connection.close()

# close database

    def run_fetchone(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
    
# fetches items from database after seached


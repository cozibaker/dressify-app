from database_functions import database_worker

def create_database():
    db = database_worker("dressify.db")
    query_user = '''CREATE table if not exists user (
        id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        email TEXT,
        password TEXT
    )'''
    query_clothing = '''CREATE table if not exists clothing (
        id INTEGER PRIMARY KEY,
        image VARCHAR(100),
        category TEXT,
        subtype TEXT,
        colour TEXT,
        occasion TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(id) on delete cascade
    )
    '''

def add_clothing(image, category, subtype, colour, occasion, user_id):
    db = database_worker("dressify.db")
    db.run_save(""" INSERT INTO clothes VALUES
            (image, category, subtype, colour, occasion, user_id)
               """)
    
@app.route('/file/<filename>')
def file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

create_database()

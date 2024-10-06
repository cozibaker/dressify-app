from database_functions import database_worker

from werkzeug.utils import secure_filename
import os
import pip
from flask import Flask, __main__, render_template, request, redirect, make_response, send_from_directory, url_for
import random

def create_database():
    db = database_worker("dressify.db")
    query_user = '''CREATE TABLE if not exists user (
        id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        email TEXT,
        password TEXT
    )'''
    query_clothing = '''CREATE TABLE if not exists clothing (
        id INTEGER PRIMARY KEY,
        image VARCHAR(100),
        category TEXT,
        subtype TEXT,
        colour TEXT,
        occasion TEXT,
        user_id INTEGER,
        suitedWeather INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(id) on delete cascade
    )
    '''

    db.run_save(query_user)
    db.run_save(query_clothing)
    db.close()

def add_clothing(img, cat, st, col, oc, u_id):
    db = database_worker("dressify.db")
    db.run_save(""" INSERT INTO clothing VALUES (img, cat, st, col, oc, u_id) """)
    
def remove_clothing(clothing_id):
    db = database_worker("dressify.db")
    db.run_save(""" DELETE FROM clothing WHERE id = clothing_id """)

def random_outfit_generator(id, oc, w):
    clothingDict = {}
    db = database_worker("dressify.db")
    for t in ["top", "jacket", "bottom", "shoes"]:
        c = db.cursor()
        c.execute(""" SELECT * from clothing WHERE id = user_id AND 
                  (category = t AND (occasion = oc AND suitedWeather = w)) """)
        L = c.fetchall()
        clothingDict[t] = L[random.randrange(0, len(L))]
    return clothingDict

create_database()

def file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app = Flask(__name__)

@app.route('/file/<filename>')
@app.route('/outfit_randomization', methods=['GET', 'POST'])

def outfit_randomization():

    db = database_worker("dressify.db")

    userId = 1 #arbitrary value, would ideally be received from the database
    currentOccasion = 'Formal' #arbitrary values
    currentWeather = 20 #arbitrary values

    random_outfit = random_outfit_generator(userId, currentOccasion, currentWeather)
    top = random_outfit["top"]
    top_id = top[0]

    jacket = random_outfit["jacket"]
    jacket_id = jacket[0]

    bottom = random_outfit["bottom"]
    bottom_id = bottom[0]

    shoes = random_outfit["shoes"]
    shoes_id = shoes[0]

    image1 = db.run_fetchone(f"SELECT image from clothing WHERE id = top_id")
    image2 = db.run_fetchone(f"SELECT image from clothing WHERE id = jacket_id")
    image3 = db.run_fetchone(f"SELECT image from clothing WHERE id = bottom_id")
    image4 = db.run_fetchone(f"SELECT image from clothing WHERE id = shoes_id")


    return render_template('randomizationPage.html', image1=image1, image2=image2, image3=image3, image4=image4)

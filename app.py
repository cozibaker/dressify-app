from database_functions import database_worker

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
        c.execute(""" SELECT * from clothing WHERE id = user_id AND (type = t AND (occasion = oc AND suitedWeather = w)) """)
        L = c.fetchall()
        clothingDict[t] = L[random.randrange(0, len(L))]
    return clothingDict
    

app = Flask(__main__)

@app.route('/file/<filename>')
def file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

create_database()

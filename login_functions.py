from urllib import request

import pip
import app
from database_functions import database_worker

from flask import Flask, render_template, request, redirect, make_response, send_from_directory, url_for

@app.route('/login',methods=['GET', 'POST'])

def signup():
    msg = ""
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        passwd = request.form['passwd']
        db = database_worker('dressify.db')
        new_user = """INSERT INTO dressify(username, email, password) 
                      VALUES (username, email, passwd)"""
        db.run_save(new_user)
        db.close()

        # Create a response object
        response = make_response(redirect(url_for('build_pet', user_id=username)))

        # Set a cookie with the username
        response.set_cookie('username', username)

        return response
    return render_template("signup.html")

def login():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']
        if len(username)>0 and len(passwd)>0:
            db = database_worker('dressify.db')
            user = db.search(f"SELECT * from dressify where username='{username}'")
            if user:
                user = user[0] # search returns a list, so here I select one
                id, username, email, hash = user
                if check_password(hashed_password=hash, user_password=passwd):
                    resp = make_response(redirect(url_for('profile', username=username)))
                    resp.set_cookie('username', f"{username}")
                    return resp
                else:
                    msg='Incorrect username or password'
            else:
                return redirect(url_for('profile', username=username))
    return render_template("login.html", message = msg)
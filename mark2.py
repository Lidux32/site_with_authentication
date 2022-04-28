import os
from flask import Flask, render_template, flash
from flask import redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import sqlite3

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128), index=True, unique=True)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    
@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/album', methods=['post', 'get'])
def alb():
    return render_template('album.html')



@app.route('/registration', methods=['post', 'get'])
def regist():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 

        user = User.query.filter_by(username=username).first()
        if user:
            return redirect (url_for('regist'))
        
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))    

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('logi'))
    
    return render_template('registration.html')



@app.route('/login', methods=['post', 'get'])
def logi():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        con = sqlite3.connect('site.db')
        completion = False
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM User")
            rows = cur.fetchall()

        for row in rows:
            dbUser = row[0]
            dbPass = row[1]
            if dbUser==username:
                completion=check_password(dbPass, password)      
            
            return redirect(url_for('alb'))

    return render_template('login.html')





if __name__=="__main__":
    app.run(debug=True, port=5002)

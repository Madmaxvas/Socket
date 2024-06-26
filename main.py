from flask import Flask
from flask_login import LoginManager
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user, current_user
from tools.forms import LoginForm, RegisterForm, Videoupload
from flask import render_template, flash, redirect, url_for, request
from flask_bs4 import Bootstrap
from misc import db
from tools.db import User
import os
import shortuuid
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'lologin'


db_cursor = db.cursor()
db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
a = db_cursor.fetchall()
if not a:
    db_cursor.execute('''CREATE TABLE info (                       
                                                mail TEXT PRIMARY KEY,
                                                username TEXT,
                                                name TEXT NOT NULL,
                                                password TEXT NOT NULL
                                                );''')
    db.commit()
    db_cursor.execute('''CREATE TABLE videous (          
                                                videoname TEXT PRIMARY KEY,
                                                username TEXT,
                                                fotos TEXT,
                                                opis TEXT,
                                                tags TEXT);''')
    db.commit()
db_cursor.close()





@login_required
@app.route('/upload', methods=['GET','POST'])
def upload():
    form1 = Videoupload()
    if form1.photo.data and form1.video.data:
        db_cursor = db.cursor()
        db_cursor.execute("SELECT * FROM info")
        out = db_cursor.fetchall()
        for i in out:
            if current_user.username in i:
                    vstav1 = shortuuid.ShortUUID().random(length=22)
                    form1.video.data.save('static/videous/' + vstav1 + '.'+ form1.video.data.filename.split('.')[1])
                    form1.photo.data.save('static/images/' + vstav1 +'.'+ form1.photo.data.filename.split('.')[1])
                    photovst = vstav1
                    db_cursor.execute('''INSERT or IGNORE INTO videous (videoname,username,fotos,opis,tags) VALUES (?, ?, ?, ?, ?)''', (vstav1,current_user.username,photovst,form1.opis.data,form1.tags.data))
        db.commit()
        db_cursor.close()
    return render_template('upload.html', form=form1)


@app.route('/login', methods=['GET', 'POST'])
def lologin():
    form = LoginForm()
    if form.validate_on_submit():
        db_cursor = db.cursor()
        db_cursor.execute("SELECT * FROM info")
        out = db_cursor.fetchall()
        db_cursor.close()
        print(out)
        for i in out:
            if i[1] == form.username.data and i[3] == form.password.data:
                user = User(i[0], i[1], i[2], i[3])
                login_user(user=user)
                return render_template('test.html', title='Вход')
        flash("Ошибочный username или password")
        return redirect(url_for('lologin'))
    return render_template('login.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_cursor = db.cursor()
        db_cursor.execute("SELECT * FROM info")
        out = db_cursor.fetchall()
        for i in out:
            if i[0] == form.email.data:
                print("Данный email уже зарегистрирован!")
                db_cursor.close()
                return redirect(url_for('register'))
            elif i[1] == form.username.data:
                print("Данный UserName уже зарегистрирован")
                db_cursor.close()
                return redirect(url_for('register'))

        db_cursor.execute(
            "INSERT or IGNORE INTO info ( name, mail, password, username) VALUES (?, ?, ?, ?)",
            (form.name.data,  form.email.data, form.password.data,form.username.data))
        db.commit()
        print('Вы зарегистрированы!')
        db_cursor.close()
        return redirect(url_for('lologin'))
    return render_template('register.html', title='Регистрация', form=form)


@login.user_loader
def load_user(user_id):
    print(f"login:{user_id}")
    db_cursor1 = db.cursor()
    db_cursor1.execute("SELECT * FROM info WHERE username=(?)", (user_id,))
    db_data = db_cursor1.fetchone()
    print(db_data)
    db_cursor1.close()
    if db_data is not None:
        return User(db_data[0], db_data[1], db_data[2], db_data[3])
    else:
        return None

if __name__ == '__main__':
    app.run()

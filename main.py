from flask import Flask
from flask_login import LoginManager
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user, current_user
from tools.forms import LoginForm, RegisterForm
from flask import render_template, flash, redirect, url_for
from flask_bs4 import Bootstrap
from misc import db
from tools.db import User
import os
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
                                                password TEXT NOT NULL);''')
    db.commit()
db_cursor.close()


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
                return redirect(url_for('main'))
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

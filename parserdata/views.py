from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from parserdata import app, login_manager, db
from parser import Parser
from parserdata.models import User
from parserdata.forms import LoginForm, RegistrationFrom

import os
from dotenv import load_dotenv

load_dotenv()


@app.route('/')
def index():
    return render_template('index.html', parsed_data=globals().get('parsed_data'), title='Data')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == str(user_id)).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data,
                                    password=form.password.data).first()
        if user:
            login_user(user)
            flash('Success', "success")
            return redirect(url_for('index'))
        else:
            flash('Invalid login or password specified.', "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Login')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationFrom()

    if form.validate_on_submit():
        if not form.login.data or not form.password.data:
            flash('Data is incorrect')
            return redirect(url_for('registration'))

        user = User(login=form.login.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('New account created', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Registration')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/reload_data')
def reload_data():
    if current_user.is_authenticated:
        global parsed_data
        parser = Parser()
        parser.data = {'browser': 'Safari', 'login': os.getenv('login'), 'password': os.getenv('password')}
        parsed_data = parser.parse()
        flash('Success', 'success')
    else:
        flash('You are not <a href="login">logged in.</a>', 'danger')
    return redirect(url_for('index'))

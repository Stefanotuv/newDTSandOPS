__author__ = "stefanotuv"

from flask import request, render_template, jsonify, url_for, redirect, Blueprint
from DTSandOPS.users.models.user import User
from DTSandOPS.users.forms import RegistrationForm, LoginForm
from DTSandOPS import db

from werkzeug import secure_filename
from DTSandOPS.utilities.global_variable import *


from flask_login import login_user, logout_user,current_user
from flask import flash

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    login_form = LoginForm()
    print(login_form.errors)
    if login_form.validate_on_submit():
        email = User.query.filter_by(email=login_form.email.data).first()
        if email is None or not email.check_password(login_form.password.data):
            # flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(email, remember=login_form.remember_me.data)
        return redirect(url_for('login_confirm'))
    return render_template('login.html', title='Sign In', login_form=login_form)

@users.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login_confirm'))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user = User(user_name=registration_form.user_name.data, email=registration_form.email.data)
        user.set_password(registration_form.password.data)
        db.session.add(user)
        db.session.commit()
        # add register confirmation
        flash(f'Congratulations { registration_form.user_name.data }, you are now a registered user!','success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='SignUp', registration_form=registration_form)

@users.route('/login_confirm')
def login_confirm():
    return render_template('login_confirm.html', title='login_confirm')

@users.route("/logout")
def logout():
    logout_user()
    return render_template('logout.html')

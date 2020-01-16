from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from journal_app.extensions import db
from journal_app.models import User, RegisterForm, LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('main.dashboard'))
            return '<h1>Invalid email or password</h1>'
    return render_template('index.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,
                                                 method='sha256')
        new_user = User(name=form.name.data,
                        email=form.email.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.index'))
    return render_template('signup.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

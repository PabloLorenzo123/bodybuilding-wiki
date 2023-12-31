from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from .models import User, Role
from . import auth
from .. import db
from .forms import EditProfileAdminForm, EditProfileForm
from ..helpers import admin_required


"""is typically used to register a function that will be executed before any request to the entire Flask application, """
@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if User.query.filter_by(email=email).first():
            flash('Email is already in use', category='error')
        elif User.query.filter_by(username=username).first():
            flash('Username is already in use', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.')
        elif not password1 or not password2:
            flash('Fill all the fields.')
        else:
            new_user = User(email=email, username=username,
                            password=password1) # Password is generated automatically thanks to the property setter in models.py
            db.session.add(new_user)
            db.session.commit()
            flash(f"Welcome {username}!")
            login_user(new_user, remember=True)
            return redirect(url_for('main.index'))

    # GET request.
    return render_template('auth/signup.html')
    

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is not None and user.verify_password(request.form.get('password')):
            login_user(user, remember=True)
            next = request.args.get('next')
            print(next)
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            flash(f"Welcome back {user.username}!")
            return redirect(next)
        flash('Invalid username or password.', category='error')
    # GET request
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/user/<username>')
def user_detail(username):
    user_profile = User.query.filter_by(username=username).first_or_404()
    return render_template('auth/user.html', user_profile=user_profile)


@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def user_update():
    form = EditProfileForm()
    # POST request.
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash(f'{current_user.name} your profile has been updated.')
        return redirect(url_for('auth.user_detail', username=current_user.username))
    # GET request.
    form.name.data = current_user.name
    form.location.data = current_user.location
    return render_template('auth/edit_profile.html', form=form)
